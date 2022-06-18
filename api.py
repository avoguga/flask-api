import os

from flask import Flask, request, jsonify, send_from_directory

DIRETORIO = "/home/gus/Downloads/doeal/output"

api = Flask(__name__)

@api.route("/arquivos", methods=["GET"])
def lista_arquivos():
    arquivos = []

    for nome_do_arquivo in os.listdir(DIRETORIO):
        endereco_do_arquivo = os.path.join(DIRETORIO, nome_do_arquivo)

        if(os.path.isfile(endereco_do_arquivo)):
            arquivos.append(nome_do_arquivo)

    return jsonify(arquivos)


@api.route("/arquivos", methods=["POST"])
def post_arquivo():
    arquivo = request.files.get("files")

    print(arquivo)
    nome_do_arquivo = arquivo.filename
    arquivo.save(os.path.join(DIRETORIO, nome_do_arquivo))

    return '', 201


if __name__ == "__main__":
    api.run(debug=True, port=8000)