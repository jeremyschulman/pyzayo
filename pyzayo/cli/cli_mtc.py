# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

import json
from operator import attrgetter

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click
from rich.console import Console
from rich.table import Table, Text
from rich.syntax import Syntax

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from pyzayo import ZayoMtcClient
from .cli_root import cli
from pyzayo import consts
from pyzayo import mtc_models

# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


@cli.group()
def mtc():
    """
    Maintenance commands.
    """
    pass


def colorize_urgency(urgency: str):
    style = {
        consts.CaseUrgency.emergency: "bold red",
        consts.CaseUrgency.demand: "bright_blue",
        consts.CaseUrgency.planned: "bright_yellow",
    }.get(consts.CaseUrgency(urgency))

    return Text(urgency, style=style)


def colorize_impact(impact):
    style = {
        consts.CaseImpact.potential_svc_aff: "",
        consts.CaseImpact.svc_aff: "bold red",
    }.get(consts.CaseImpact(impact))

    return Text("\n".join(impact.split()), style=style)


@mtc.command(name="cases")
def mtc_cases():
    """
    Show listing of maintenance caess.
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

    pdates = attrgetter("primary_date", "primary_date_2", "primary_date_3")

    for rec in recs:
        row_obj = mtc_models.CaseRecord.parse_obj(rec)
        row_obj.urgency = colorize_urgency(row_obj.urgency)
        row_obj.impact = colorize_impact(row_obj.impact)
        table.add_row(
            row_obj.case_num,
            row_obj.urgency,
            row_obj.status,
            row_obj.impact,
            "\n".join(str(pd) for pd in pdates(row_obj) if pd),
            row_obj.location,
            str(row_obj.from_time),
            str(row_obj.to_time),
            row_obj.reason,
        )

    console.print(table)


@mtc.command(name="case-details")
@click.argument("case_number")
def mtc_case_details(case_number):
    """
    Show specific case details.
    """
    zapi = ZayoMtcClient()
    case = zapi.get_case(by_case_num=case_number)

    console = Console()

    if not case:
        console.print(f"Case [bold white]{case_number}: [bold red]Not found")
        return

    console.print(f"Case [bold white]{case_number}[/bold white]: [bold green]Found")
    console.print(Syntax(code=json.dumps(case, indent=3), lexer_name="json"))
