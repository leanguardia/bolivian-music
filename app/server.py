import pandas as pd
import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify
from ast import literal_eval

from app.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/delgard/DataScience/bolivian-music/lake/bolivian_music_dev.db'
db.init_app(app)

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
