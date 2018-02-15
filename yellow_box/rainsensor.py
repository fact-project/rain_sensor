#!/usr/bin/env python
import os
import json
from datetime import datetime, timedelta
from yellow_box import YellowBox, YellowBoxMockup
import pandas as pd
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
        try:
            report = b.read()  # read blocks until a fresh report comes in
            average = build_running_average(
                report,
                width=timedelta(seconds=30)
            )
            write_to_current(average, current_path)
            with open(filename(outdir), 'a') as file:
                save_to_file(report, file)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # log the exception and and traceback
            log.exception('')


history = pd.DataFrame()


def build_running_average(report, width):
    NORM_LEN = 2 * 98404.
    now = datetime.utcnow()

    d = dict(report._asdict())
    s = pd.Series(d, name=now)
    s['cond'] = s.condensation_detector_number_of_pulses
    s['drops'] = s.drop_counter_pulse_length / NORM_LEN
    s.drop([
        'condensation_detector_pulse_length',
        'condensation_detector_number_of_pulses',
        'drop_counter_pulse_length',
        'drop_counter_number_of_pulses',
        'time_between_message_updates_in_ms',
        'chksum',
        'time_since_boot_in_ms',
    ], inplace=True)

    global history
    history = history.append(s)

    # cut away too old stuff
    history = history[now-width:now]

    average = history.mean()
    # the rain parameter in Final_Rain_Parameter.ipynb
    # was defined as:
    # the maximum of (cond, drops) devided by 2, **summed** over 30seconds.
    # But here I calculated the mean, so I have to multiply with 30. / 2. = 15.
    rain = max(average.cond, average.drops) * 15.
    # Using the mean instead of the sum, makes the range of the parameter
    # independend of the choice of the integration window.
    # So when people decide to integrate over 60 sec instead of 30,
    # the rain parameter should still be between 0..100.

    # At the start of the program, or when damaged reports come in,
    # we might get less than 30 reports in 30 seconds.
    # Whoever consumes the output of this program might want to ignore
    # results, which are based on less than ... dunno .. 3 reports?
    N = len(history)

    return {
        'time': now.isoformat(),
        'rain': rain,
        'statistics': N
    }


def filename(outdir):
    return os.path.join(
        outdir,
        datetime.utcnow().date().isoformat() + ".jsonl"
        )


def write_to_current(d, path):
    with open(path, 'w') as file:
        json.dump(d, file)


def save_to_file(report, file):
    d = dict(report._asdict())
    d['timestamp_utc'] = datetime.utcnow().isoformat()
    json.dump(d, file)
    file.write('\n')

if __name__ == '__main__':
    main()
