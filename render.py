#!/usr/bin/env python3

"""
Render Jinja template.
"""

from typing import TextIO, Sequence, Dict
from types import SimpleNamespace
from jinja2 import Template
import click
from yaml import Loader, Node


def construct_object(loader: Loader, node: Node) -> object:
    """
    Build a object (not a dict) from a YAML parse tree.
    """
    res = SimpleNamespace()
    for key, value in loader.construct_mapping(node).items():
        if key.startswith("__") and key.endswith("__"):
            continue
        setattr(res, key, value)
    return res


def load_parameter_file(parameter_file: TextIO) -> Dict:
    """
    Load a parameter file (YAML format).
    """
    loader = Loader(parameter_file)
    loader.add_constructor(u"!object", construct_object)
    return loader.get_data()


@click.command()
@click.argument("parameter_files", metavar="CONFIG", type=click.File("rt"), nargs=-1)
@click.option("-o", "output", metavar="CONFIG", default="-")
def main(parameter_files: Sequence[TextIO], output: str) -> None:
    parameters = {}
    for parameter_file in parameter_files:
        parameters.update(load_parameter_file(parameter_file))
    template_filename = "templates/" + parameters["template"]
    template = Template(open(template_filename, "rt").read())
    with click.open_file(output, "w") as f:
        f.write(template.render(**parameters))


if __name__ == "__main__":
    main()
