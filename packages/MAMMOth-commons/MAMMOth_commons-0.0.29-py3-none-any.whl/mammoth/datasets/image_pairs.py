from typing import List
from mammoth.datasets import Dataset


class ImagePairs(Dataset):
    def __init__(
        self,
        path,
        root_dir,
        target,
        data_transform,
        batch_size,
        shuffle,
        cols,
        img1_path_format: str = "{root}/{col}/{id}.png",
        img2_path_format: str = "{root}/{col}/{id}.png",
    ):
        """
        Args:
            path (str): Path to the CSV file with annotations (should involve the columns img1_name|img2_name|attribute1|...|attributeN).
            root_dir (str): Root image dataset directory (eg the db_path for the UC2).
            target (str): The target attribute to be predicted (eg the attack for UC2).
            data_transform (callable): A function/transform that takes in an image and returns a transformed version.
            batch_size (int): How many samples per batch to load.
            shuffle (bool): Set to True to have the data reshuffled every time they are obtained.
        """

        self.path = path
        self.root_dir = root_dir
        self.target = target
        self.data_transform = data_transform
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.img1_path_format = img1_path_format
        self.img2_path_format = img2_path_format
        self.cols = cols

    def to_torch(self, sensitive: List[str]):
        # dynamic dependencies here to not force a torch dependency on commons from components that don't need it
        from torch.utils.data import DataLoader
        from mammoth.datasets.backend.torch_implementations import (
            PytorchImagePairsDataset,
        )

        torch_dataset = PytorchImagePairsDataset(
            csv_path=self.path,
            root_dir=self.root_dir,
            target=self.target,
            sensitive=sensitive,
            data_transform=self.data_transform,
            img1_path_format=self.img1_path_format,
            img2_path_format=self.img2_path_format,
        )

        return DataLoader(
            dataset=torch_dataset, batch_size=self.batch_size, shuffle=self.shuffle
        )
