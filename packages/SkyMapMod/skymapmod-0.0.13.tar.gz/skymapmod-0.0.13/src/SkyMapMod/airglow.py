import numpy as np
import math
import matplotlib.pyplot as plt

from .airglow_spectrum import wavelenght_kp, intensity_kp
from .modtran_default_kp_transparency import wavelenght_modtran_kp, trancparency_modtran_kp

def airglow_custom(wavelenght_airglow = wavelenght_kp, intensity_airglow = intensity_kp, wavelenght_atmosphere = wavelenght_modtran_kp, transparency_atmosphere = trancparency_modtran_kp):
    wavelenght = []
    intensity = []
    for i in range(wavelenght_airglow.shape[0]):
        for j in range(wavelenght_atmosphere.shape[0]):
            if wavelenght_airglow[i] == wavelenght_atmosphere[j]:
                wavelenght.append(wavelenght_airglow[i])
                intensity.append(intensity_airglow[i] / transparency_atmosphere[j])
    return(np.array(wavelenght), np.array(intensity))
