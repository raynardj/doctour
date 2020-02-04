![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
# Doc Tour
> An nasty way to parse python knowledge


### Tutorial

#### Installation
Plese install on [anaconda3](https://www.anaconda.com/distribution/)
```shell
python -m pip install doc_tour
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

## Exam variable during your coding

eg. while you're doing nlp and using lstm, you wonder what the code in pytorch is, what's its inheritance structure, which of the functions was defined in the lstm code, which other functions are inherited from its ancestors

```python
from torch import nn
import numpy as np
import doctour
```

you can exam class, fuction, module, variable...

```python
doctour.exam(nn.LSTM)
```

    please visit http://localhost:8080/doc/read/LSTM_173834/140681093056304/





    <DocTour:LSTM_173834>


