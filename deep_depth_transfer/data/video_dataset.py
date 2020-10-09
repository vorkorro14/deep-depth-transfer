import numpy as np
import torch
from torch.utils.data import Dataset


class VideoDataset(Dataset):
    def __init__(self,
                 left_video_dataset,
                 right_video_dataset=None,
                 pose_dataset=None,
                 transform=None):
        self._left_video_dataset = left_video_dataset
        self._right_video_dataset = right_video_dataset
        self._pose_dataset = pose_dataset
        self._transform = transform

    def set_transform(self, transform):
        self._transform = transform

    def get_image_size(self):
        return self._left_video_dataset.get_image_size()

    def __getitem__(self, index):
        if self._transform is None:
            raise AttributeError("Transform is None, you should apply set transform before")
        image_data_point = {
            "image": np.array(self._left_video_dataset[index]),
            "image2": np.array(self._right_video_dataset[index]),
            "image3": np.array(self._left_video_dataset[index + 1]),
            "image4": np.array(self._right_video_dataset[index + 1])
        }
        image_data_point = self._transform(**image_data_point)
        image_data_point = {
            "left_current_image": torch.from_numpy(image_data_point["image"]).permute(2, 0, 1),
            "right_current_image": torch.from_numpy(image_data_point["image2"]).permute(2, 0, 1),
            "left_next_image": torch.from_numpy(image_data_point["image3"]).permute(2, 0, 1),
            "right_next_image": torch.from_numpy(image_data_point["image4"]).permute(2, 0, 1),
        }
        if self._pose_dataset is None:
            return {**image_data_point}
        return {**image_data_point, **self._pose_dataset[index]}

    def __len__(self):
        return len(self._left_video_dataset) - 1