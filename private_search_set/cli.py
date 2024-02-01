import click
import json
import os
import sys
import pdb
from private_search_set.main import PrivateSearchSet
from flor import BloomFilter

def json_specs(json_file):
    with open(json_file) as file:
        data = convert_hyphen_in_json(json_file)
        pss = PrivateSearchSet(**data)  # Create an instance of the PrivateSearchSet class
    if set(data.keys()) == set(pss.__dict__.keys()):
        click.echo("Fields in JSON file correspond to the private search set class.")
        PrivateSearchSet.print_private_search_set(pss)
        return pss
    else:
        click.echo("Fields in JSON file do not correspond to the private search set class.")
        exit(1)

def convert_hyphen_in_json(json_file):
    """Convert hyphens in JSON file to underscores."""
    with open(json_file) as file:
        data = json.load(file)
        data = {k.replace('-', '_'): v for k, v in data.items()}
        return data

@click.pass_context
def ingest_stdin(ctx):
    pss = ctx.obj
    click.echo("Ingesting stdin to PSS file.")
    # Create the folder if it does not exist
    if not os.path.exists(ctx.params["pss_home"]):
        os.makedirs(ctx.params["pss_home"])
    if pss.bloomfilter['format'] == 'dcso-v1':
        bf = BloomFilter(n=pss.bloomfilter['capacity'], p=pss.bloomfilter['fp-probability'])
        # Read from stdin  
        for line in sys.stdin.buffer.read().splitlines():  
            click.echo(line)
            bf.add(line)
        file_path = os.path.join(ctx.params["pss_home"], 'private-search-set.bloom')
        with open(file_path, 'wb') as f:
            bf.write(f)
    else:
        print("Bloomfilter format not supported.")
        exit(1) 



@click.command()
@click.option('--pss-home', required=True, type=click.Path(exists=False) , help='PSS working folder.')
@click.option('--json-file', required=True, type=click.Path(exists=True), help='Path to the PSS JSON file.')
@click.option('--ingest', required=True, type=click.BOOL , help='ingest stdin to PSS file')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, json_file, pss_home, ingest, debug):
    ctx.obj = json_specs(json_file)
    if ingest:
        ingest_stdin()
    pass

def main():
    cli(obj={})