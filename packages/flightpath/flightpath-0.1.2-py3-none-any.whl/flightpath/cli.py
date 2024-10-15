#!/usr/bin/env python3

from requests.auth import HTTPBasicAuth
import logging
import getpass
import click
import os

from flightpath.airflow import etl_dependencies, etl_task_instances, get_all_dag_ids
from flightpath.common import calculate_critical_path


# Updated CLI commands
@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Extract information from an Airflow instance."""
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    ctx.obj = {}

@cli.command()
@click.option('-u', '--username', type=str, help='Airflow username')
@click.option('-p', '--password', type=str, help='Airflow password')
@click.option('--baseurl', required=True, help='Base URL of the Airflow instance')
@click.option('--task-id', required=True, help='ID of the task')
@click.option('--dag-id', required=False, help='ID of the DAG. If not provided, all DAGs will be extracted.')
@click.option('--dag-run-id', required=True, help='ID of the DAG run')
@click.option('-o', '--output', type=click.Path(), required=True, help='Output DuckDB file path')
@click.option('--clobber', is_flag=True, help='Delete existing output file before generating new one')
@click.option('--stay-within-dag', is_flag=True, help='Only trace the critical path within the dag_id specified',)
@click.pass_context
def trace(ctx: click.Context, username: str, password: str, baseurl: str, task_id: str, dag_id: str, dag_run_id: str, output: str, clobber: bool, stay_within_dag: bool) -> None:
    """Extract all data and trace a critical path."""
    auth = HTTPBasicAuth(username or input("Enter Airflow username: "), 
                         password or getpass.getpass("Enter Airflow password: "))

    if clobber and os.path.exists(output):
        os.remove(output)
        logging.info(f"Deleted existing DuckDB file: {output}")


    if stay_within_dag:
        dag_ids = [dag_id]
    else:
        logging.info("Fetching all dag_ids")
        dag_ids = get_all_dag_ids(baseurl, auth)
    
    etl_dependencies(baseurl, dag_ids, dag_run_id, auth, output)
    etl_task_instances(baseurl, dag_ids, dag_run_id, auth, output)
    logging.info(f"Finished extracting dependencies and task instances for DAG {dag_id} DAG Run: {dag_run_id}")
    
    critical_path = calculate_critical_path(
        task_id=task_id,
        dag_id=dag_id,
        dag_run_id=dag_run_id,
        duckdb_location=output
    )

    [click.echo(o) for o in critical_path]


if __name__ == "__main__":
    cli()

    # Start airflow by changing directory to tests/airflow_example and running `astro dev start`
    # poetry run flightpath --verbose trace -u admin -p admin --baseurl http://localhost:8080 --task-id task_4 --dag-id diamond2 --dag-run-id scheduled__2024-10-12T00:00:00+00:00 --output ~/Downloads/flightpath.db --clobber