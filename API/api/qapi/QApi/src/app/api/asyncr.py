from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from email.utils import formataddr
from email.mime.text import MIMEText
import asyncio
import nest_asyncio
import smtplib


nest_asyncio.apply()
router = APIRouter()

# Constants
SCRIPT_PATH="/qa"

# Test database
test_db = {
    "RTB": "detection.sh",
    "pyRTB": "detection_python.sh",    
    "Hello": "hello.sh",
    "Timeout": "hello_wait.sh",        
    "Stress": "stress.py",
    "Unknown": "bad.azerty"}

# Data model Class
class PlatformParameters(BaseModel):
    title: str
    description: Optional[str] = None

# System call Class
class SysCall():
    async def run(self, cmd):
        try:
            proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
            return {"return": str(stdout)}
        except asyncio.TimeoutError:
            # If it timed out we should terminate the process
            try:
                proc.kill()
            except OSError:
                # Ignore 'no such process' error
                pass
            finally:
                return {"error": "timeout"}
    '''
    async def run_proc(self, proc):
        while True:
            line = await proc.stdout.readline()
            if line == b'':
                break

    async def kill_proc(self, proc):
        await asyncio.sleep(5)
        proc.kill()
    '''

# Functions
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
        status = 0
    except:
        print("[DEBUG] ERROR : mail is not sent")
        status = 1
        pass
    finally:
        server.quit()
        return status


# End points
@router.get("/rtb")
async def rtb():
    cmd = f"sh {SCRIPT_PATH}/detection.sh"
    syscall = SysCall()
    loop = asyncio.get_event_loop()
    output = loop.run_until_complete(syscall.run(cmd))
    #return str(output).split("Gate")[-1].split(">")[0:2]
    output = str(output).split("Gate")[-1].split(">")[0:2]
    node_1 = output[0].split("\\")[0]
    node_2 = output[1].split("\\")[0]
    return [node_1, node_2]


@router.post("/platform")
async def platform(pf: PlatformParameters):
    if(pf.title in str(test_db.keys())):    
        # Test is in list ?
        cmd = test_db[pf.title]
        cmd_type = cmd.split(".")[-1]
        if (cmd_type != "sh") and (cmd_type != "py"):
            return(f"DB error : forbidden script type : {cmd_type}")
        cmd = f"{cmd_type} {SCRIPT_PATH}/{cmd}"            
    else:
        # Test is NOT in list
        return(f"Unknown test : {pf.title}")
    syscall = SysCall()
    loop = asyncio.get_event_loop()
    
    result = loop.run_until_complete(syscall.run(cmd))
    send_mail(f"\"{pf.title}\" : {result}")
    return result
