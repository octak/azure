from App.database import db
from App.models import *


def create_picture(url):
    picture = Picture(url)
    db.session.add(picture)
    db.session.commit()
    return picture

def get_picture_by_id(pictureID):
    return Picture.query.get(pictureID)

def get_all_pictures():
    return Picture.query.all()

def get_all_pictures_json():
    pictures = get_all_pictures()
    if not pictures:
        return []
    pictures.sort(key=lambda picture: picture.average_rating, reverse=True)
    pictures = [picture.toJSON() for picture in pictures]
    return pictures
