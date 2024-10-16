from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Iterable, List, Union

import numpy as np
from scipy.optimize import minimize


class CircuitModel(ABC):
    """
    Base class representing any circuit model.

    This circuit model and all its methods are assumed to be linear
    time-invariant.
    """

    @abstractmethod
    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        """
        Find the impedance of the system, given an angular frequency.

        Args:
            omega: Float or array representing the angular frequency, in rad/s

        Returns:
            Corresponding impedance for the input angular frequency/frequencies
        """
        raise NotImplementedError

    def voltage(self, current: np.ndarray, sample_rate: float) -> np.ndarray:
        """
        Calculate the voltage of the circuit given a current signal

        Args:
            current: Array representing the current signal
            sample_rate: Sampling rate of the signal, in Hz

        Returns:
            Array representing the resulting voltage of the circuit
        """

        current_fft = np.fft.fft(current)
        # TODO: Allow non-uniform time array input (non-uniform FFT)
        freqs = np.fft.fftfreq(len(current), d=1 / sample_rate)
        omega = 2 * np.pi * freqs
        impedance = self.impedance(omega)
        voltage_fft = current_fft * impedance
        voltage = np.fft.ifft(voltage_fft).real

        return voltage

    def current(self, voltage: np.ndarray, sampling_rate: float) -> np.ndarray:
        """
        Calculate the current of the circuit given a voltage signal

        Args:
            voltage: Array representing the voltage signal
            sample_rate: Sampling rate of the signal, in Hz

        Returns:
            Array representing the resulting current of the circuit
        """
        voltage_fft = np.fft.fft(voltage)
        # TODO: Allow non-uniform time array input (non-uniform FFT)
        freqs = np.fft.fftfreq(len(voltage), d=1 / sampling_rate)
        omega = 2 * np.pi * freqs
        impedance = self.impedance(omega)
        current_fft = voltage_fft / impedance
        current = np.fft.ifft(current_fft).real

        return current

    def dc_resistance(self) -> float:
        """
        Returns the total DC resistance of the circuit
        """
        return float(self.impedance(0).real)

    def dc_power_from_current(self, current: float | np.ndarray) -> float | np.ndarray:
        return current**2 * self.dc_resistance()

    def dc_power_from_voltage(self, voltage: float | np.ndarray) -> float | np.ndarray:
        return voltage**2 / self.dc_resistance()

    def get_parameters(self) -> List[Union[float, int]]:
        return [v for v in self.__dict__.values() if isinstance(v, (float, int))]

    def set_parameters(self, params: List[Union[float, int]]):
        keys = [k for k, v in self.__dict__.items() if isinstance(v, (float, int))]
        for key, value in zip(keys, params):
            setattr(self, key, value)

    def fit_impedance(self, omega: np.ndarray, z_true: np.ndarray):
        """
        Automatically fits the circuit parameters to measured impedance values.

        Sets the circuit parameters to the minimized ones when the minimization
        is performed.

        Args:
            omega: The measured angular frequencies, in rad/s
            z_true: The measured impedances, in Ohm
        """
        initial_params = self.get_parameters()

        def objective(params):
            cpy = deepcopy(self)
            cpy.set_parameters(params)
            z_pred = cpy(omega)
            return np.mean(np.abs((z_true - z_pred) / z_true))

        result = minimize(objective, initial_params, method="Nelder-Mead")
        self.set_parameters(result.x)

    def __add__(self, other):
        return Series(self, other)

    def __truediv__(self, other):
        return Parallel(self, other)


class Series(CircuitModel):
    first: CircuitModel
    second: CircuitModel

    def __init__(self, first: CircuitModel, second: CircuitModel):
        self.first = first
        self.second = second

    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        return self.first.impedance(omega) + self.second.impedance(omega)

    def get_parameters(self):
        return self.first.get_parameters() + self.second.get_parameters()

    def set_parameters(self, params):
        n = len(self.first.get_parameters())
        self.first.set_parameters(params[:n])
        self.second.set_parameters(params[n:])


class Parallel(CircuitModel):
    first: CircuitModel
    second: CircuitModel

    def __init__(self, first: CircuitModel, second: CircuitModel):
        self.first = first
        self.second = second

    def impedance(self, omega: float | np.ndarray) -> complex | np.ndarray:
        first = self.first.impedance(omega)
        second = self.second.impedance(omega)

        if not isinstance(first, Iterable):
            first = [first]
        if not isinstance(second, Iterable):
            second = [second]

        total = np.zeros_like(omega, dtype=complex)
        for i, (f, s) in enumerate(zip(first, second)):
            if f == 0 or s == 0:
                total[i] = 0
            else:
                total[i] = 1 / (1 / f + 1 / s)

        if len(total) == 1:
            return float(total[0])

        return total

    def get_parameters(self):
        return self.first.get_parameters() + self.second.get_parameters()

    def set_parameters(self, params):
        n = len(self.first.get_parameters())
        self.first.set_parameters(params[:n])
        self.second.set_parameters(params[n:])
