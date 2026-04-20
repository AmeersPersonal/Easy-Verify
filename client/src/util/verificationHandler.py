# from LLMs.llm import estimate_age, FAILED_STATUS_CODE
from util.webSocketHandler import finishVerify





def startVerification(img1, img2, img3, callUI):
    print("starting verification")
    # result = 0
    # try:
    #     result = estimate_age(img1, img2, img3)
    # except Exception as e:
    #     print("ERROR")
    #     print(e)

    # if result == FAILED_STATUS_CODE:
    #     callUI.failedVerify()
    #     print("Verification Error")
    # else:
    #     print(result)
    finishVerify()  # maybe pass estimated age here
