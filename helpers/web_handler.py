from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, validators, StringField
from helpers.global_access import GlobalMods as GM
from cheroot.wsgi import Server as wsgiserver, PathInfoDispatcher
from os import urandom

web_app = Flask(__name__)
web_app.config['SECRET_KEY'] = urandom(16)


class CommandForm(Form):
    commandField = StringField('Command: ', validators=[validators.DataRequired()])


@web_app.route("/", methods=['GET', 'POST'])
def main():
    form = CommandForm(request.form)
    if request.method == 'POST':
        command = request.form['commandField']
        if form.validate():
            GM.jjmumblebot.remote_command(command)
            flash(f'Command Sent: {command}')
            return redirect('/')
        else:
            flash("Error: A command is required!")
    return render_template('index.html', form=form)


def init_web():
    d = PathInfoDispatcher({'/': web_app})
    GM.web_server = wsgiserver((GM.cfg['Web_Interface']['WebIP'], int(GM.cfg['Web_Interface']['WebPort'])), d)
    GM.web_server.start()


def stop_web():
    if GM.web_server is not None:
        GM.web_server.stop()
