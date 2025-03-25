#Build Automation Interfaces
import click
from datetime import datetime
from ai_processor import AIProcessor
import os
from dotenv import load_dotenv
# At the top with other imports
from openai import OpenAI


# Load environment variables
load_dotenv()


@click.group()
def cli():
    """DevOps Incident Response CLI"""
    pass

@cli.command()
@click.argument('error_message')
def resolve(error_message):
    """Get resolution for an error"""
    processor = AIProcessor()
    solution = processor.generate_solution(error_message)
    click.echo(f"\n=== INCIDENT RESOLUTION ===\n{solution}\n")

@cli.command()
@click.argument('error_message')
@click.argument('root_cause')
@click.argument('solution_steps', nargs=-1)
def add_incident(error_message, root_cause, solution_steps):
    """Add a new incident to the database"""
    processor = AIProcessor()
    processor.db.store_incident(error_message, root_cause, list(solution_steps))
    processor._initialize_vector_index()  # Refresh index
    click.echo("Incident added successfully!")

if __name__ == '__main__':
    cli()