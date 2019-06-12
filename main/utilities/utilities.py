import base64
import datetime
import os

from face_reco_site import settings


IMG_STORAGE_PATH = settings.IMG_STORAGE_PATH


def save_image(img_name, img_data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    photo_path = "{}/{}_{}.png".format(IMG_STORAGE_PATH, img_name, timestamp)
    with open(photo_path, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(img_data.split(",")[1])))
    return photo_path


