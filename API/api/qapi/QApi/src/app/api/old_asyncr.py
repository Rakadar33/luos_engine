from fastapi import APIRouter, HTTPException
import os
import time
import subprocess
import asyncio
import nest_asyncio

nest_asyncio.apply()
router = APIRouter()

class SysCall():
    async def run(self):

        shell = 1
        args = "sh /qa/hello.sh"
        args = "sh /qa/hello_wait.sh"
        args = "python3 /qa/test.py"
        args = "sh /qa/detection.sh"

        if shell:
            proc = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE)
        else:
            proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE)

        #'''

        #'''
        #proc = await asyncio.create_subprocess_exec(
        #                'ping','-c', '2', 'www.google.fr',
        #                stdout=asyncio.subprocess.PIPE)
        #'''


        '''
        asyncio.gather(self.run_proc(proc), self.kill_proc(proc))
        await proc.wait()

        #return {"result": "Hello Luos\n"}
        return {"return": str(proc.stdout)        
        '''

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
            return {"return": "111 : "+ str(stdout)}
        except asyncio.TimeoutError:
            # If it timed out we should terminate the process
            try:
                proc.kill()
            except OSError:
                # Ignore 'no such process' error
                pass
            finally:
                return {"error": "timeout"}


    async def run_proc(self, proc):
        while True:
            line = await proc.stdout.readline()
            if line == b'':
                #time.sleep(1)
                break

    async def kill_proc(self, proc):
        await asyncio.sleep(5)
        proc.kill()


@router.get("/rtb")
async def a_test():
    syscall = SysCall()
    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(syscall.run())
    return ret
    #loop.close()
'''

def callback(fut: asyncio.Future):
    pass
    """just prints result. Callback should be sync function"""
    if not fut.cancelled() and fut.done():
        print(fut.result())
    else:
        print("No results")


#async def dummy_run_script():    
#    await asyncio.sleep(6)
#    result = 10
#    return result

async def run_script():
    """this is something which takes a lot of time"""
    script_path="./"
    command = ["sh hello.sh"]
    #command = ["python3 -c \"print(1)\""]
    #command = ["pyluos-bootloader detect /dev/ttyUSB0"]    
    command = ["sh hello_wait.sh"]
    proc = subprocess.Popen(command,                            
                            universal_newlines=True,
                            cwd=script_path,                            
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out

@router.get("/test")
async def a_test():
    """Main async func in the app"""

    # create task
    task = asyncio.create_task(run_script())
    #task.add_done_callback(callback)

    # try to await the task
    try:
        result = await asyncio.wait_for(task, timeout=1)
    except asyncio.TimeoutError as ex:
        return {"error" : "Timeout"}
    else:
        return {"result" : result}
'''
