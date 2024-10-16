import numpy as np
from cimulate.ecm import CircuitModel


class Resistor(CircuitModel):
    resistance: float

    def __init__(self, resistance: float):
        self.resistance = resistance

    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        return self.resistance


class Capacitor(CircuitModel):
    capacitance: float

    def __init__(self, capacitance: float):
        self.capacitance = capacitance

    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        omega = np.asarray(omega)
        impedance = np.zeros_like(omega, dtype=complex)

        impedance[omega != 0] = 1 / (1j * omega[omega != 0] * self.capacitance)
        impedance[omega == 0] = np.inf

        if len(impedance) == 1:
            return float(impedance[0])

        return impedance


class Inductor(CircuitModel):
    inductance: float

    def __init__(self, inductance: float):
        self.inductance = inductance

    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        return 1j * omega * self.inductance


class Warburg(CircuitModel):
    w: float

    def __init__(self, w: float):
        self.w = w

    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        omega = np.asarray(omega)
        impedance = np.zeros_like(omega, dtype=complex)

        impedance[omega != 0] = self.w / np.sqrt(1j * omega[omega != 0])
        impedance[omega == 0] = np.inf

        if len(impedance) == 1:
            return float(impedance[0])

        return impedance
