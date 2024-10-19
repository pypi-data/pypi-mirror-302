import contextlib
import io
from itertools import repeat
import logging
import time
from pathlib import Path
from typing import Any, Dict, TypeVar

import click
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown as RichMarkdown
from rich.text import Text

logger = logging.getLogger(__name__)


class MarkdownStream:
    live = None
    when = 0
    min_delay = 0.050
    live_window = 6

    def __init__(self, mdargs=None):
        self.printed = []

        if mdargs:
            self.mdargs = mdargs
        else:
            self.mdargs = {}

        self.live = Live(Text(""), refresh_per_second=1.0 / self.min_delay)
        self.live.start()

    def __del__(self):
        if self.live:
            with contextlib.suppress(Exception):
                self.live.stop()

    def update(self, text, final=False) -> None:
        now = time.time()
        if not final and now - self.when < self.min_delay:
            return
        self.when = now

        string_io = io.StringIO()
        console = Console(file=string_io, force_terminal=True)

        markdown = RichMarkdown(text, **self.mdargs)

        console.print(markdown)
        output = string_io.getvalue()

        lines = output.splitlines(keepends=True)
        num_lines = len(lines)

        if not final:
            num_lines -= self.live_window

        if final or num_lines > 0:
            num_printed = len(self.printed)

            show = num_lines - num_printed

            if show <= 0:
                return

            show = lines[num_printed:num_lines]
            show = "".join(show)
            show = Text.from_ansi(show)
            self.live.console.print(show)

            self.printed = lines[:num_lines]

        if final:
            self.live.update(Text(""))
            self.live.stop()
            self.live = None
        else:
            rest = lines[num_lines:]
            rest = "".join(rest)
            # rest = '...\n' + rest
            rest = Text.from_ansi(rest)
            self.live.update(rest)


class Markdown:
    """Stream formatted JSON-like text to the terminal with live updates."""

    def __init__(self, data=None, mdargs=None, style="default", save=None, min_delay=0.05, live_window=6):
        logger.debug(f"Initializing MarkdownStreamer with data: {data}")
        self.data = data or {}
        self.mdargs = mdargs or {}
        self.style = style
        self.console = Console(style=self.style, force_terminal=True)
        self.save = save
        self.min_delay = min_delay
        self.live_window = live_window
        self.last_update_time = time.time()
        self.printed_lines = []

    def generate_markdown(self, data=None, depth=0):
        """Generate Markdown from JSON with headers based on depth."""
        markdown_lines = []
        indent = "  " * depth

        if isinstance(data, dict):
            for key, value in data.items():
                if key == "name":
                    markdown_lines.append(f"\n{indent}{'#' * max(1, depth)} {value}\n")
                elif isinstance(value, dict | list):
                    markdown_lines.append(f"\n{indent}- **{key}**:\n")
                    markdown_lines.extend(self.generate_markdown(value, depth + 1))
                else:
                    markdown_lines.append(f"{indent}- **{key}**: {value}")
        elif isinstance(data, list):
            for item in data:
                markdown_lines.extend(self.generate_markdown(item, depth))
        else:
            markdown_lines.append(f"{indent}{data}")
        return markdown_lines   

    def stream(self, speed_factor=10000):
        """Stream the markdown content dynamically based on its length."""
        markdown_content = "\n".join(self.generate_markdown(self.data))
        content_length = len(markdown_content)
        if content_length == 0:
            logger.error("No content to stream.")
            return
        speed = max(0.01, min(0.1, speed_factor / content_length))  # Adjust speed dynamically
        speed /= 2
        refresh_speed = 1 / 20
        rendered = ""

        pm = MarkdownStream()

        for i in range(6, len(markdown_content)):
            pm.update(markdown_content[:i], final=False)
            time.sleep(speed * refresh_speed)

        pm.update(markdown_content, final=True)

def recursive_read(file, include=None, depth=0, max_depth=5):
    """Recursively read files or directories and return their content as a dictionary."""
    if depth > max_depth and max_depth > 0:
        return {}
    include = include or {".json", ".md", ".txt", ".yaml", ".toml", ".py"}
    data = {}
    file_path = Path(file).resolve()
    print(f"Reading path: {file_path}")
    if file_path.is_file() and file_path.suffix in include and "__pycache__" not in str(file_path) and ".pyc" not in str(file_path):
        print(f"Reading file: {file_path}")
        logger.info(f"Reading file: {file_path}")
        content = file_path.read_text()
        if file_path.suffix == ".py":
            data[str(file_path)] =  "\n# " + file_path.name + "\n" + "```python\n" + content + "\n```\n"
        else:
            data[str(file_path)] = content
    elif file_path.is_dir():
        print(f"Reading directory: {file_path}")
        for sub_path in [p for p in file_path.iterdir() if "__pycache__" not in str(p) and ".pyc" not in str(p)]:
            print(f"Reading sub-path: {sub_path}")
            child = recursive_read(sub_path, include, depth + 1, max_depth)
            print(f"Child: {child}")
            data.update(child)
    return data


@click.command("mdstream")
@click.argument("file", type=click.Path(exists=True))
@click.option("--depth", "-d", default=-1, help="Depth of headers")
@click.option("--save", "-s", help="Save markdown content to a file")
def cli(file, depth, save):
    """Stream markdown content from a file."""
    data = recursive_read(file,depth=0,max_depth=depth) 
    md_streamer = Markdown(data=data, save=save)
    from rich.traceback import install
    install(show_locals=True)
    md_streamer.stream()


def example():
    """Run an example with predefined JSON data."""
    json_data = [
        {
            "name": "markdown-to-json",
            "version": "2.1.2",
            "summary": "Markdown to dict and json deserializer",
            "latest_release": "2024-09-20T20:38:56",
            "author": "Nathan Vack",
            "earliest_release": {"version": "1.0.0", "upload_time": "2015-12-10T21:01:13", "requires_python": None},
            "urls": {
                "Bug Tracker": "https://github.com/njvack/markdown-to-json/issues",
                "Change Log": "https://github.com/njvack/markdown-to-json/blob/main/CHANGELOG.md",
            },
            "description": "# Markdown to JSON converter\n## Description\nA simple tool...",
            "requires_python": ">=3.8",
        }
    ]

    md_streamer = Markdown(data=json_data)
    md_streamer.stream()


if __name__ == "__main__":
    cli()
