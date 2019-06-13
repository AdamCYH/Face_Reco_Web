import base64
import datetime

from face_reco_site import settings

RECOGNITION_IMG_UPLOAD = settings.RECOGNITION_IMG_UPLOAD
ENROLLMENT_IMG_UPLOAD = settings.ENROLLMENT_IMG_UPLOAD


def save_image(img_data, type, fname, lname="", img_name=""):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    if type == "recognition":
        img_storage_path = RECOGNITION_IMG_UPLOAD
        photo_path = "{}/{}_{}.png".format(img_storage_path, img_name, timestamp)
    elif type == "enrollment":
        img_storage_path = ENROLLMENT_IMG_UPLOAD
        photo_path = "{}/{}_{}_{}.png".format(img_storage_path, fname, lname, timestamp)

    with open(photo_path, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(img_data.split(",")[1])))
    return photo_path
