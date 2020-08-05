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
zapi = ZayoClient()

# use the instance methods to retrieve data
cases = zapi.get_cases()
```

# Usage Documentation
**WORK IN PROGRESS**

For now, please use the docstrings by doing:
```python
from pyzayo import ZayoClient

help(ZayoClient)
```

# CLI Tool

The `zayocli` tool supports the maintenance cases and service inventory features:

```shell
Usage: zayocli [OPTIONS] COMMAND [ARGS]...

  Zayo CLI tool to access information via the API.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  cases     Maintenance commands.
  services  Inventory Service commands.
```

**cases subcommand**

```bash
Usage: zayocli cases [OPTIONS] COMMAND [ARGS]...

  Maintenance commands.

Options:
  --help  Show this message and exit.

Commands:
  list          Show listing of maintenance caess.
  show-details  Show specific case details.
```

**services subcommand**
```shell
Usage: zayocli services [OPTIONS] COMMAND [ARGS]...

  Inventory Service commands.

Options:
  --help  Show this message and exit.

Commands:
  circuit  Show service record for given circuit ID.
  list     List service inventory.
```

# Zayo API Documentation
   * [Serivce Inventory](http://54.149.224.75/wp-content/uploads/2020/02/Service-Inventory-Wiki.pdf)
   * [Maintenance](http://54.149.224.75/wp-content/uploads/2020/03/Maintenance-Cases-Wiki.pdf)

