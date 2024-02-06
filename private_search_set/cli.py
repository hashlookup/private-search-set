import click

import pdb
from private_search_set.main import PrivateSearchSet

@click.pass_context
def ingest_stdin(ctx):
    pss = ctx.obj
    click.echo("Ingesting stdin to PSS file.")
    pss.ingest_stdin(ctx.params["debug"])
    pss.write_to_files(ctx.params["pss_home"])

@click.pass_context
def check_stdin(ctx):
    pss = ctx.obj
    pss.check_stdin(ctx.params["debug"])

@click.command()
@click.option('--pss-home', required=True, type=click.Path(exists=False) , help='PSS working folder.')
@click.option('--json-file', required=False, type=click.Path(exists=True), help='Path to the PSS JSON file.')
@click.option('--ingest/--check', required=True, type=click.BOOL , help='ingest or check stdin into/against PSS files')
@click.option('--key', required=False, type=click.STRING , help='specify key content for HMAC operations')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, json_file, pss_home, ingest, key, debug):
    # If a json-file with PSS metadata is provided, load the PSS from the JSON file
    # set the key if provided
    if json_file:
        try:
            ctx.obj = PrivateSearchSet.load_from_json_specs(json_file, key, debug)
        except ValueError as e:
            click.echo(e)
            exit(1)
    # If pss_home is provided, load the PSS from the files in the folder
    # set the key if provided
    elif pss_home:
        try:
            ctx.obj = PrivateSearchSet.load_from_pss_home(pss_home, key, debug)
        except ValueError as e:
            click.echo(e)
            exit(1)
    if ingest:
        try:
            ingest_stdin()
        except ValueError as e:
            click.echo(e)
            exit(1)
    else:
        try:
            check_stdin()
        except ValueError as e:
            click.echo(e)
            exit(1)
    pass

def main():
    cli(obj={})