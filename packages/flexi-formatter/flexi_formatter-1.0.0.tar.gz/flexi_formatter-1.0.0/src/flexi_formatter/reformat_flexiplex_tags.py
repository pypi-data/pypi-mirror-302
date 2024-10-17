import re
import sys
import typer
import simplesam
from flexi_formatter import __version__ 

app = typer.Typer()

@app.command()
def main(infile: str):
    with simplesam.Reader(open(infile)) as in_bam:
        with simplesam.Writer(sys.stdout, in_bam.header) as out_sam:
            for read in in_bam:
                # Get header name and split by "_#"
                bc_umi = read.qname.split("#")[0]
                bc = bc_umi.split("_")[0]
                read.tags['CB'] = bc

                if len(bc_umi.split("_")) > 1:
                    umi = bc_umi.split("_")[1]
                    read.tags['UR'] = umi

                # Write new reads
                out_sam.write(read)

@app.callback()
def callback():
    """
    A simple tool for processing BAM/SAM files.
    """
    pass

@app.command()
def version():
    """Prints the version of the tool."""
    typer.echo(f"flexi_formatter version: {__version__}")

if __name__ == "__main__":
    app()