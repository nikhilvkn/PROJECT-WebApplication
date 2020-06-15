#!/usr/local/bin/python3

from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
from inception import Server, Service, InceptionTools
from pathlib import Path
from collections import Counter
import sys
import datetime

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/<string:url_path>')
def path(url_path):
    return render_template(url_path)


@app.route('/count_service', methods=['POST','GET'])
def count_service():
   if request.method == 'POST':
      datacenter = request.form['Datacenter']
      environment = request.form['Environment']
      result = {}
      service_list = []

      data = InceptionTools(datacenter)
      work_fulldata = data.dc_data()

      for elements in work_fulldata['dynconfigMonitoringServerUrls']:
         for values in elements['url']:
            if elements['environment'] == environment:
               service_list.append(values['container'])
      count = Counter(service_list)
      counter = 0
      for key, value in count.items():
         if value < 3:
            counter += 1
            result[key] = str(value)
      return render_template('result.html', data=result)
      if counter == 0:
         return render_template('output.html', data='All services have 3 or more instances')


@app.route('/server-check', methods=['POST','GET'])
def server_check():
   if request.method == 'POST':
      datacenter = request.form['Datacenter']
      environment = request.form['Environment']
      inception_service = request.form['Service']

   if inception_service:
      service_data = inception_service.split(',')
      inception_request = Service(datacenter, environment)
      all_service = inception_request.specific_service()
      for content in service_data:
         if content not in all_service:
            return render_template('output.html',data = f'''FileNotFound Exception: Service {content} not found in {environment} environment.
   Please re-check service name''')
            sys.exit()
      inception_request = Server(datacenter, environment, service_data)
      return render_template('result-data.html', data = inception_request.specific_service())

   if datacenter:
      if bool(datacenter) ^ bool(environment):
         inception_request = Server(datacenter)
         return render_template('result-data.html', data = inception_request.all_server())
      else:
         inception_request = Server(datacenter, environment)
         return render_template('result-data.html', data = inception_request.specific_server())