#!/usr/bin/env python
import os
import json
from datetime import datetime
from yellow_box import YellowBox, YellowBoxMockup

import click
import logging

logging.basicConfig(
    filename=os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        'rainsensor.log'
    ),
    level=logging.DEBUG
)
log = logging.getLogger(__name__)


@click.command()
@click.argument(
    'outdir',
    type=click.Path(exists=True, file_okay=False)
    )
@click.argument(
    'current_path',
    type=click.Path()
    )
@click.option('--debug', is_flag=True)
def main(outdir, current_path, debug):
    if debug:
        b = YellowBoxMockup()
    else:
        b = YellowBox()

    while True:
        report = b.read()  # read blocks until a fresh report comes in
        write_to_current(report, current_path)
        with open(filename(outdir), 'a') as file:
            save_to_file(report, file)


def filename(outdir):
    return os.path.join(
        outdir,
        datetime.utcnow().date().isoformat() + ".jsonl"
        )


def write_to_current(report, path):
    with open(path, 'w') as file:
        d = dict(report._asdict())
        d['timestamp_utc'] = datetime.utcnow().isoformat()
        json.dump(d, file)


def save_to_file(report, file):
    d = dict(report._asdict())
    d['timestamp_utc'] = datetime.utcnow().isoformat()
    json.dump(d, file)
    file.write('\n')

if __name__ == '__main__':
    main()
