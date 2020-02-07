import os
import codecs
import json
import pandas as pd
import numpy as np

from flask import Flask, flash, request, redirect, url_for, send_file, render_template, session
from functools import wraps
from werkzeug.utils import secure_filename

from forms.form import LoginForm
from utils.gera_arquivo_txt import generate_txt_file

# URL base e extensão permitida
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, "upload")
ALLOWED_EXTENSIONS = set(["xls"])

app = Flask(__name__)
app.secret_key = "my_secret_key"

# Set meu path de upload no flask
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "upload")


def is_logged_in(f):
    """
    @access Public
    @desc   Verifica se existe uma sessão iniciada no sistema
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


def allowed_file(filename):
    """Função que verifica o tipo da extensão do arquivo para upload"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """
    @access Public
    @desc Carrega página principal
    """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    @access Public
    @desc   Acesso a login
    """
    form = LoginForm()

    if request.method == "POST":
        auth = False
        with open("users.json") as json_file:
            data = json.load(json_file)
            for user in data:
                if (user["username"] == form.username.data and user["password"] == form.senha.data):
                    session["logged_in"] = True
                    session["sped_username"] = user["username"]

                    return redirect(url_for("index"))
                else:
                    erro = "Usuário ou senha incorretos!"
                    return render_template("login.html", form=form, erro=erro)

    return render_template("login.html", form=form)


@app.route("/logout")
@is_logged_in
def logout():
    """
    @access Public
    @desc   Logout do sistema se existir uma sessão iniciada
    """
    session.clear()
    return redirect(url_for("index"))


@app.route("/blocoh", methods=["GET", "POST"])
@is_logged_in
def blocoh():
    """
    @access Private
    @desc Carrega coversão do bloco H
    """
    msg = None
    if request.method == "POST":
        # Verifico se o POST request tem o arquivo
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            msg = generate_txt_file(filename, session["sped_username"], basedir)
            if msg:
                return send_file(os.path.join(UPLOAD_FOLDER, session["sped_username"] + "-blocos_h_0200_k.txt"), 
                    as_attachment=True)
            else:
                return render_template("blocoh.html", msg=msg)

    return render_template("blocoh.html", msg=msg)


# Main
if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
