import click

import pdb
from private_search_set.main import PrivateSearchSet

@click.pass_context
def ingest_stdin(ctx):
    pss = ctx.obj
    click.echo("Ingesting stdin to PSS file.")
    pss.ingest_stdin()
    pss.write_to_files(ctx.params["pss_home"])

@click.pass_context
def check_stdin(ctx):
    pss = ctx.obj
    pss.check_stdin()

@click.command()
@click.option('--pss-home', required=True, type=click.Path(exists=False) , help='PSS working folder.')
@click.option('--json-file', required=False, type=click.Path(exists=True), help='Path to the PSS JSON file.')
@click.option('--ingest', required=True, type=click.BOOL , help='ingest stdin to PSS files')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, json_file, pss_home, ingest, debug):
    if json_file and pss_home:
        # TODO maybe allow conversion in the future
        raise ValueError("Please provide either a json-file or a pss-home, not both.")
    # If a json-file with PSS metadata is provided, load the PSS from the JSON file
    if json_file:
        ctx.obj = PrivateSearchSet.load_from_json_specs(json_file)
    # If pss_home is provided, load the PSS from the files in the folder
    if pss_home:
        ctx.obj = PrivateSearchSet.load_from_pss_home(pss_home)
    if ingest:
        ingest_stdin()
    else:
        check_stdin()
    pass

def main():
    cli(obj={})