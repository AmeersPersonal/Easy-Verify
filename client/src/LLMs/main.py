from deepface import DeepFace
import cv2
import easyocr
import re
from datetime import datetime
import os

# we should use this for when to store the photo of the person and when to delete it, we can also use it to store the photos of the ID for a short period of time
PHOTO_DIR= os.path.dirname(os.path.realpath(__file__)) + "/temp_photos"
ID_DIR = os.path.dirname(os.path.realpath(__file__)) + "/temp_ids"

"""
I've decied this doesn't need OOP
instead we will just utlize the methods in the client class
Instead of extracting img from user idea lets have them take or upload a close up picutre of their idea of theri ID and anohter one to extract text
"""
#TODO: how do we define if it failed for some reason?
FAILED_STATUS_CODE = 324

def estimate_age(img1, img2, img3)-> int:
    """
    img paramters are img paths
    The AI will exmaine 3 images and will give an estimate age of the user
    """



    img_list = [img1, img2, img3]
    estimated_age = []

    try:
        for img in img_list:
            analysis = DeepFace.analyze(img_path=img, actions=["age"], enforce_detection=True, silent=True)
            #deals with multiple faces
            if isinstance(analysis, list):
                raise Exception
            else:
                age = analysis['age']
                estimated_age.append(age)

    except ValueError:
        pass
    except Exception:
        pass

    if not estimated_age or len(estimated_age) != len(img_list):
        return FAILED_STATUS_CODE

    #averaged out age, should we automatically choose to lowest one?

    final_guess = round(sum(estimated_age) / len(estimated_age))

    return final_guess

def verify_user_id(img1, img2)->bool:
    """
    Compres user id img to the img they recently took
    this will just return a bool
    """
    try:
        """
        TODO:
        Test differnt verfication models
        """
        analysis =  DeepFace.verify(img1_path=img1, img2_path=img2, model_name="VGG-face", detector_backend="retinaface", enforce_detection=True)

        return analysis["verified"]

    except ValueError:
        pass
    except Exception:
        pass

def extract_dob(img1):
    "This will extract DOB from an ID"
    reader = easyocr.Reader(['en'], gpu=False) # lets assume the user does not have a gpu for now, we can add it later
    result = reader.readtext(img1)
    dob_pattern = r'(\d{2}[-/]\d{2}[-/]\d{4})|(\d{4}[-/]\d{2}[-/]\d{2})'
    for res in result:
        text = res[1]
        match = re.search(dob_pattern, text)
        if match:
            dob_str = match.group(0)
            try:
                dob = datetime.strptime(dob_str, '%d-%m-%Y')
            except ValueError:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d')
                except ValueError:
                    continue
            return dob.date()
    return None


def cleanup_temp_files():
    """
    This will clean up the temp photos and ids after we are done with them
    should we implement this after running the functions or after we get the results back to the user?
    """

    for folder in [PHOTO_DIR, ID_DIR]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
