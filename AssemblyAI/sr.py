import pyaudio
import websockets
import asyncio
import base64
import json
import os
auth_key = 'b85db88421954a8ea7b604c93a017787'

dirname = os.path.dirname(__file__)
content_path = os.path.join(dirname, 'content.txt')

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():
   print(f'Connecting websocket to url ${URL}')
   async with websockets.connect(
       URL,
       extra_headers=(("Authorization", auth_key),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           while True:
               try:
                   data = stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   
                   await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:   
                   print(e)
                   
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               await asyncio.sleep(0.01)

           return True

       async def receive():
           while True:
               try:
                   result_str = await _ws.recv()
                  # print(json.loads(result_str)['text'])
                  # print(json.loads(FinalTranscript)['text'])
                   
                   msg_object = json.loads(result_str)
                   if msg_object['message_type'] == 'FinalTranscript':
                       print(msg_object['text'])
                       file_object = open(content_path, 'a')
                       file_object.write (msg_object['text'])
                       file_object.write("\n")
                       file_object.write (" ")
                       file_object.close()
                   
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"

       send_result, receive_result = await asyncio.gather(send(), receive())
       


asyncio.run(send_receive())