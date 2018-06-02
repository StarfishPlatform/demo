import json
import os
from collections import defaultdict

import click

os.environ['STARFISH_API_URL'] = os.environ.get('STARFISH_API_URL', 'http://localhost:3000')


def process(filename, jline, field, accum):
    accum[jline.get(field, None)] += 1


@click.command()
@click.option('--field', '-f', default='age')
@click.option('--output', '-O', type=click.Path())
@click.argument('files', nargs=-1, type=click.Path())
def demo_filter(field, files, output):
    accum = defaultdict(int)

    for filename in files:
        with open(filename, 'r') as f:
            for line in f:
                jline = json.loads(line)
                process(filename, jline, field, accum)

    with open(output, 'w') as out:
        json.dump(accum, out)


if __name__ == '__main__':
    demo_filter()
