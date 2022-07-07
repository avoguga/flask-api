import os
import cloudinary
from cloudinary.api import resources
from cloudinary.uploader import upload
import requests
import psycopg2
import csv
import re

# Variables
portarias_regex = r'^(PORTARIA)(.{0,200}) (con(.{0,3})ce(.{0,3})der(.{0,3})f.(.{0,3})ri(.{0,3})as) (.{0,600}),(.\n?)(.\s?)(.{0,10})(\d{2}(.{0,3})de(.{0,10})\d{4}.)((.*?)+\n)((.*?)+\n)((.*?)+\n)'
portaria_n_regex  = r'^(PORTARIA)(.{0,30})(\d{0,5})\/(20\d{2})'
servidor_regex = r'(ser(.{0,3})vi(.{0,3})do(.{0,6}))(\s?)(\n?)(.*?)(,|\n)'
cpf_regex = r'CPF(.{0,20})\d{2}(\s?)(\n?)'
matricula_regex = r'ma(.{0,3})tr(.{0,4})cu(.{0,3})la(.{0,3})n(.{0,5})(.*?)[A-Za-z]{1}'
cargo_regex = r'car(.{0,3})go(.{0,4})de(.{0,3})(.*?),'
data_assinatura_regex = r'/AL,(.*?)\.'


# Functions
def text(filename):
    import fitz # PyMuPDF
    print('Iniciando extração de texto do .pdf...')
    with fitz.open(filename) as doc:
        text = "" 
        for page in doc:
            text += page.get_text()
    print('Extração finalizada.')
    return text


def data(text):
    print('Iniciando mineração de dados...')
    # Database Connection
    connection = ''
    connection = psycopg2.connect(database = 'd5pfqaru9r1sh9',
                                            user = 'wntytvnytmlydw',
                                            password = '2ef597f114dabe4d52ac4a17983bfc35d74730f07397cbd1b0bfb7ec35a28b8b',
                                            host = 'ec2-52-206-182-219.compute-1.amazonaws.com')
    # Extraction
    portarias = re.finditer(portarias_regex, text, flags = re.I | re.DOTALL | re.MULTILINE)
    with open('extracao_doeal.csv', 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file)
        # First row
        w.writerow(['evento','portaria','servidor(a)','cpf','matricula','cargo','data_assinatura'])
        for portaria in portarias:
            # Columns (Search)
            evento = 'Concessão de Férias'
            portaria_n = re.search(portaria_n_regex, portaria.group(), flags = re.I | re.DOTALL | re.MULTILINE)
            servidor = re.search(servidor_regex, portaria.group(), flags = re.I | re.DOTALL | re.MULTILINE)
            cpf = re.search(cpf_regex, portaria.group(), flags = re.I | re.DOTALL | re.MULTILINE)
            matricula = re.search(matricula_regex, portaria.group(), flags = re.I | re.DOTALL | re.MULTILINE)
            cargo = re.search(cargo_regex, portaria.group(), flags = re.I | re.DOTALL | re.MULTILINE)
            data_assinatura = re.search(data_assinatura_regex, portaria.group(), flags = re.I | re.DOTALL | re.MULTILINE)
            # Columns (String)
            portaria = portaria_n.group().replace('portaria/'.upper(),'').replace('portaria'.upper(),'') if portaria_n is not None else ''
            servidor = servidor.group().replace('-','').replace('\n','').replace('servidora','').replace('servidor','').replace('(a)','').replace(',','').strip() if servidor is not None else ''
            cpf = cpf.group()[6:].replace('\n','').replace(' ','').replace('º','') if cpf is not None else ''
            matricula = matricula.group().replace('matrícula','').replace('matricula','').replace('\n','').replace(',','').replace('n.','').replace('n','').replace(' ','').replace('p','').replace('º','') if matricula is not None else ''
            cargo = cargo.group().replace('de','').replace(',','').replace('\n','').replace('-','').replace('cargo','').strip() if cargo is not None else ''
            data_assinatura = data_assinatura.group().replace('\n','').replace('AL','').replace(',','').replace('.','').replace('/','').replace('  ',' ').strip() if data_assinatura is not None else ''
            # Write .csv
            print(servidor)
            w.writerow([evento, portaria, servidor, cpf, matricula, cargo, data_assinatura])
            # Postgres Insert
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO servidor (nome, cpf, matricula, cargo) VALUES(%s, %s, %s, %s)", (servidor, cpf, matricula, cargo))      
                connection.commit()                     
            except (Exception, psycopg2.Error) as error:
                print("Error ao carregar os dados", error)   

    cursor.close()
    connection.close()

    print('Mineração finalizada.')


from flask import Flask, request, jsonify, send_from_directory, render_template


api = Flask(__name__)

@api.route("/arquivos", methods=["GET"])
def lista_arquivos():
    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
      api_secret=os.getenv('API_SECRET'))
    result = resources()
    return jsonify(result)

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

@api.route('/extrair')
def extract():
  txt = text('DOEAL.pdf')
  data(txt)
  return "<h1>A rota para dar POST é /upload/arquivo! <br/> <br/> Para dar GET use a rota /arquivos!</h1>"

if __name__ == "__main__":
    api.run(debug=True, port=8000)