import logging

import click
from lhotse.utils import Pathlike, fix_random_seed

from alignersuperb.metrics import UtteranceBoundaryError, WordBoundaryError
from alignersuperb.utils import find_files, map_files, parse_textgrid, print_table

formatter = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(format=formatter, level=logging.WARNING)


@click.group()
def cli():
    fix_random_seed(0)


@cli.group()
def run():
    pass


@run.command()
@click.argument("align_path", type=click.Path(allow_dash=True, dir_okay=True, file_okay=False))
@click.option(
    "-t",
    "--target-path",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Path to the target textgrid files.",
)
def metrics(
    target_path: Pathlike,
    align_path: Pathlike,
):
    """
    Eval forced alignment metrics.
    """
    return _metrics(target_path, align_path)

def _metrics(
    target_path: Pathlike,
    align_path: Pathlike,
):
    """
    Eval forced alignment metrics.
    """
    target_files = map_files(find_files(target_path, extension=".TextGrid"))
    align_files = map_files(find_files(align_path, extension=".TextGrid"))

    # filter out missing target files
    keep = []
    for key in align_files.keys():
        if key not in target_files:
            # logging.warn(f"Missing target file for {key}")
            continue
        keep.append(key)

    logging.info(f"TARGET {len(target_files)} files, ALIGN {len(align_files)} files, keep {len(keep)} files.")

    target_files = {k: v for k, v in target_files.items() if k in keep}
    align_files = {k: v for k, v in align_files.items() if k in keep}

    target_files = parse_textgrid(target_files)
    align_files = parse_textgrid(align_files)

    metrics_fn = [WordBoundaryError(), UtteranceBoundaryError()]

    table = {}
    for fn in metrics_fn:
        v = fn(target_files, align_files)
        table.update(v)
    print_table(
        table,
        col_list=["UBE_Start", "UBE_End", "WBE", "WBE_Start", "WBE_End", "Num UTTerances"],
        aligner_name=str(align_path).split("/")[-1],
    )


if __name__ == "__main__":
    import sys
    _metrics(sys.argv[1], sys.argv[2])
