#!/usr/local/bin/python3

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/<string:url_path>')
def path(url_path):
    return render_template(url_path)