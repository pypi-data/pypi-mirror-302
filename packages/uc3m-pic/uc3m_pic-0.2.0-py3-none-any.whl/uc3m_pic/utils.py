import os
import torch
from PIL import Image

def conv2d_output_size(input_size, kernel_size, padding=0, stride=1,
                          pool_kernel_size=1, pool_stride=1):
    '''
    Computes the output size of a convolutional layer, supposing square 
    dimensions in input, kernel, padding and stride, and a pooling layer with
    symmetric dimensions in kernel and stride.

    Parameters
    ----------
    input_size : int
        Input size 
    kernel_size : int
        Kernel size
    padding : int, optional
        Padding size. The default is 0.
    stride : int, optional
        Stride size. The default is 1.
    pool_kernel_size : int, optional
        Pooling kernel size. The default is 1.
    pool_stride : int, optional
        Pooling stride size. The default is 1.
    
    Returns
    -------
    pool_output : int
        Output size of the pooling layer
    '''
    
    conv_output = (input_size + 2*padding - kernel_size) // stride + 1
    pool_output = (conv_output - pool_kernel_size) // pool_stride + 1

    return pool_output


def train(model, dataloader, loss_fn, optimizer, lr_scheduler=None):
    
    '''
    Training loop

    Parameters
    ----------
    model : torch.nn.Module
        Model to train
    dataloader : torch.utils.data.DataLoader
        Dataloader with the training data
    loss_fn : torch.nn.Module
        Loss function
    optimizer : torch.optim.Optimizer
        Optimizer

    Returns
    -------
    None
    '''

    device = next(model.parameters()).device
    model.train()
    for x, y in dataloader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        y_pred = model(x)
        loss = loss_fn(torch.log(y_pred), y)
        loss.backward()
        optimizer.step()
    if lr_scheduler:
        lr_scheduler.step()


def test(model, dataloader, loss_fn, metrics_fn):

    '''
    Test loop

    Parameters
    ----------
    model : torch.nn.Module
        Model to test
    dataloader : torch.utils.data.DataLoader
        Dataloader with the testing data
    loss_fn : torch.nn.Module
        Loss function
    metrics_fn : torchmetrics.Metric
        Metric function

    Returns
    -------
    loss_fn : float
        Loss value
    metrics_fn : float
        Metric value
    '''
    
    device = next(model.parameters()).device
    model.eval()
    metrics_fn = metrics_fn.to(device)
    metrics_fn.reset()
    with torch.no_grad():
        loss = 0
        for x, y in dataloader:
            x, y = x.to(device), y.to(device)
            y_pred = model(x)
            loss += loss_fn(torch.log(y_pred), y).sum()
            metrics_fn.update(y_pred, y)
        
        loss = loss / len(dataloader.dataset)
        metrics = metrics_fn.compute()

    return loss, metrics


class InMemoryDataset(torch.utils.data.Dataset):
    '''
    Dataset class that loads all images into memory

    Parameters
    ----------
    root : str
        Path to the root directory
    transform : callable, optional
        Transform to apply to the images. The default is None.
    
    Returns
    -------
    None
    '''


    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        self.data = None  # Use None for an uninitialized tensor

        # Load all images into memory
        self._load_images()

    def _load_images(self):
        labels = sorted(os.listdir(self.root))
        self.num_classes = len(labels)
        num_images = sum(len(os.listdir(os.path.join(self.root, label))) for label in labels)

        # Allocate memory for images as uint8 tensors
        self.data = torch.zeros((num_images, 3, 320, 425), dtype=torch.uint8)
        self.labels = torch.zeros((num_images, 1), dtype=torch.uint8)

        current_index = 0
        for idx, label in enumerate(labels):
            label_path = os.path.join(self.root, label)
            if os.path.isdir(label_path):
                for filename in os.listdir(label_path):
                    image_path = os.path.join(label_path, filename)
                    image = Image.open(image_path).convert("RGB")
                    if self.transform:
                        image = self.transform(image)
                    image = (255 * image).to(torch.uint8)  # Convert to uint8
                    self.data[current_index] = image
                    self.labels[current_index] = idx
                    current_index += 1

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image = self.data[idx].to(torch.float32) / 255.0  # Convert back to float32
        label = self.labels[idx].to(torch.float32)
        # Convert to one-hot encoding
        # ! This one-hot encoding has not been tested
        label = torch.nn.functional.one_hot(label, num_classes=self.num_classes).squeeze()
        return image, label