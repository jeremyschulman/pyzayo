import click


@click.group()
def cli():
    pass


@cli.group()
def mtc():
    """
    Maintenance commands
    """
    pass


@mtc.command(name='cases')
def mtc_cases():
    """
    Show maintenance caess.
    """
    print("Show maintenance cases")


def main():
    cli()

