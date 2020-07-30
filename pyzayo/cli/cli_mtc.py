# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from operator import itemgetter

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from rich.console import Console
from rich.table import Column, Table, Text

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from pyzayo import ZayoMtcClient
from .cli_root import cli
from pyzayo import consts


@cli.group()
def mtc():
    """
    Maintenance commands
    """
    pass


def colorize_urgency(urgency: str):
    style = {
        consts.CaseUrgency.emergency: "bold red",
        consts.CaseUrgency.demand: "bright_blue",
        consts.CaseUrgency.planned: "bright_yellow"
    }.get(consts.CaseUrgency(urgency))

    return Text(urgency, style=style)


def colorize_impact(impact):
    style = {
        consts.CaseImpact.potential_svc_aff: "",
        consts.CaseImpact.svc_aff: "bold red",
    }.get(consts.CaseImpact(impact))

    return Text('\n'.join(impact.split()), style=style)


@mtc.command(name='cases')
def mtc_cases():
    """
    Show maintenance caess.
    """
    zapi = ZayoMtcClient()
    recs = zapi.get_cases()

    console = Console()

    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Case #")
    table.add_column("Urgency")
    table.add_column("Status")
    table.add_column("Impact")
    table.add_column("Primary Date")
    table.add_column("Location", width=12, overflow="fold")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Reason")

    row_maker = itemgetter('caseNumber', 'urgency', 'status', 'levelOfImpact',
                           'primaryDate', 'location', 'fromTime', 'toTime',
                           "reasonForMaintenance")
    for rec in recs:
        row_data = list(row_maker(rec))
        row_data[1] = colorize_urgency(row_data[1])
        row_data[3] = colorize_impact(row_data[3])
        table.add_row(*row_data)

    console.print(table)

