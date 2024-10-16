#! /usr/bin/env python3

# Copyright (c) 2020, 2022-2024 D. Bohdan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import annotations

import argparse
import contextlib
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, TYPE_CHECKING

import psutil

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

__version__ = "0.6.0"


DEFAULT_RECORD_TIME = 1000
DEFAULT_SAMPLE_TIME = 200
SPARKLINE_TICKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
USAGE_DIVISOR = 1 << 20  # Report memory usage in binary megabytes.


def main() -> None:
    args = cli(sys.argv)

    with open_output(args.output_path, sys.stderr) as output:
        try:
            start_dt = datetime.now(tz=timezone.utc)
            process = psutil.Popen([args.command, *args.arguments])
            maximum, history, timestamps = track(
                process,
                output,
                newlines=args.newlines,
                sparkline_length=args.length,
                wait_record=args.record,
                wait_sample=args.sample,
                mem_format=args.mem_format,
                quiet=args.quiet,
            )
            process.wait()

            if not history:
                print("no data collected", file=output)
            else:
                if not args.newlines and not args.quiet:
                    print(file=output)
                summary = summarize(
                    history,
                    maximum,
                    start_dt,
                    datetime.now(tz=timezone.utc),
                    args.mem_format,
                    args.time_format,
                )
                print("\n".join(summary), file=output)

            if args.dump_path != "":
                with Path(args.dump_path).open("w") as dump_file:
                    for value, timestamp in zip(history, timestamps):
                        print(timestamp // 1_000_000, value, file=dump_file)
        except Exception as err:  # noqa: BLE001
            tb = sys.exc_info()[-1]
            frame = traceback.extract_tb(tb)[-1]
            line = frame.lineno
            file_info = (
                f"file {Path(frame.filename).name!r}, "
                if "__file__" in globals() and frame.filename != __file__
                else ""
            )

            print(
                f"\nerror: {err}\n"
                f"(debug info: {file_info}line {line}, "
                f"exception {type(err).__name__!r})",
                file=output,
            )
            sys.exit(1)

        sys.exit(process.returncode)


def hms_delta(
    start_dt: datetime,
    end_dt: datetime,
) -> tuple[int, int, float]:
    delta = end_dt - start_dt
    total_millis = (
        delta.days * 24 * 60 * 60 * 1000
        + delta.seconds * 1000
        + delta.microseconds // 1000
    )

    hours, rem = divmod(total_millis, 60 * 60 * 1000)
    minutes, rem = divmod(rem, 60 * 1000)
    seconds = rem / 1000

    return hours, minutes, seconds


def summarize(
    history: Sequence[int],
    maximum: int,
    start_dt: datetime,
    end_dt: datetime,
    mem_format: str,
    time_format: str,
) -> list[str]:
    return [
        (" avg: " + mem_format) % (sum(history) / len(history) / USAGE_DIVISOR),
        (" max: " + mem_format) % (maximum / USAGE_DIVISOR),
        "time: " + time_format % hms_delta(start_dt, end_dt),
    ]


def cli(argv: Sequence[str]) -> argparse.Namespace:
    argv0 = Path(sys.argv[0])
    prog = (
        f"{Path(sys.executable).name} -m {argv0.parent.name}"
        if argv0.name == "__main__.py"
        else argv0.name
    )

    parser = argparse.ArgumentParser(
        description="Track the RAM usage (resident set size) of a process and "
        "its descendants in real time.",
        prog=prog,
    )
    parser.add_argument(
        "command",
        default=[],
        help="command to run",
    )
    parser.add_argument(
        "arguments",
        default=[],
        help="arguments to command",
        metavar="args",
        nargs=argparse.REMAINDER,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-d",
        "--dump",
        default="",
        dest="dump_path",
        help="file in which to write full memory usage history when finished",
        metavar="path",
    )
    parser.add_argument(
        "-l",
        "--length",
        default=20,
        dest="length",
        help="sparkline length (default: %(default)d)",
        metavar="n",
        type=int,
    )
    parser.add_argument(
        "-m",
        "--mem-format",
        default="%0.1f",
        dest="mem_format",
        help='format string for memory amounts (default: "%(default)s")',
        metavar="fmt",
        type=str,
    )
    parser.add_argument(
        "-n",
        "--newlines",
        action="store_true",
        default=False,
        help="print new sparkline on new line instead of over previous",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        dest="output_path",
        help='output file to append to ("-" for standard error)',
        metavar="path",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="do not print sparklines, only final report",
    )
    parser.add_argument(
        "-r",
        "--record",
        default=None,
        help=(
            "how frequently to record/report memory usage "
            f"(default: every {DEFAULT_RECORD_TIME} ms)"
        ),
        metavar="ms",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--sample",
        default=None,
        help=(
            "how frequently to sample memory usage "
            f"(default: every {DEFAULT_SAMPLE_TIME} ms)"
        ),
        metavar="ms",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--time-format",
        default="%d:%02d:%04.1f",
        dest="time_format",
        help='format string for run time (default: "%(default)s")',
        metavar="fmt",
        type=str,
    )
    parser.add_argument(
        "-w",
        "--wait",
        default=None,
        help=(
            'set "--sample" and "--record" time simultaneously '
            "(that both options override)"
        ),
        metavar="ms",
        type=int,
    )

    args = parser.parse_args(argv[1:])

    if args.record is None:
        args.record = args.wait or DEFAULT_RECORD_TIME
    if args.sample is None:
        args.sample = args.wait or DEFAULT_SAMPLE_TIME

    return args


@contextlib.contextmanager
def open_output(path: str, fallback: IO[str]) -> Iterator[IO[str]]:
    handle = fallback
    if path != "-":
        handle = Path(path).open("a", 1)  # noqa: SIM115

    try:
        yield handle
    finally:
        if handle is not sys.stderr:
            handle.close()


def track(
    parent: psutil.Popen,
    output: IO[str],
    *,
    newlines: bool = False,
    sparkline_length: int = 20,
    wait_sample: int = 100,
    wait_record: int = 1000,
    mem_format: str = "0.1f%",
    quiet: bool = False,
) -> tuple[int, list[int], list[int]]:
    core_fmt = "%s " + mem_format
    fmt = core_fmt + "\n" if newlines else "\r" + core_fmt
    history = []
    # The time when the last record was added to history
    # in nanoseconds since the epoch.
    last_record_time = 0
    # The time when the sample was taken in nanoseconds since the epoch.
    last_sample_time = 0
    # The maximum total resident set size overall.
    maximum = 0
    # The maximum total resident set size since the last record.
    record_maximum = 0
    timestamps = []

    def add_record(current_time: int) -> None:
        nonlocal last_record_time

        if current_time - last_record_time < wait_record * 1_000_000:
            return

        history.append(record_maximum)
        timestamps.append(current_time)
        last_record_time = current_time

        if not quiet:
            latest = history[-sparkline_length:]
            line = sparkline(0, maximum, latest)
            print(
                fmt % (line, record_maximum / USAGE_DIVISOR),
                end="",
                file=output,
            )

    try:
        while parent.is_running() and parent.status() != psutil.STATUS_ZOMBIE:
            tree = parent.children(recursive=True)
            tree.append(parent)

            current_total = sum([x.memory_info().rss for x in tree])
            record_maximum = max(current_total, record_maximum)
            maximum = max(record_maximum, maximum)

            current_time = time.time_ns()
            add_record(current_time)

            delta = (current_time - last_sample_time) // 1_000_000
            last_sample_time = current_time
            time.sleep(max(0, (wait_sample - delta) / 1000))

        add_record(time.time_ns())
    except (KeyboardInterrupt, psutil.NoSuchProcess):
        pass

    return (maximum, history, timestamps)


def sparkline(minimum: float, maximum: float, data: Sequence[float]) -> str:
    tick_max = len(SPARKLINE_TICKS) - 1

    if minimum == maximum:
        return SPARKLINE_TICKS[0]

    return "".join(
        SPARKLINE_TICKS[int(tick_max * (x - minimum) / (maximum - minimum))]
        for x in data
    )


if __name__ == "__main__":
    main()
