# Python client for Zayo API

This package provides a python 3.8 asyncio based client to access the Zayo
API system.

The following API functional areas are supported:
   * Service Inventory
   * Maintenance

This package also includes a CLI tool `zayocli` to retrieve and display information
obtained via the API.

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
from pyzayo import ZayoClient

# create a client to the Maintenace API authenticate using the ZAYO_ variables
zmtc = ZayoClient()

# use the instance methods to retrieve data
cases = zmtc.get_cases()
```

# Usage Documentation:

**WORK IN PROGRESS** 

For now, please use the docstrings by doing:
```python
from pyzayo import ZayoClient

help(ZayoClient)
```

# Zayo API Documentation
   * [Serivce Inventory](http://54.149.224.75/wp-content/uploads/2020/02/Service-Inventory-Wiki.pdf) 
   * [Maintenance](http://54.149.224.75/wp-content/uploads/2020/03/Maintenance-Cases-Wiki.pdf) 

