import json

import click
from starfish_shell import ShellFactory


def profile_matcher(profile):
    return profile['login']['username']


FACTORY = ShellFactory.from_env(matcher=profile_matcher)


def get_field(field, jline):
    for f in field:
        jline = jline.get(f, {})
    return str(jline).lower()


def filter_profiles(profiles, field, value, is_search):
    for profile in profiles:
        current_value = get_field(field, profile)

        if (is_search and value in current_value) or (current_value == value):
            yield profile


@click.command()
@click.option('--field', '-f', default='age')
@click.option('--search/--no-search', default=False)
@click.option('--value', '-V', default='25')
@click.option('--output', '-O', type=click.Path())
@click.argument('files', nargs=-1, type=click.Path())
def demo_filter(field, search, value, files, output):
    field = field.split('/')
    filtered = []

    for filename in files:
        with open(filename, 'r') as f:
            jlines = (json.loads(line) for line in f)
            shelled = FACTORY.shell_iterator(jlines, source=filename)

            profiles = filter_profiles(shelled, field, value, is_search=search)
            filtered += list(profiles)

    with open(output, 'w') as out:
        shelled = FACTORY.shell_iterator(filtered, destination=output)
        for x in shelled:
            json.dump(x, out)
            out.write('\n')


if __name__ == '__main__':
    demo_filter()
