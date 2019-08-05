import functools
import os

from flask import (flash, redirect, render_template, request,
                   send_from_directory, session, url_for)

from app import app
from app.forms import TranslateForm
from app.handlers import (TerminateHandler, TranslateEnRus, TranslateEnUk,
                          TranslatorRusEn, TranslatorRusUk)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')


@app.route("/index")
@app.route('/')
def index():
    return render_template('index.html',
                           title='Main page')


@app.route('/translator', methods=['GET', 'POST'])
def translator():
    translate_form = TranslateForm()

    fisrt_t_rus_en = TranslatorRusEn()
    t_rus_uk = TranslatorRusUk()
    t_en_rus = TranslateEnRus()
    t_en_uk = TranslateEnUk()
    terminate = TerminateHandler()

    handlers = [fisrt_t_rus_en, t_rus_uk, t_en_rus, t_en_uk]

    chain = functools.reduce(lambda acc, tr: tr.set_next(
        acc), handlers, terminate)

    if translate_form.validate_on_submit():
        text_for_translate = translate_form.input_text.data
        dest_language = translate_form.to_language.data
        translated_text = chain.translate(text_for_translate, dest_language)

        session['dest'] = dest_language
        session['text'] = text_for_translate

        if translated_text is None:
            flash("Нужный переводчик отсутсвует", 'danger')
            return redirect(url_for('translator'))

        session['translated_text'] = translated_text
        return redirect(url_for('translator'))

    if request.method == 'GET':
        translate_form.input_text.data = session.pop('text', "Input text")
        translate_form.output_field.data = session.pop(
            'translated_text', "")
        translate_form.to_language.data = session.pop('dest', '')
    return render_template('translate.html',
                           title="translate",
                           translate_form=translate_form)


@app.route('/about')
def about():
    return render_template('about.html',
                           title='About')
