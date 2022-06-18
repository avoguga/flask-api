import os

from flask import Flask, request, jsonify, send_from_directory

DIRETORIO = "/home/gus/Downloads/doeal/output"

app = Flask(__name__)

@app.route("/arquivos", methods=["GET"])
def lista_arquivos():
    arquivos = []

    for nome_do_arquivo in os.listdir(DIRETORIO):
        endereco_do_arquivo = os.path.join(DIRETORIO, nome_do_arquivo)

        if(os.path.isfile(endereco_do_arquivo)):
            arquivos.append(nome_do_arquivo)

    return jsonify(arquivos)


@app.route("/arquivos", methods=["POST"])
def post_arquivo():
    arquivo = request.files.get("files")

    print(arquivo)
    nome_do_arquivo = arquivo.filename
    arquivo.save(os.path.join(DIRETORIO, nome_do_arquivo))

    return '', 201

@app.route('/')
def index():
    return "<h1>A rota para dar POST ou GET é a rota /arquivos!</h1>"


if __name__ == "__main__":
    app.run(debug=True, port=8000)