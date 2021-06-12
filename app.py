'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
import cv2
from flask import Flask, render_template, request
from flask import Flask, render_template, Response
app = Flask(__name__)

def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    camera = cv2.VideoCapture(0)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define sensors GPIOs
button = 20
senPIR = 16

#define actuators GPIOs
ledRed = 14
ledYlw = 18
ledGrn = 27
ledBlk = 23

#initialize GPIO status variables
buttonSts = 0
senPIRSts = 0
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0
ledBlkSts = 0

# Define button and PIR sensor pins as an input
GPIO.setup(button, GPIO.IN)   
GPIO.setup(senPIR, GPIO.IN)

# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT)
GPIO.setup(ledBlk, GPIO.OUT) 

# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)
GPIO.output(ledBlk, GPIO.LOW)
	
@app.route("/")
def index():
	# Read GPIO Status
	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
	ledBlkSts = GPIO.input(ledBlk)

	templateData = {
      'button'  : buttonSts,
      'senPIR'  : senPIRSts,
      'ledRed'  : ledRedSts,
      'ledYlw'  : ledYlwSts,
      'ledGrn'  : ledGrnSts,
	  'ledBlk'	: ledBlkSts,
      }
	return render_template('index.html', **templateData)
	camera.release()
# The function below is executed when someone requests a URL with the actuator name and action in it:
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
	if deviceName == 'ledYlw':
		actuator = ledYlw
	if deviceName == 'ledGrn':
		actuator = ledGrn
	if deviceName == 'ledBlk':
		actuator = ledBlk
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
	ledBlkSts = GPIO.input(ledBlk)
   
	templateData = {
	  'button'  : buttonSts,
      'senPIR'  : senPIRSts,
      'ledRed'  : ledRedSts,
      'ledYlw'  : ledYlwSts,
      'ledGrn'  : ledGrnSts,
	  'ledBlk'	: ledBlkSts,
	}
	return render_template('index.html', **templateData)
	camera.release()
        

    
    




if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
