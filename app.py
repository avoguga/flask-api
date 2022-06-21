import random
import os
import cloudinary
from cloudinary.uploader import upload

from flask import Flask, request, jsonify, send_from_directory, render_template

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

@api.route("/upload/arquivo", methods=['POST'])
def upload_file():
  api.logger.info('in upload route')

  cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
  upload_result = None
  if request.method == 'POST':
    file_to_upload = request.files['file']
    api.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = upload(file_to_upload)
      api.logger.info(upload_result)
      return jsonify(upload_result)

@api.route('/')
def index():
    return "<h1>A rota para dar POST é /upload/arquivo! <br/> <br/> Para dar GET use a rota /arquivos!</h1>"

if __name__ == "__main__":
    api.run(debug=True, port=8000)