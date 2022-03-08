__name__ = 'main' # have to change the name for some reason otherwise it wont import

from flask import Blueprint, make_response, render_template

main_router = Blueprint(__name__, 'routes')

@main_router.route('/')
def home():
    return render_template('home.html')

@main_router.route('/signin')
def signin():
    return render_template('sign_in.html')

@main_router.route('/signup')
def signup():
    return render_template('sign_up.html')

@main_router.route('/signout')
def signout():
    return make_response(200, 'SIGNED_OUT')

@main_router.route('/account')
def account():
    return render_template('account.html')