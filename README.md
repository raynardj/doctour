![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

# doctour

An nasty way to parse python knowledge

### Tutorial

#### Installation
Plese install on [anaconda3](https://www.anaconda.com/distribution/)
```shell
python -m pip install git+https://github.com/raynardj/doctour
```
#### Running
On your terminal, the default port is 8080, Now visit [http://localhost:8080](http://localhost:8080) for web UI
```shell
doctour
```

Or assgin a port 
```shell
doctour --port=8001
```

#### Use DocTour while coding
```python
from torch import nn
import numpy as np
import doctour
```
you can exam class, fuction, module, variable...
```python
doctour.exam(nn.LSTM)
```
This will return a visit address
```
please visit http://localhost:8080/doc/read/LSTM_213748/140265367140768/
```


### Notebooks
* [Experiments](nbs/doc_tour.ipynb)
