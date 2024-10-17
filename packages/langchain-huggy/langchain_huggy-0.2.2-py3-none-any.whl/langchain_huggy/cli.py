# src/langchain_huggy/cli.py

import click
import uvicorn
from .api import app  # Import the FastAPI app from your api.py file

@click.group()
def cli():
    """Command line interface for langchain_huggy."""
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind the server to.')
@click.option('--port', default=11435, help='Port to bind the server to.')
def server(host, port):
    """Start the langchain_huggy server."""
    click.echo(f"Starting langchain_huggy server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    cli()