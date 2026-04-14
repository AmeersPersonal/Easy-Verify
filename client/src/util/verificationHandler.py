from LLMs.llm import estimate_age, FAILED_STATUS_CODE
from util.webSocketHandler import finishVerify


def startVerification(img1, img2, img3):
    print("starting verification")
    result = 0
    try:
        result = estimate_age(img1, img2, img3)
    except Exception as e:
        print("ERROR")
        print(e)
    if result == FAILED_STATUS_CODE:
        print("Verification Error")
    else:
        finishVerify() # maybe pass estimated age here
    
        
    