from deepface import DeepFace
import cv2

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

    final_guess = round(sum(estimate_age) / len(estimate_age))

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
