"""CLI for regscale-dev commands."""

import contextlib
import os
import sys

import click
from rich.console import Console


@click.group()
def cli() -> click.Group:
    """RegScale-Dev CLI."""
    pass


@cli.command()
@click.option("--iterations", default=100, help="The number of times to run the function")
def profile(iterations: int) -> None:
    """Profile the CLI."""
    from regscale.dev.profiling import profile_about_command, profile_my_function

    profile_my_function(profile_about_command, iterations=iterations)
    console = Console()
    console.print(
        "Profiling complete, you can view the file in [yellow]profile_stats.csv[reset] or [yellow]profile_stats.pstat[reset]"
    )


@cli.command()
@click.option("--iterations", default=100, help="The number of times to run the function")
@click.option("--no-output", is_flag=True, help="Output in dictionary form")
def calculate_start_time(iterations: int, no_output: bool) -> None:
    """Calculate the start time for the CLI."""
    from regscale.dev.profiling import calculate_load_times

    calculate_load_times(iterations=iterations, no_output=no_output)


@cli.command()
@click.option("--raw", is_flag=True, help="Output raw results")
def calculate_import_time(raw: bool) -> None:
    """Calculate the import time for the CLI."""
    from regscale.dev.profiling import calculate_cli_import_time

    load_time = calculate_cli_import_time()
    if raw:
        print(load_time)
    else:
        console = Console()
        console.print(f"It took {load_time:.6f} seconds to import the CLI.")


@cli.command()
@click.option("--csv", is_flag=True, help="Output raw results to `analysis.csv`")
def analyze(csv: bool) -> None:
    """Analyze the CLI codebase and generate an optional PDF report or a CSV as well as raw JSON.
    This command must be run from the root of the git repository.
    The code metrics generated include git commits, Halstead Metrics, and Cyclomatic Complexity in addition to
    a variety of other metrics useful for analyzing the codebase.
    """
    if not os.path.exists(".git"):
        print("This command must be run from the root of the repository.")
        sys.exit(1)
    import gc
    import json
    from collections import OrderedDict, defaultdict

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from rich.console import Console
    from rich.progress import track

    from regscale.dev.analysis import analyze_code_files, analyze_git, generate_barplot, generate_heatmap
    from regscale.utils.numbers import is_number

    console = Console()
    console.print("[yellow]Analyzing RegScale-CLI...")
    git_metrics = analyze_git()
    code_metrics = analyze_code_files()
    raw_data = {
        key: {**git_metrics.get(key, {}), **code_metrics.get(key, {})} for key in set(git_metrics) | set(code_metrics)
    }
    data = OrderedDict(sorted(raw_data.items()))
    # Sample data for one file to identify numeric metrics
    sample_data = next(iter(data.values()), {})
    json.dump(data, open("analysis.json", "w"))
    if csv:
        import pandas as pd  # Optimize import performance

        df = pd.DataFrame(data)
        df = df.transpose()
        df.to_csv("analysis.csv")
        console.print("[green]Done! You can view the raw analysis in analysis.csv or in analysis.json.")
        sys.exit(0)
    metrics_to_track = list(filter(lambda key: is_number(sample_data.get(key)), sample_data.keys()))
    # Aggregate metrics by directory with progress tracking
    aggregated_data = defaultdict(lambda: defaultdict(float))
    for file, metrics in track(data.items(), description="[cyan]Aggregating metrics..."):
        directory = "/".join(file.split("/")[:-1])
        for metric, value in metrics.items():
            if metric in metrics_to_track:
                aggregated_data[directory][metric] += value
    with PdfPages("Metrics Report.pdf") as pdf:
        for metric in track(metrics_to_track, description="[cyan]Generating heatmaps..."):
            plot = generate_heatmap(data, metric)
            plt.tight_layout()
            pdf.savefig(figure=plot, dpi=300)
            plt.close(plot)
            gc.collect()
        for metric in track(metrics_to_track, description="[cyan]Generating barplots..."):
            plot = generate_barplot(data, metric)
            plt.tight_layout()
            pdf.savefig(figure=plot, dpi=300)
            plt.close(plot)
            gc.collect()
        console.print("[yellow]Generating aggregated metrics graphics...")
        plt.figure(figsize=(50, 50))
        plt.axis("tight")
        plt.axis("off")
        selected_metrics = [
            "commit_count",
            "Halstead Volume",
            "Cyclomatic Complexity",
            "Halstead Effort",
        ]
        table_data: list = []  # initialize an empty list to collect table_data
        for file, val in track(data.items(), description="[cyan]Generating table..."):
            row = [file, *[val.get(metric, "N/A") for metric in selected_metrics]]
            table_data.append(row)
        plt.table(
            cellText=table_data,
            colLabels=["File"] + selected_metrics,
            cellLoc="center",
            loc="center",
        )
        pdf.savefig()
        gc.collect()
        console.print("[yellow]Generating aggregated metrics graphics...")
        for metric in track(metrics_to_track, description="[cyan]Generating aggregated heatmaps..."):
            heatmap_plot = generate_heatmap(aggregated_data, metric, figsize=(20, 20), font_size=10)
            plt.tight_layout()
            pdf.savefig(figure=heatmap_plot, dpi=150)
            plt.close(heatmap_plot)
            gc.collect()
        console.print("[red]Writing PDF to file, this may take some time . . . ")
    console.print("[green]Done! You can view the raw analysis in analysis.json and the report in Metrics Report.pdf.")


@cli.command()
@click.option("--hide_source", is_flag=True, help="Hide the source code link in the generated documentation")
def make_docs(hide_source: bool) -> None:
    """Generate documentation for the CLI."""
    from regscale.dev.docs import generate_docs

    generate_docs(hide_source=hide_source)


with contextlib.suppress(ImportError, SystemExit):
    from regscale.airflow.azure.cli import cli as azure_cli

    cli.add_command(azure_cli)


if __name__ == "__main__":
    cli()
