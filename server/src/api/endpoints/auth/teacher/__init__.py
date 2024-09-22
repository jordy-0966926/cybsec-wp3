from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from server.src.lib.models.user import Teacher as User

blueprint = Blueprint('teacher', __name__, template_folder='templates')

# Source: https://stackoverflow.com/questions/60532973/how-do-i-get-a-is-safe-url-function-to-use-with-flask-and-how-does-it-work


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@blueprint.route('/teacher', methods=['GET', 'POST'])
def teacher_login():
    if current_user.is_authenticated:
        return {'status': 'ok'}

    if request.method == 'POST':
        session_user = User()
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))

        if session_user.authenticate_user(username, password):
            login_user(session_user, remember=False)
            # Check for 'next' parameter in the request URL
            next_page = session.get('next')
            if not next_page or not is_safe_url(next_page):
                next_page = url_for('agendas_blueprint.agendas')

            return redirect(next_page)

    return render_template('auth_teacher.jinja')


@blueprint.route('/logout')
@login_required
def teacher_logout():
    logout_user()
    return redirect(url_for('auth_blueprint.user_login'))
