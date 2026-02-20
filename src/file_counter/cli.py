"""Command-line interface for file-counter."""

from __future__ import annotations

from pathlib import Path

import click

from file_counter.counter import FileCounter, FileStats


@click.command()
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Directory to count files in",
)
@click.option(
    "--recursive/--no-recursive",
    default=False,
    help="Recursively scan subdirectories (default: False)",
)
@click.option(
    "--hidden",
    is_flag=True,
    default=False,
    help="Include hidden files (starting with .)",
)
def main(directory: Path, recursive: bool, hidden: bool) -> None:
    """File Counter - Count files in a directory, grouped by extension.

    Example:
        file-counter --directory /path/to/dir --recursive --hidden
    """
    try:
        counter = FileCounter(directory, recursive=recursive, include_hidden=hidden)
        stats: FileStats = counter.count()
        _print_stats(stats, directory)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except NotADirectoryError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


def _print_stats(stats: FileStats, directory: Path) -> None:
    """Print file statistics in a formatted way.

    Args:
        stats: File statistics to print
        directory: Directory that was scanned
    """
    click.echo("File Counter Results")
    click.echo("=" * 40)
    click.echo(f"Directory: {directory}")
    click.echo(f"Total files: {stats.total}")
    click.echo()
    click.echo("By extension:")

    # Sort extensions by count (descending) then by name
    sorted_extensions = sorted(stats.by_extension.items(), key=lambda x: (-x[1], x[0]))

    for ext, count in sorted_extensions:
        ext_display = ext if ext else "(none)"
        click.echo(f"  {ext_display}: {count} files")


if __name__ == "__main__":
    main()
