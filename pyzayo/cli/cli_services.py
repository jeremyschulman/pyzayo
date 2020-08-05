"""
This file contains the CLI command for the ZAYO API service inventory feature area.

References
----------
    For the Rich package, colors are defined here:
    https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors

"""

# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import List, Dict

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click
from rich.console import Console
from rich.table import Table, Text

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from pyzayo import ZayoClient
from .cli_root import cli
from pyzayo.consts import InventoryStatusOption

# -----------------------------------------------------------------------------
#
#                               TABLE CODE BEGINS
#
# -----------------------------------------------------------------------------


def colorize_status(status):
    """ colorize the service.status field """
    return Text(
        status,
        style={
            InventoryStatusOption.active: "bright_green",
            InventoryStatusOption.pending_change: "bright_yellow",
        }.get(status),
    )


def make_services_table(services: List[Dict]) -> Table:
    """
    Create a Rich.Table of service inventory records.

    Parameters
    ----------
    services: List[Dict]
        Service inventory records in the form of the API dict.

    Returns
    -------
    The Table ready for console rendering.
    """
    count = len(services)
    title = f"Services ({count})" if count > 1 else "Service"

    table = Table(
        title=Text(title, style="bright_white", justify="left"),
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
    )

    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Product")
    table.add_column("Circuit Id")
    table.add_column("Bandwidth")
    table.add_column("Location A")
    table.add_column("Location Z")

    def make_location(_loc):
        """ create address from location fields """
        return f"{_loc['name']}\n{_loc['city']}, {_loc['state']} {_loc['postalCode']}"

    for rec in services:
        comps = rec["components"][0]

        table.add_row(
            rec["serviceName"],
            colorize_status(rec["status"]),
            f"{rec['productGroup']}\n{rec['productCategory']}",
            comps["circuitId"],
            comps["bandwidth"],
            make_location(comps["locations"][0]),
            make_location(comps["locations"][1]),
        )

    return table


# -----------------------------------------------------------------------------
#
#                               CLI CODE BEGINS
#
# -----------------------------------------------------------------------------


@cli.group("services")
def svc():
    """ Inventory Service commands. """
    pass


@svc.command(name="list")
def cli_svc_inventory_list():
    """
    List service inventory.
    """
    zapi = ZayoClient()
    svc_list = zapi.get_services()
    console = Console()
    console.print(make_services_table(services=svc_list))


@svc.command(name="circuit")
@click.argument("circuit_id")
def cli_svc_by_circuit(circuit_id):
    """
    Show service record for given circuit ID.
    """
    zapi = ZayoClient()
    cir_rec = zapi.get_service_by_circuit_id(circuit_id)

    if not cir_rec:
        print(f"Circuit not found: {circuit_id}")
        return

    console = Console()
    console.print(make_services_table(services=[cir_rec]))
