from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
import cv2
import base64
import numpy as np

from mywebsocket.connection import WebSocket


class IndexView(TemplateView):
    template_name = "index.html"

'''

async def websocket_view(socket):
    await socket.accept()
    await socket.send_text('hello')
    await socket.close()
'''
def from_b64(uri):
    '''
        Convert from b64 uri to OpenCV image
        Sample input: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    encoded_data = uri.split(',')[1]
    data = base64.b64decode(encoded_data)
    np_arr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def to_b64(img):
    '''
        Convert from OpenCV image to b64 uri
        Sample output: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    _, buffer = cv2.imencode('.jpg', img)
    uri = base64.b64encode(buffer).decode('utf-8')
    return f'data:image/jpg;base64,{uri}'

def grayscale(data):
    try:
        img = from_b64(data)
        # Do some OpenCV Processing
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # End for OpenCV Processing
        #cv2.imshow('dfg',img)
        print(type(img))
        #img = cv2.putText(img, 'hi', (10,10), cv2.FONT_HERSHEY_SIMPLEX, 2, (125,0,255), 2, cv2.LINE_AA)
					
        return to_b64(img)
    except:
        # just in case some process is failed
        # normally, for first connection
        # return the original data
        return data

async def websocket_view(socket: WebSocket):
    await socket.accept()    
    while True:
        message = await socket.receive_jsonb()
        await socket.send_jsonb(grayscale(message))