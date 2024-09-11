import cv2
from PIL import Image
import numpy as np
from simulation import is_simulated, get_sim_camera


class Camera():
    def read(self):
        if is_simulated():
            simcameradata = get_sim_camera()
            if simcameradata and len(simcameradata) > 0:
                ar = np.uint8(np.array(simcameradata).reshape((100, 100, 4)))
                ar = cv2.cvtColor(ar, cv2.COLOR_BGRA2RGB)
                return True, ar
            else:
                return False, np.zeros((100, 100, 4))
        else:
            return False, np.zeros((100, 100, 4))
