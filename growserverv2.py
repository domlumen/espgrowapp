###########################
#Created by Lumen Limitless
#Grow Server v2
###########################

upip.install('uasyncio')
import picoweb

app = picoweb.WebApp(__name__)

tempLimit = 80
humLimit = 65
temp = hum = 0

def garbage_collect():
  if gc.mem_free() < 102000:
    gc.collect()
    print('Garbage Collected')
    
def read_sensor():
    global temp, hum
    garbage_collect()
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

            # uncomment for Fahrenheit
            temp = temp * (9/5) + 32.0

            hum = round(hum, 1)
            temp = round(temp, 1)
            return(msg)
        else:
            return('Invalid sensor readings.')
    except: KeyboardInterrupt:
      sys.exit()
    except OSError as e:
        return('Failed to read sensor.')


def sensor_thread():
    while True:
        read_sensor()
        time.sleep(2.5)


def oled_thread():
    while True:
        oled.fill(0)
        oled.show()
        oled.text("Air Temp " + str(temp) + "F", 0, 65)
        oled.text("Humidity " + str(hum) + "%", 0, 75)
        oled.show()
        time.sleep(2.5)


def relay_thread():
    while True:
        if temp > 70 or hum > 50:
            r.value(1)
        else:
            r.value(0)


@app.route("/")
def index(req, resp):

    if req.method == 'POST':
        pass
    else:
        if r.value() == 1:
            relay_state = "ON"
        else:
            relay_state = "OFF"
        yield from picoweb.start_response(resp)
        yield from resp.awrite("""<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://kit.fontawesome.com/79ca270dd8.js" crossorigin="anonymous"></script>
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
     background-color: black;
     color: white;
    }
    h2 { font-size: 3.0rem; color: green; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>Grow Server</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="labels">Humidity</span>
    <span>"""+str(hum)+"""</span>
    <sup class="units">%</sup>
  </p>
  <p>
    <i class="fas fa-fan" style="color:#aaa2aa;"></i> 
    <span class="labels">Exhaust: """+relay_state+"""</span>
  </p>
  <form action="form">
  <input name="setTemp"/>
  <input name="setHum"/>
  <input type="submit"/>
  </form>
</body>
</html>""")


@app.route("/form")
def form(req, resp):
    global tempLimit, humLimit
    if req.method == 'POST':
        yield from req.read_form_data()
        tempLimit = int(req.form["setTemp"])
        humLimit = int(req.form["setHum"])
    else:
        yield from picoweb.start_response(resp)
        yield from resp.awrite("<h1>DONE</h1> <a href="/">go back</a>")


if __name__ == '__main__':
    _thread.start_new_thread(sensor_thread, ())
    _thread.start_new_thread(relay_thread, ())
    _thread.start_new_thread(oled_thread, ())
    app.run(debug=True, host="192.168.0.132")


