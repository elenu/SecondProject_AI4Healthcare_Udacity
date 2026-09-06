"""
Contains class that runs inferencing
"""
import torch
import numpy as np

from networks.RecursiveUNet import UNet

from utils.utils import med_reshape

class UNetInferenceAgent:
    """
    Stores model and parameters and some methods to handle inferencing
    """
    def __init__(self, parameter_file_path='', model=None, device="cpu", patch_size=64):

        self.model = model
        self.patch_size = patch_size
        self.device = device

        if model is None:
            self.model = UNet(num_classes=3)

        if parameter_file_path:
            self.model.load_state_dict(torch.load(parameter_file_path, map_location=self.device))

        self.model.to(device)

    def single_volume_inference_unpadded(self, volume):
        """
        Runs inference on a single volume of arbitrary patch size,
        padding it to the conformant size first

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        # Pad/crop the volume to the patch size expected by the model along
        # the Y and Z axes, keeping the original X (slice) dimension.
        padded_volume = med_reshape(volume, (volume.shape[0], self.patch_size, self.patch_size))

        padded_prediction = self.single_volume_inference(padded_volume)

        # Crop the prediction back down to the original volume's dimensions.
        prediction = np.zeros(volume.shape)
        slices = tuple(slice(0, min(s, n)) for s, n in zip(volume.shape, padded_prediction.shape))
        prediction[slices] = padded_prediction[slices]

        return prediction

    def single_volume_inference(self, volume):
        """
        Runs inference on a single volume of conformant patch size

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        self.model.eval()

        # Assuming volume is a numpy array of shape [X,Y,Z] and we need to slice X axis
        slices = []

        for i in range(volume.shape[0]):
            slice_ = volume[i, :, :]
            slice_ = torch.from_numpy(slice_).unsqueeze(0).unsqueeze(0).float().to(self.device)
            with torch.no_grad():
                prediction = self.model(slice_)
                prediction = torch.argmax(prediction, dim=1)
                prediction = prediction.squeeze(0).cpu().numpy()
            slices.append(prediction)

        return np.stack(slices, axis=0)
