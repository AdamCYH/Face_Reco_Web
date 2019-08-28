import base64
import datetime

from face_reco_site import settings

RECOGNITION_IMG_UPLOAD = settings.RECOGNITION_IMG_UPLOAD
ENROLLMENT_IMG_UPLOAD = settings.ENROLLMENT_IMG_UPLOAD


def save_image(img_data, request_type, fname="", lname="", img_name=""):
    """
    This function saves image to local server.
    :param img_data: base64 image data
    :param request_type: could be enrollment or recognition, they will be stored in a different place
    :param fname: fname used as part of the file name
    :param lname: lname used as part of the file name
    :param img_name: original image name if available
    :return: photo path
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")

    if request_type == "recognition":
        img_storage_path = RECOGNITION_IMG_UPLOAD
        photo_path = "{}/{}_{}.png".format(img_storage_path, img_name, timestamp)
    elif request_type == "enrollment":
        img_storage_path = ENROLLMENT_IMG_UPLOAD
        photo_path = "{}/{}_{}_{}.png".format(img_storage_path, fname, lname, timestamp)

    with open(photo_path, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(img_data.split(",")[1])))
    return photo_path
