import cv2
from PIL import Image
import numpy as np
from simulation import is_simulated


class Camera():
    sim_data = None
    def set_sim_data(self, data):
        self.sim_data = data

    def read(self):
        if is_simulated() and self.sim_data is not None and len(self.sim_data) > 0:
            ar = np.array(self.sim_data).reshape((100, 100, 4))
            image = Image.fromarray(ar, "RGB")
            # image.show()
            return True, image
        else:
            return False, np.array([])
