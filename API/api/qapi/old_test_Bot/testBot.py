import multiprocessing
import queue
import subprocess
import smtplib
from email.utils import formatdate, formataddr
from email.mime.text import MIMEText
from typing import List
from xml.dom.pulldom import END_ELEMENT
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zeroconf import DNSAddress

# ------------------------------------------------------------------------------------------------
#     TUTO HERE :
#
#     https://ichi.pro/fr/fastapi-comment-traiter-les-demandes-entrantes-par-lots-12336388900588
#
# -------------------------------------------------------------------------------------------------


# ---------------
# HTML Page
# ---------------
html_qa = """
<!DOCTYPE html>
<html>
    <head>
        <title>QA Test</title>
    </head>
    <body>
        <h1>FASTAPI WebSocket - QA Test</h1>
        <h2>ID: <span id="ws-id"></span></h2>
        <h2>Available tests : RTB, Hello</h1>        
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Launch Test</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


# ---------------
# Class
# ---------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_answer_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


# ---------------
# Params
# ---------------
test_path = "/var/www/PF/Quality_assurance/Platforms/Delivery_Platform/Tests"
log_path = "/var/www/PF/Quality_assurance/Platforms/Delivery_Platform/Results/test_result.log"

# ---------------ex
# Functions
# ---------------
def send_mail(message):
    name= message.split("\"")[1]
    msg = MIMEText(message)
    msg['From'] = formataddr(('Luos PF Robot', 'pf.qa@luos.io'))
    msg['To'] = formataddr(('Luos Team', 'robot.qa@luos.io'))
    msg['Subject'] = f"[PF Robot] Test result : {name}"

    server = smtplib.SMTP('localhost')
    try:
        server.sendmail('pf.qa@luos.io', ['robot.qa@luos.io'], msg.as_string())
        #server.sendmail('pf.qa@luos.io', ['jerome.galan@luos.io'], msg.as_string())
    except:
        print("[DEBUG] ERROR : mail is not sent")
        pass
    finally:
        server.quit()

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

def embedded_test(test_params):
    test_list = {"RTB": "test_detect.py",
                 "Hello": "hello.sh"}

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
        send_mail(f"\"{test_params}\" : Timeout")
        return(f"\"{test_params}\" : Timeout")
    else:
        test_result = messageQueue.get()        
        send_mail(f"\"{test_params}\" : {test_result}")
        return(f"\"{test_params}\" : {test_result}")

async def push_result():
    for i in range(testAPP.queue_limit):
        if not testAPP.queue_system.empty():
            obj = testAPP.queue_system.get_nowait()
            if obj['websocket'] in manager.active_connections:
                await manager.send_answer_message(f"[Test Result] {obj['message']}", obj['websocket'])


# -----------------------------------------------------------------
# main
# -----------------------------------------------------------------
messageQueue = multiprocessing.Queue(maxsize=2)

testAPP = FastAPI()
testAPP.queue_system = queue.Queue()
testAPP.queue_limit = 5

manager = ConnectionManager()

refresh= 1
testAPP.scheduler = AsyncIOScheduler()
testAPP.scheduler.add_job(push_result, 'interval', seconds=refresh)
testAPP.scheduler.start()


# ---------------
# End points
# ---------------

@testAPP.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            test_params = await websocket.receive_text()
            #testAPP.queue_system.put({"message": "Coucou", "websocket": websocket})            
            result = embedded_test(test_params)
            testAPP.queue_system.put({"message": result, "websocket": websocket})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client #{client_id} disconnected")


@testAPP.get("/")
async def qa_main():
    return HTMLResponse(html_qa)

@testAPP.get("/ping")
def pong():
    return {"ping": "pong!"}

@testAPP.post("/post_test")
def test():
    print("post OK")
    pass
#curl -X POST 
#-H "Content-Type: application/json" -d '{"test":Hello, "param":128}' '127.0.0.1:8000/post_test'



router = APIRouter()


@router.get("/test_route")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}


testAPP.include_router(test_route.router)