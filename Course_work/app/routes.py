import os
import json
from datetime import datetime
from flask import render_template
from flask import redirect
from flask import request
from flask import g
from flask import abort
from flask import url_for
from flask import session
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required

from app import app, lm, db
from app.forms import LoginForm, EditProfileForm, SignUpForm, SearchForm
from app.models import User, ROLE_ADMIN, ROLE_USER, Card, Notepad, NON_PUBLIC, PUBLIC
from app.flashProxy import FlashProxy
from app.tablegateways import UserTableGateway, CardTableGateway
from app.strgenerator import StringGenerator
from app.games import CLASSIC_GAME, NON_CLASSIC_GAME
from app.gamebulder import GameBulder


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/index", methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous:
        return render_template('overview.html',
                               title="Overview")
    return render_template("index.html",
                           title="Home",
                           last_your_notepads=current_user.get_notepads().limit(4).all())


@app.route("/results")
def search_results():
    search_input = request.args.get('search_input', "", type=str)
    found_notepads = Notepad.get_notepads_by_name(search_input)
    return render_template('searchResult.html',
                           title=f'f res for {search_input}',
                           notepads=found_notepads,
                           search_input=search_input)


@app.route("/signUp", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        remember_me = sign_up_form.remember_me.data
        params = {
            "login": sign_up_form.login.data,
            "password_hash": User.hash_password(sign_up_form.password.data),
            "admin": ROLE_USER
        }
        user = User(**params)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=remember_me)
        return redirect(url_for('index'))
    return render_template('signUp.html',
                           title="Sign Up",
                           form=sign_up_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = UserTableGateway.get_user_by_login(
            login_form.login.data).first()
        password_is_correct = user.check_password(login_form.password.data)
        if password_is_correct:
            login_user(user, remember=login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            FlashProxy.flash("Invalid username or password", FlashProxy.DANGER)
    return render_template("login.html",
                           title='Login Page',
                           form=login_form)


@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.route('/userSettings', methods=['GET', 'POST'])
@login_required
def user_settings():
    edit_profile_form = EditProfileForm(current_user.login)
    if request.method == 'GET':
        edit_profile_form.login.data = current_user.login
        edit_profile_form.about_me.data = current_user.about_me
    elif edit_profile_form.validate_on_submit():
        new_login = edit_profile_form.login.data
        new_about_me = edit_profile_form.about_me.data

        current_user.change_login(new_login)
        current_user.set_about_me(new_about_me)

        db.session.commit()
        FlashProxy.flash('Your changes have been saved.', FlashProxy.SUCCESS)
        return redirect(url_for('user_settings'))
    return render_template('userSettings.html',
                           title='Users settings',
                           form=edit_profile_form)


@app.route('/stats')
@login_required
def statistics():
    notepads_for_repead = current_user.check_notepads()
    if not notepads_for_repead:
        notepads_for_repead = None
    return render_template('statistics.html',
                           title='Stats',
                           notepads = notepads_for_repead)


@app.route('/myNotepads')
@login_required
def notepads():
    page = request.args.get('page', 1, type=int)
    notepads = current_user.get_notepads().paginate(
        page, app.config["NOTEPADS_PER_PAGE"], True)
    next_url = url_for(
        'notepads', page=notepads.next_num) if notepads.has_next else None
    prev_url = url_for(
        'notepads', page=notepads.prev_num) if notepads.has_prev else None
    return render_template('myNotepads.html',
                           title='My notepads',
                           notepads=notepads.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           page=page)


@app.route('/publicNotepads')
def public_notepads():
    page = request.args.get('page', 1, type=int)
    # t = current_user.get_notepads().first()
    # FlashProxy.flash(t.day_when_learned)
    # FlashProxy.flash((datetime.now().date() - t.day_when_learned).days)
    # FlashProxy.flash(current_user.check_notepads())
    # FlashProxy.flash(current_user.get_notepads().all())
    notepads = Notepad.get_public_notepads().paginate(
        page, app.config["NOTEPADS_PER_PAGE"], True)
    next_url = url_for(
        'public_notepads', page=notepads.next_num) if notepads.has_next else None
    prev_url = url_for(
        'public_notepads', page=notepads.prev_num) if notepads.has_prev else None
    return render_template('publicNotepads.html',
                           title='Public notepads',
                           notepads=notepads.items,
                           prev_url=prev_url,
                           next_url=next_url)


@app.route('/editNotepad', methods=['GET', 'POST'])
@login_required
def edit_notepad():
    notepad_id = request.args.get('notepad_id', None, type=int)
    notepad = current_user.get_notepad(notepad_id).first_or_404()
    if not current_user.is_owner(notepad):
        abort(404)
    if request.method == 'POST':
        notepad_json_string = request.data.decode("UTF-8")
        # TODO Баг - если имя занято, сериализация пройдет с ошибкой
        notepad.deserialize(notepad_json_string)
        db.session.commit()
    return render_template('editNotepad.html',
                           title="Edit Notepad",
                           notepad=notepad)


@app.route('/createNotepad')
@login_required
def create_notepad():
    users_notepads = current_user.get_notepads().all()
    busy_names = [notepad.name for notepad in users_notepads]

    notepad_name = StringGenerator.make_unique_string(
        busy_names, "New notepad")

    new_notepad = current_user.create_notepad(notepad_name)
    db.session.add(new_notepad)
    db.session.commit()
    return redirect(url_for('edit_notepad', notepad_id=new_notepad.notepad_id))


@app.route('/user')
def user():
    page = request.args.get('page', 1, type=int)
    login = request.args.get('login', None, type=str)
    user = UserTableGateway.get_user_by_login(login).first_or_404()
    notepads = user.get_public_notepads().paginate(
        page, app.config["NOTEPADS_PER_PAGE"], True)
    next_url = url_for(
        'user', login=user.login, page=notepads.next_num) if notepads.has_next else None
    prev_url = url_for(
        'user', login=user.login, page=notepads.prev_num) if notepads.has_prev else None
    return render_template('user.html',
                           title=user.login,
                           user=user,
                           notepads=notepads.items,
                           prev_url=prev_url,
                           next_url=next_url)


@app.route("/getnotepadjson")
@login_required
def get_notepad_json():
    notepad_id = request.args.get('notepad_id', None, type=int)
    notepad = current_user.get_notepad(notepad_id).first()
    return notepad.to_json()


@app.route("/deleteNotepad", methods=["POST"])
@login_required
def delete_notepad():
    notepad_id = request.args.get('notepad_id', None, type=int)
    notepad_for_deliting = current_user.get_notepad(notepad_id)
    current_user.delete_notepad(notepad_for_deliting)
    db.session.commit()
    return "Successful"


@app.route("/flashMessage", methods=["POST"])
@login_required
def put_message():
    message = request.args.get('message', None, type=str)
    category = request.args.get('category', "info", type=str)
    FlashProxy.flash(message, category)
    return "Success"


@app.route("/test")
def test():
    return render_template("test.html")


@app.route('/previewNotepad')
def preview_notepad():
    notepad_id = request.args.get('notepad_id', None, type=int)
    notepad = Notepad.query.filter_by(notepad_id=notepad_id).first_or_404()
    if current_user.is_anonymous and not notepad.is_public():
        abort(404)
    return render_template('previewNotepad.html',
                           title=notepad.name,
                           notepad=notepad)


@app.route('/learning', methods=["GET", "POST"])
def learn():
    allowed_play_modes = frozenset([0, 1])
    mode = request.args.get("mode", None, int)
    notepad_id = request.args.get("notepad_id", None, int)
    if (mode not in allowed_play_modes) or (mode is None):
        abort(404)
    notepad = current_user.get_notepad(notepad_id).first_or_404()
    game = GameBulder.build_game(mode, notepad)
    return game.run()


@app.route('/mark_known/<card_id>/<play_mode>')
def mark_known(card_id, play_mode):
    card = CardTableGateway.get_card_by_id(card_id).first_or_404()
    card.known = True
    notepad_id = card.get_self_notepad().first().notepad_id
    db.session.commit()
    # FlashProxy.flash('Card marked as known.', FlashProxy.SUCCESS)
    return redirect(url_for('learn', notepad_id=notepad_id, mode=play_mode))
