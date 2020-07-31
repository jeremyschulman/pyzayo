"""

References
----------
    Colors:
    https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors
"""
# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from operator import attrgetter

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click
from rich.console import Console
from rich.table import Table, Text
import maya

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from pyzayo import ZayoMtcClient
from .cli_root import cli
from pyzayo import consts
from pyzayo.mtc_models import CaseRecord, ImpactRecord, NotificationDetailRecord
from pyzayo.consts import CaseStatusOptions

# -----------------------------------------------------------------------------
#
#                               TABLE CODE BEGINS
#
# -----------------------------------------------------------------------------


def colorize_urgency(urgency: str):
    style = {
        consts.CaseUrgencyOptions.emergency: "bold red",
        consts.CaseUrgencyOptions.demand: "bright_blue",
        consts.CaseUrgencyOptions.planned: "bright_yellow",
    }.get(
        consts.CaseUrgencyOptions(urgency)  # noqa
    )  # noqa

    return Text(urgency, style=style)


def colorize_status(status):
    return Text(
        status,
        style={CaseStatusOptions.scheduled: "bright_yellow"}.get(
            consts.CaseStatusOptions(status)  # noqa
        ),
    )


def colorize_impact(impact):
    style = {
        consts.CaseImpactOptions.potential_svc_aff: "",
        consts.CaseImpactOptions.svc_aff: "bold red",
    }.get(
        consts.CaseImpactOptions(impact)  # noqa
    )  # noqa

    return Text("\n".join(impact.split()), style=style)


def make_cases_table(recs):
    n_cases = len(recs)
    title = f"Cases ({n_cases})" if n_cases > 1 else "Case"
    table = Table(
        title=title,
        title_style="bright_white",
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
    )

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

    for row_obj in recs:

        if row_obj.status != consts.CaseStatusOptions.closed:
            row_obj.urgency = colorize_urgency(row_obj.urgency)  # noqa
            row_obj.impact = colorize_impact(row_obj.impact)
            row_obj.status = colorize_status(row_obj.status)

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

    return table


def make_impacts_table(impacts):
    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
        title=f"Impacts ({len(impacts)})",
        title_style="bright_white",
    )

    table.add_column("Case #")
    table.add_column("Circuit Id")
    table.add_column("Expected Impact")
    table.add_column("CLLI A")
    table.add_column("CLLI Z")

    for rec in impacts:
        row_obj = ImpactRecord.parse_obj(rec)

        table.add_row(
            row_obj.case_num,
            row_obj.circuit_id,
            row_obj.impact,
            row_obj.clli_a,
            row_obj.clli_z,
        )

    return table


def make_notifs_table(notifs):

    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
        title=f"Notifications ({len(notifs)})",
        title_style="bright_white",
    )

    table.add_column("Id")
    table.add_column("Type")
    table.add_column("Email Sent")
    table.add_column("Email Subject")
    table.add_column("Email To")

    for rec in notifs:
        row_obj = NotificationDetailRecord.parse_obj(rec)
        email_list = sorted(map(str.strip, row_obj.email_list.split(";")))
        mt = maya.parse(row_obj.date)
        dstring = (
            mt.local_datetime().strftime("%Y-%m-%d\n%H:%M:%S")
            + f"\n({mt.slang_time()})"
        )

        table.add_row(
            row_obj.name, row_obj.type, dstring, row_obj.subject, "\n".join(email_list)
        )

    return table


# -----------------------------------------------------------------------------
#
#                               CLI CODE BEGINS
#
# -----------------------------------------------------------------------------


@cli.group()
def mtc():
    """
    Maintenance commands.
    """
    pass


@mtc.command(name="cases")
def mtc_cases():
    """
    Show listing of maintenance caess.
    """
    zapi = ZayoMtcClient()
    recs = [
        rec
        for rec in map(CaseRecord.parse_obj, zapi.get_cases())
        if rec.status != CaseStatusOptions.closed
    ]
    console = Console()
    console.print(make_cases_table(recs))


@mtc.command(name="case-details")
@click.argument("case_number")
def mtc_case_details(case_number):
    """
    Show specific case details.
    """
    zapi = ZayoMtcClient()

    # find the case by number

    case, impacts, notifs = zapi.get_case_details(by_case_num=case_number)

    console = Console()

    if not case:
        console.print(f"Case [bold white]{case_number}: [bold red]Not found")
        return

    # TODO raw dumping data for now ... need to make pretty.

    console.print(f"Case [bold white]{case_number}[/bold white]: [bold green]Found")
    console.print(make_cases_table([case]))
    console.print(make_impacts_table(impacts))
    console.print(make_notifs_table(notifs))

    # console.print(Syntax(code=json.dumps(case, indent=3), lexer_name="json"))
