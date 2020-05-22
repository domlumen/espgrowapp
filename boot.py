
import usocket as socket
import utime as time

import sys
import network

from machine import Pin
import dht
import ds18x20
import onewire

import esp
esp.osdebug(None)

import gc
gc.collect()

import _thread
from machine import I2C
import ssd1306

#Sensor initialize
try:
  dht_sensor = dht.DHT22(Pin(25))
  print('found DHT22 Sensor')
except:
  print('failed to find DHT22 Sensor')
  pass

try:
  ds_pin = machine.Pin(4)
  ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
  roms = ds_sensor.scan()
  print('Found DS devices: ', roms)
except:
  print('failed to find DS18X20 sensor')
  pass
  

#OLED initialize
i2c = I2C(-1, scl=Pin(15), sda=Pin(4))

oled_width = 128
oled_height = 64
p = Pin(16, Pin.OUT)
p.value(1)
oled = ssd1306.SSD1306_I2C(oled_width, oled_width, i2c)

#relay initialize
r = Pin(26, Pin.OUT)
r.value(0)
#Network initialize
ssid = 'TC8715DA9'
password = 'TC8715D0D74A9'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())









