import click
from xtract.core import process_codebase, generate_embeddings, query_codebase


@click.group()
def cli():
    """CLI for querying codebase using embeddings."""
    pass


@cli.command()
@click.argument('codebase_path')
def process(codebase_path):
    """
    Load and process the codebase into chunks.
    """
    num_chunks = process_codebase(codebase_path)
    click.echo(f"Codebase processed: {num_chunks} chunks found.")


@cli.command()
@click.option("--model_name", default="microsoft/codebert-base", help="Name of the embedding model to use.")
def generate(model_name):
    """
    Generate embeddings for the codebase.
    """
    num_embeddings = generate_embeddings(model_name)
    click.echo(f"Embeddings generated: {num_embeddings} embeddings saved.")


@cli.command()
@click.argument("query")
@click.option("--count", "-c", default=5, help="Number of top results to return.")
def query(query, count):
    """
    Query the codebase for relevant code snippets.
    """
    results = query_codebase(query, count)
    click.echo(f"Top {count} results:")
    for i, snippet in enumerate(results):
        click.echo(f"\nResult {i+1}:\n{snippet}\n")


if __name__ == "__main__":
    cli()
