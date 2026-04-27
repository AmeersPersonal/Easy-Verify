from LLMs.llm import estimate_age, FAILED_STATUS_CODE
from util.webSocketHandler import finishVerify
import threading


#These two events control the thread where the LLM runs
verificationEvent = threading.Event()
errorEvent = threading.Event()
verificationSucess = False
result = 0
errorImageID = -1

def verificationThreadEvent(img1, img2, img3, verificationEvent, errorEvent):
    global result
    global verificationSucess
    global errorImageID
    try:
        result = estimate_age(img1, img2, img3)
    except ValueError as e:
        print(e)
        errorImageID = int(str(e))
        print(errorImageID)
        errorEvent.set()
    except Exception as e:
        print("ERROR")
        print(e)
        errorEvent.set()
    if result == FAILED_STATUS_CODE:
        verificationEvent.set()
        print("Verification Failed")
    else:
        verificationSucess = True
        verificationEvent.set()


def startVerification(img1, img2, img3, callUI):
    #Steps:
        # switch to loading screen
        # run the llm in a new thread and wait for the event
        # when the event is set, we then switch to the done screen

    print("starting verification")
    callUI.mainUI.switchToLoadingUI()
    global result
    #run the llm in a seperate thread, then wait for the events
    verifyingThread = threading.Thread(
        target=verificationThreadEvent,
        daemon=True,
        args = (img1, img2, img3, verificationEvent, errorEvent)
    )
    verifyingThread.start()
    while not verificationEvent.is_set():
        callUI.mainUI.root.update()
        if errorEvent.is_set():
            print("ERROR")
            print(errorImageID)
            #FUNCTION TO HANDLE ERROR HERE
            # switch to the corresponding ui status and go back to the verify ui
            break
    #handle the thread events

    print(result)
    global verificationSucess
    finishVerify(verificationSucess)  # maybe pass estimated age here
    callUI.mainUI.switchToCompleteUi()
    callUI.mainUI.doneInterface.setStatus("Verified Sucessfully")
