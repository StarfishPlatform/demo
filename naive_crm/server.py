import itertools
import json
import os
from subprocess import call

from flask import Flask, render_template, request, redirect, url_for

BASE_SERVICE_ID = 'customer-crm'

os.environ.setdefault('STARFISH_API_URL', 'http://localhost:3000')

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


def load_jsonlines(path, count=None):
    with open(path, 'r') as f:
        lines = []
        for line in f:
            lines.append(json.loads(line))

    if count is None:
        return lines
    else:
        return itertools.islice(lines, count)


def run_filter(field, value, input, output, is_search=False, suffix=''):
    service_id = f'{BASE_SERVICE_ID}-search'
    if suffix:
        service_id += '-' + suffix

    env = os.environ.copy()
    env['STARFISH_SERVICE_ID'] = service_id

    p = ['python3', './scripts/demo_filter.py',
         '--field', field, '--value', value,
         '--output', output]

    if is_search:
        p += ['--search']

    p += [input]

    c = call(p, env=env)
    return c


@app.route('/')
def home():
    params = request.args

    profiles = load_jsonlines('data/dataset.jsonlines', count=100)
    return render_template('home.html', profiles=profiles, params=params)


@app.route('/filter', methods=['POST'])
def do_filter():
    f = request.form
    firstname = f['firstname']
    gender = f['gender']

    print("Start")
    c = None
    if gender and firstname:
        c = run_filter('name/first', firstname, is_search=True, input='./data/dataset.jsonlines',
                       output='/tmp/run0.jsonlines', suffix='phase1')
        print("INTERM=", c)
        c = run_filter('gender', gender, input='/tmp/run0.jsonlines', output='/tmp/run1.jsonlines', suffix='phase2')
    elif firstname:
        c = run_filter('name/first', firstname, is_search=True, input='./data/dataset.jsonlines',
                       output='/tmp/run1.jsonlines')
    elif gender:
        c = run_filter('gender', gender, input='./data/dataset.jsonlines', output='/tmp/run1.jsonlines')
    print('End, FILTER CALL=', c)

    # No computation (no filters), redirect to home
    if c is None:
        return redirect(url_for('.home'), code=302)

    # Else, send back parameters to render the result
    params = {}
    if gender:
        params['gender'] = gender
    if firstname:
        params['firstname'] = firstname

    return redirect(url_for('.show_run', run_id='run1', **params), code=302)


@app.route('/runs/<run_id>')
def show_run(run_id):
    params = request.args
    profiles = load_jsonlines(f'/tmp/{run_id}.jsonlines', count=100)
    return render_template('home.html', profiles=profiles, params=params)
