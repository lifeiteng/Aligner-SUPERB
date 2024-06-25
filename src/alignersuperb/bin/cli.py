import logging

import click
from lhotse.utils import fix_random_seed
from lhotse.utils import Pathlike


@click.group()
def cli():
    pass

@cli.group()
def run():
    pass


@run.command()
@click.argument("align_path", type=click.Path(allow_dash=True))
@click.option(
    "-t",
    "--target-path",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the target textgrid files.",
)
@click.option(
    "--force-segment",
    is_flag=True,
    help="Force keep original text segment, only update(re-align) the timestamp.",
)
def eval(
    align_path: Pathlike,
    target_path: Pathlike,
    force_segment: bool,
):
    """
    Eval forced alignment metrics.

    .. hint::
        ``--force-segment`` must be used when you don't re-segment the text.
    """
    logging.info(f"TODO")


