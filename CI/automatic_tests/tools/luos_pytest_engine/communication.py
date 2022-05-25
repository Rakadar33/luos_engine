# coding:utf-8

tab= 50*" "


def send_Luos_JSON_Command(s, cmd, sleep_time=0.001):
    cmd = cmd + '\n\r'
    print(f"---> JSON Send :       {cmd}")
    s.write(cmd.encode())
    

def receive_Luos_JSON_Command(expected_message=''):
    msg = 'no message'    
    if expected_message=='':
        debug_retry=0        
        data = USBserial.readline() 
        if len(data) != 0:
            try :
                msg = json.loads(data)
                print(f"{tab}<--- JSON Receive :\n")                
                print(json.dumps(msg, indent=4, sort_keys=True))                

            except :
                msg = data.decode("utf-8")
                print(f"{tab}<--- JSON Error decoding message :    {msg}")
                pass
            return msg
    else:
        debug_retry=1
        debug_error=0
        error_msg_buffer=[]
        unexepected_msg_buffer=[]
        for i in range(1000):
            data = USBserial.readline()
            
            '''if i%100 == 0:
                print(f"retry number {i}")'''
            
            if len(data) != 0:
                try :
                    debug_retry+=1
                    msg = json.loads(data)
                    if expected_message in str(data):
                        print(f"Expected message received : {expected_message}")
                        break
                    elif not "{}" in str(data):
                        unexepected_msg_buffer.append(msg)
                except :
                    msg = data.decode("utf-8")
                    error_msg_buffer.append(msg)
                    debug_error+=1
                    pass
            time.sleep(0.01)

        '''
        # Print error for Debug
        pprint(f"{tab}{debug_error} errors")
        for _,err in enumerate(error_msg_buffer):
            pprint(f"{tab}ignore:{err}")
            
        # Print unexpected message for Debug
        pprint("Unexpected Message")
        print(unexepected_msg_buffer)
        print(f"{tab}<--- {debug_retry-1} retry")
        '''
        
        # Print message        
        print(f"{tab}<--- JSON Receive message {expected_message} :\n")                
        print(json.dumps(msg, indent=4, sort_keys=True))

        return msg
