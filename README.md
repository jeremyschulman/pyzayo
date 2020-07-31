# Python client for Zayo API

This package provides a python 3.8 asyncio based client to access the Zayo
API system.  

This package also includes a CLI tool `zayocli` that can be used to access and
display the Zayo Maintenance API features.

# Installation

```bash
pip install pyzayo
```

# Before You Begin

You must export two environment variables for use with this library:

  * `ZAYO_CLIENT_ID` - Your unique client ID value
  * `ZAYO_CLIENT_SECRET` - Your unique client secret value

You must obtain these values from Zayo.

# Quick Start

```python
from pyzayo import ZayoMtcClient

# create a client to the Maintenace API authenticate using the ZAYO_ variables
zmtc = ZayoMtcClient()

# use the instance methods to retrieve data
cases = zmtc.get_cases()
```

# Documentation

For now the ZayoMtClient docstrings.  More docs coming soon.
