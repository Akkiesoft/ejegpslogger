#!/usr/bin/env python3
import os
import time
import json
from datetime import datetime
from pa1010d import PA1010D
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735
import threading
import socketserver
from http import server

def disp_loop():
  global draw, gps, timestamp, lat, lng, sat
  while True:
    result = gps.update()
    if result:
      timestamp = gps.data['timestamp']
      lat = gps.data['latitude']
      lng = gps.data['longitude']
      sat = gps.data['num_sats']
      rec = str(recording)

      # for display
      draw.rectangle((0, 0, 160, 80), (0, 0, 0))
      MESSAGE = """
N: {:.5f}
E: {:.5f}
Sats: {:s}
Rec: {:s}
""".format(lat, lng, sat, rec)
      draw.text((0, -15), MESSAGE, font=font, fill=(255, 255, 255))
      disp.display(img)
    time.sleep(1.0)

def record_loop():
  global lat, lng, sat, recording
  while True:
    if recording:
      now = datetime.now()
      nowstr = "{:4d}/{:02d}/{:02d},{:02d}:{:02d}:{:02d}".format(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second
      )
      f = open(recording, 'a')
      f.write("{:s},{:.5f},{:.5f},{:s}\n".format(nowstr, lat, lng, sat))
      f.close()
    time.sleep(10)

class Handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        global timestamp, lat, lng, sat, recording
        response = 200
        if self.path == "/":
            body = html
        elif self.path == "/location":
            body_json = {
                'time': str(timestamp),
                'latitude': lat,
                'longitude': lng,
                'sat': sat,
                'recording': recording
            }
            body = json.dumps(body_json)
        elif self.path == "/rec/start":
            if recording:
              response = 400
              body = 'now recording.'
            else:
              now = datetime.now()
              recording = "{:4d}{:02d}{:02d}-{:02d}{:02d}{:02d}.csv".format(
                now.year, now.month, now.day,
                now.hour, now.minute, now.second
              )
              f = open(recording, 'w')
              f.write("Date,Time,Latitude,Longitude,Sats\n")
              f.close()
              body = recording
        elif self.path == "/rec/stop":
            recording = 0
            body = "0"
        elif self.path == "/rec/status":
            body = str(recording)
        else:
            response = 404
            body = "Not found"
        body = bytes(body, 'UTF-8')
        self.send_response(response)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
  allow_reuse_address = True
  daemon_threads = True


if __name__ == '__main__':
  timestamp = 0
  lat = 5
  lng = 5
  sat = 0
  recording = 0

  # Create ST7735 LCD display class.
  disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    rotation=90,
    spi_speed_hz=10000000
  )
  disp.begin()
  img = Image.new('RGB', (160, 80), color=(0, 0, 0))
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
  draw.text((0, 0), "starting...", font=font, fill=(255, 255, 255))
  disp.display(img)

  # init GPS
  gps = PA1010D()
  time.sleep(2)

  # load html
  RUNDIR = os.path.dirname(os.path.abspath(__file__))
  f = open(RUNDIR + "/webui.html", 'r')
  html = f.read()
  f.close()

  try:
    running = True
    disp_thread = threading.Thread(target=disp_loop)
    disp_thread.setDaemon(True)
    disp_thread.start()

    record_thread = threading.Thread(target=record_loop)
    record_thread.setDaemon(True)
    record_thread.start()

    address = ('', 80)
    server = StreamingServer(address, Handler)
    server.serve_forever()
  except KeyboardInterrupt:
    running = False
