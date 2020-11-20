from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String(24), unique=True, nullable=False)
    name        = db.Column(db.String(180), nullable=False)
    tracks      = db.Column(db.Integer, nullable=False)
    owner_name  = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(360), nullable=False)

    def __repr__(self):
        return '<Playlist %s %s >' % (self.id, self.playlist_id)
