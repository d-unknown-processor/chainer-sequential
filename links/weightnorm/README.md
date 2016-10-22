# Weight Normalization Layer for Chainer

code for the paper [Weight Normalization: A Simple Reparameterization to Accelerate Training of Deep Neural Networks](https://arxiv.org/abs/1602.07868)

## Requirements

- Chainer 1.17

## Usage
### Installation

```
YOUR PROJECT DIR
├── weightnorm
│   ├── __init__.py
│   ├── convolution_2d.py
│   ├── deconvolution_2d.py
│   └── linear.py
```

### Running

before:
```
from chainer import links as L
layer = L.Linear(...)
```

after:
```
import weightnorm as WN
layer = WN.Linear(...)
```