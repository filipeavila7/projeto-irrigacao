from flask import jsonify, render_template

from src import app

# Estado simulado
estado_irrigacao = {
    "agua": 0,  # 0 = desligado, 1 = ligado
    "umidade": 45,  # valor simulado da umidade
}

# Usuário de teste
usuarios = {"email@gmail.com": "1234"}  # e-mail: senha


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify(estado_irrigacao)


@app.route("/ligar", methods=["POST"])
def ligar():
    estado_irrigacao["agua"] = 1
    return "", 204


@app.route("/desligar", methods=["POST"])
def desligar():
    estado_irrigacao["agua"] = 0
    return "", 204


@app.route("/forgot", methods=["GET"])
def forgot():
    return render_template("esqueci_a_senha.html")


@app.route("/resetar_senha", methods=["GET"])
def reset():
    return render_template("resetar_senha.html")


@app.route("/sent", methods=["GET"])
def sent():
    return render_template("sent.html")


@app.route("/painel_admin", methods=["GET"])
def painel_admin():
    return render_template("painel_admin.html")
