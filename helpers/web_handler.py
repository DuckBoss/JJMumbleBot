from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, validators, StringField
from helpers.global_access import GlobalMods as GM
from plugins.youtube.youtube_helper import YoutubeHelper as YH
import utils
from shutil import copyfile
from cheroot.wsgi import Server as WsgiServer, PathInfoDispatcher
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
            if command[0] == GM.cfg['Main_Settings']['CommandToken']:
                GM.jjmumblebot.remote_command(command)
                flash(command)
                return redirect('/')
            else:
                flash(f"Error: Commands must start with [{GM.cfg['Main_Settings']['CommandToken']}]")
        else:
            flash("Error: A command is required!")
    return render_template('index.html', form=form)


@web_app.route("/history", methods=['GET', 'POST'])
def cmd_history():
    cmd_strings = list(GM.cmd_history.queue_storage)
    return render_template('history.html', cmd_strings=cmd_strings)


@web_app.route("/youtube", methods=['GET', 'POST'])
def cmd_youtube():
    cmd_strings = list(YH.queue_instance.queue_storage)
    return render_template('youtube.html', cmd_strings=cmd_strings, cur_playing=YH.current_song_info)


def init_web():
    d = PathInfoDispatcher({'/': web_app})
    GM.web_server = WsgiServer((GM.cfg['Web_Interface']['WebIP'], int(GM.cfg['Web_Interface']['WebPort'])), d)
    GM.web_server.start()


def stop_web():
    if GM.web_server is not None:
        GM.web_server.stop()
