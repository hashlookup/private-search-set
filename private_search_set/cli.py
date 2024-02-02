import click
from private_search_set.main import PrivateSearchSet

@click.pass_context
def ingest_stdin(ctx):
    pss = ctx.obj
    click.echo("Ingesting stdin to PSS file.")
    pss.ingest_stdin()
    pss.write_to_files(ctx.params["pss_home"])


@click.command()
@click.option('--pss-home', required=True, type=click.Path(exists=False) , help='PSS working folder.')
@click.option('--json-file', required=True, type=click.Path(exists=True), help='Path to the PSS JSON file.')
@click.option('--ingest', required=True, type=click.BOOL , help='ingest stdin to PSS file')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, json_file, pss_home, ingest, debug):
    ctx.obj = PrivateSearchSet.load_from_json_specs(json_file)
    if ingest:
        ingest_stdin()
    pass

def main():
    cli(obj={})