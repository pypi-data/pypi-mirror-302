# ![hostasphere](https://avatars.githubusercontent.com/u/164780978?s=30 "logo") hand-e.fr

## Hostasphere - Profiler API

### Description

The Profiling API allows you to measure execution time, memory usage,
and other metrics related to OpenHosta for Python functions.
The collected data is sent to your Hostasphere monitoring interface.

### Installation

Install the required dependencies with pip :

```schell
pip install hostasphere-profiler==v1.0
```

### Usage

To profile a function, use the decorator `@profiler.track()`:

```python
from profiler.core import Profiler

profiler = Profiler(
    address='localhost:50051', # required, is the address of the datasource, default is 'localhost:50051'
    token='hsp_0d6d562910026e3ba0b511dd2c99a47d374f810055003c149eb5fbcdad693319', # required
    refresh_interval=0.1, # optional, double representing the interval in seconds between each refresh of recorded metrics, default is 0.1
    session_tag="dev-1", # optional, string representing the session tag, default is None, esaier to identify the session in the monitoring interface
)

@profiler.track()
def my_func():
    # Function logic
    pass
```

#### Add markers
Yo can add markers to your profiling session to help you identify specific parts of your code.
```python
profiler.get_session().add_annotation('Calculating CPU usage', '#008000')
```
annotation: str
color: str # optional, default is '#000000'

You can find many examples in the [examples](https://github.com/hand-e-fr/hostasphere/tree/main/api/python3/examples) folder.

### In future versions

- Catch exceptions and send them to the monitoring interface
- Add more metrics
- Add the possibility to send custom metrics
- Add the possibility to send logs
- Add the possibility to send traces
