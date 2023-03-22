import cv2
import numpy as np
import base64
import time

from channels.generic.websocket import AsyncWebsocketConsumer


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            # Convert the image to bytes and then to base64
            img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
            img_base64 = base64.b64encode(img_bytes).decode()

            # Send the base64-encoded image to the client
            await self.send(img_base64)

            # Delay for a short period of time to limit the frame rate
            time.sleep(0.1)