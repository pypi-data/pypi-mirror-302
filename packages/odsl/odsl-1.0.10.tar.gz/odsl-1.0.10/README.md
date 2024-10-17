# ODSL Python SDK

The python SDK for the [OpenDataDSL](https://opendatadsl.com) data management platform

## Installation
You can install the ODSL Python SDK from [PyPI](https://pypi.org/project/odsl/):

    python -m pip install odsl

## About
This python SDK for OpenDataDSL has the following features:

* Find any data in OpenDataDSL using the ```list``` command
* Retrieve any data using the ```get``` command
* Update any data (if you have permission) using the ```update``` command

Check out our [demo repository](https://github.com/OpenDataDSL/odsl-python-sdk-demo) for examples of real-world usage.

## Usage

### Logging in and getting started

```python
from odsl import sdk

odsl = sdk.ODSL()
odsl.login()
```

### Logging in using a secret
```python
from odsl import sdk

odsl = sdk.ODSL()
odsl.loginWithSecret(tenantId, clientId, secret)
```

### Finding master data

```python
objects = odsl.list('object', source='public', params={'source':'ECB'})
print(objects[0])
```

### Getting master data

```python
obj = odsl.get('object', 'public', '#ECB')
print(obj['description'])
```

### Getting a timeseries
```python
ts = odsl.get('data', 'public', '#ABN_FX.EURUSD:SPOT', {'_range':'from(2024-07-01)'})
print(ts)
```

### Getting a forward curve
```python
id = '#AEMO.EL.AU.NEM.NSW1.FORECAST:DEMAND:2024-07-15'
curve = odsl.get('data', 'public', id)
for c in curve['contracts']:
	print(c['tenor'] + " - " + str(c['value']))
```

### Updating some private master data
```python
var = {
    '_id': 'AAA.PYTHON',
    'name': 'Python Example'
}
odsl.update('object', 'private', var)
```

### Reading and updating some private master data
```python
po = odsl.get('object', 'private', 'AAA.PYTHON')
po['description'] = 'Updated from Python'
odsl.update('object', 'private', po)
```
