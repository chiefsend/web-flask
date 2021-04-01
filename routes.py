from urllib.parse import urljoin
from flask import render_template, redirect, url_for, current_app, abort, request, flash
from werkzeug.exceptions import HTTPException

import requests as api
from chiefsend import app
from util import AuthForm, get_password, set_password, SearchForm


@app.route('/privacy')
def privacy():
    return render_template('Privacy.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/', methods=['GET', 'POST'])
def landing():
    form = SearchForm()
    if form.validate_on_submit():
        share_id = form.query.data.split(sep="/")[-1]
        return redirect(url_for('download', share_id=share_id))

    return render_template('Landing.html', form=form)


@app.errorhandler(HTTPException)
def http_error(e):
    return render_template('Error.html', e=e)


@app.route('/public')
def public():
    res = api.get(urljoin(current_app.config['API_URL'], '/shares'))
    if res.status_code != 200:
        abort(res.status_code)
    else:
        shares = res.json()
        return render_template('Public.html', shares=shares)


@app.route('/d/<string:share_id>/')
def download(share_id):
    password = get_password(share_id)
    if password:
        res = api.get(urljoin(current_app.config['API_URL'], f'/share/{share_id}'), auth=(share_id, password))
    else:
        res = api.get(urljoin(current_app.config['API_URL'], f'/share/{share_id}'))

    if res.status_code == 401:
        return redirect(url_for('download_auth', share_id=share_id))
    elif res.status_code != 200:
        abort(res.status_code)
    else:
        share = res.json()
        print(share)
        return render_template('Download.html', up=share)


@app.route('/d/<string:share_id>/auth', methods=['GET', 'POST'])
def download_auth(share_id):
    form = AuthForm()
    if form.validate_on_submit():
        set_password(share_id, form.password.data)
        return redirect(url_for('download', share_id=share_id))
    else:
        for field, error in form.errors.items():
            from markupsafe import Markup
            flash(Markup(f'<b>{field}:</b> {error}'), category='danger')

    flash('Zugriff verweigert.', category='danger')
    return render_template('DownloadAuth.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('Upload.html')


@app.route('/shared/<string:share_id>')
def shared(share_id):
    return render_template('Shared.html', share_id=share_id)
