import io
import time
import base64

from picamera2 import Picamera2


picam2 = Picamera2()
picam2.start()

data = io.BytesIO()
picam2.capture_file(data, format='jpeg')

print(base64.b64encode(data.getvalue()))
