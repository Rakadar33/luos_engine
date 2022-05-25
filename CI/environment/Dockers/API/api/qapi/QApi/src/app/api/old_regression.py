from fastapi import APIRouter
import multiprocessing
import queue
import subprocess


# ---------------
# Params
# ---------------
test_path = "/var/www/PF/Quality_assurance/Platforms/Delivery_Platform/Tests"
log_path = "/var/www/PF/Quality_assurance/Platforms/Delivery_Platform/Results/test_result.log"

test_list = {
    "RTB": "test_detect.py",
    "Hello": "hello.sh",
    "KO": "aaa.bbb"}

# ---------------
# Main
# ---------------
router = APIRouter()
messageQueue = multiprocessing.Queue(maxsize=2)

# ---------------
# Functions
# ---------------
def end_of_test():
    print("[DEBUG] End of test")
    pass

def test_script(command, script, messageQueue):
    result = "Test started"
    #print("[DEBUG] Start TEST SCRIPT Thread")
    try:
        print(f"[DEBUG] RUN : {command} {script}")
        process = subprocess.Popen([command, script],
                                   universal_newlines=True,
                                   cwd=test_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        result, error = process.communicate()
        print(f"[DEBUG] RESULT : {result[0:10]}")
        print(f"[DEBUG] ERROR : {error[0:10]}")
    except:
        result = "Sys error"
        pass
    if len(error):
        #print(f"[DEBUG ] length {len(error)}")
        #print(f"[DEBUG] process.returncode : {process.returncode}")
        #print(f"[DEBUG ] error --{error}--")
        #print("[DEBUG ] ERROR processing command")
        result = error
    #print("[DEBUG] END TEST SCRIPT Thread wit result :")
    #print(f"[DEBUG] {result}")
    #print(result)
    messageQueue.put(result)
    #print("[DEBUG] Queue PUT OK")

def aaaaaembedded_test(test_params):
    result = "FATAL"
    if(test_params in test_list.keys()):
        # Test is in list
        script = test_list[test_params]
        script_type = script.split(".")[1]
        if script_type == "sh":
            # Shell script
            command = script_type
        elif script_type == "py":
            # Python script
            command = "python3"
        else:
            return(f"Forbidden script type {script_type}")
    else:
        # Test is NOT in list
        return(f"Unknown test \"{test_params}\"")

    # Launch test
    test_process = multiprocessing.Process(target=test_script, args=(command, script, messageQueue),)
    test_process.start()
    timeout_test_process = 8  # seconds
    test_process.join(timeout_test_process)

    if test_process.is_alive():
        print("Test Timeout")
        # Terminate - may not work if process is stuck for good
        test_process.terminate()
        # OR Kill - will work for sure, no chance for process to finish nicely however
        # p.kill()
        test_process.join()
        #send_mail(f"\"{test_params}\" : Timeout")
        end_of_test()
        result= f"\"{test_params}\" : Timeout"
    else:
        test_result = messageQueue.get()        
        #send_mail(f"\"{test_params}\" : {test_result}")
        result= f"\"{test_params}\" : {test_result}"

    end_of_test()
    return(result)

#'''
def embedded_test(test_params):
    end_of_test()
    return("EMBDED")
#'''


#@router.post("/regression") !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@router.post("/reg")
async def non_reg_test():
    '''
    print("[DEBUG] GOOOOO")
    embedded_test("Hellooooo")
    print("[DEBUG] AWAIT")    
    #result = await end_of_test()
    #print(f"[DEBUG] AWAIT END WITH RESULT: {result}")
    '''

    test_result= 'OK111'
    return {"result": test_result}
