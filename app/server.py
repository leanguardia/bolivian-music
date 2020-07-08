from flask import Flask
from flask import Flask
from flask import render_template, request, jsonify

import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
  return render_template('home.html')


def main():
    app.run(host='0.0.0.0', port=3003, debug=True)


if __name__ == '__main__':
    main()
