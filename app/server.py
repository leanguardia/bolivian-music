from flask import Flask
from flask import Flask
from flask import render_template, request, jsonify

import pandas as pd
import numpy as np
from ast import literal_eval

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
  artists = pd.read_csv('data/artists_grouped.csv')
  artists.genres = artists.genres.apply(literal_eval)
  ranked_artists = {}
  for group in artists.groupby('ranking'):
     ranked_artists[group[0]] = group[1].to_dict('records')
  return render_template('home.html', rank_artists=ranked_artists)


def main():
    app.run(host='0.0.0.0', port=3003, debug=True)


if __name__ == '__main__':
    main()
