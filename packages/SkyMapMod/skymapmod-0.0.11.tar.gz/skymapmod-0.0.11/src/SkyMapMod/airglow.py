import numpy as np
import math
import matplotlib.pyplot as plt

from .airglow_spectrum import wavelenght_kp, intensity_kp
from .modtran_default_kp_transparency import wavelenght_modtran_kp, trancparency_modtran_kp

def airglow_kp_default():
    from .airglow_spectrum import wavelenght_kp, intensity_kp
    from .modtran_default_kp_transparency import wavelenght_modtran_kp, trancparency_modtran_kp
    wavelenght = []
    intensity = []
    for i in range(wavelenght_kp.shape[0]):
        for j in range(wavelenght_modtran_kp.shape[0]):
            if wavelenght_kp[i] == wavelenght_modtran_kp[j]:
                wavelenght.append(wavelenght_kp[i])
                intensity.append(intensity_kp[i] / trancparency_modtran_kp[j])
    return(np.array(wavelenght), np.array(intensity))

def airglow_kp(wavelenght_custom, transparency_custom):
    from .airglow_spectrum import wavelenght_kp, intensity_kp
    wavelenght = []
    intensity = []
    for i in range(wavelenght_kp.shape[0]):
        for j in range(wavelenght_custom.shape[0]):
            if wavelenght_kp[i] == wavelenght_custom[j]:
                wavelenght.append(wavelenght_kp[i])
                intensity.append(intensity_kp[i] / transparency_custom[j])
    return(np.array(wavelenght), np.array(intensity))

def airglow_custom(wavelenght_airglow, intensity_airglow, wavelenght_custom, transparency_custom):
    wavelenght = []
    intensity = []
    for i in range(wavelenght_airglow.shape[0]):
        for j in range(wavelenght_custom.shape[0]):
            if wavelenght_airglow[i] == wavelenght_custom[j]:
                wavelenght.append(wavelenght_airglow[i])
                intensity.append(intensity_airglow[i] / transparency_custom[j])
    return(np.array(wavelenght), np.array(intensity))
