import random
import os
import cloudinary
from cloudinary.api import resources
from cloudinary.uploader import upload

from flask import Flask, request, jsonify, send_from_directory, render_template

DIRETORIO = "/home/gus/Downloads/doeal/output"

app = Flask(__name__)

@app.route("/arquivos", methods=["GET"])
def lista_arquivos():
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
      api_secret=os.getenv('API_SECRET'))
    result = resources()
    return jsonify(result)

@app.route("/upload/arquivo", methods=['POST'])
def upload_file():
  app.logger.info('in upload route')

  cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
  upload_result = None
  if request.method == 'POST':
    file_to_upload = request.files['file']
    app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = upload(file_to_upload)
      app.logger.info(upload_result)
      return jsonify(upload_result)

@app.route('/')
def index():
    return "<h1>A rota para dar POST é /upload/arquivo! <br/> <br/> Para dar GET use a rota /arquivos!</h1>"

if __name__ == "__main__":
    app.run(debug=True, port=8000)