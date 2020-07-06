# Bolivian Artists Recommender
### Sistema de recomendación de Música Boliviana

Bolivian musicians are very talented but unfortunately not many people know it. This data-based project aims to promote bolivian artists and make them more visible for locals and the world.

The project consists in:
- The construction of a dataset of bolivian artists by fetching public Spotify data.

- The application of data clustering techniques to segment the collected data and gain
  artists description.
- The implementation of a web app for data visualization and knowledge-based artist recommendations.

## Dependencies

- Python 3
- Jupyter Notebook
- Spotipy
- Pandas
- Numpy
- Matplotlib
- Flask

## Project Structure
### App
### Data
### Models
- Artist-Clustering.ipynb

## Recommender
Fask app


## Dataset Construction
At the time of starting this project, no dataset with Bolivian music was found. Hence, a data
was collected and the dataset was built from strach.

### Collection and Filtering

```
python data/spotify_playlists.py
```

## Future Work
- Improve genre classification (crowd-sourced data labelling).
- Extend artist data (e.g. group/individual, starting dates, number of tracks/albums, languages).
- Implement track collector

Contributions are welcome.

## Acknowledgements
Udacity, Spotify, Bolivian Musicians, and family and friends who helped me identifying genres.

## Licence
Copyright (c) 2020 Leandro Guardia