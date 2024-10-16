# `cimulate`

The `cimulate` package provides a framework for modeling electrical components 
and calculating their impedance. Components can be combined in series and 
parallel, with easy access to impedance calculations over a range of 
frequencies.

## Example

```python
from cimulate import Resistor, Capacitor, Inductor
import numpy as np

# Create components
r = Resistor(100)  # 100 Ohms
c = Capacitor(1e-6)  # 1 µF
l = Inductor(1e-3)  # 1 mH

# Combine components in series (+) and parallel (/)
circuit = r + c / l

# You can calculate the impedance (remember to use angular frequency)
frequency = np.linspace(0.001, 1000, 1000)  # 1 mHz to 1 kHz
omega = 2 * np.pi * frequency
impedance = circuit.impedance(omega)

# You can even simulate voltages with a driving current
time = np.linspace(0, 60, 1000)
current = time / 6
voltage = circuit.voltage(current)
```

## Roadmap

- [x] Automatic fitting of all circuit parameters
- [x] Voltage simulation given a driving current, and vice versa
- [ ] More circuit elements
