from gpiozero import MotionSensor

pir=MotionSensor(4)

while True:
	if pir.motion_detected:
		print ('κίνηση')
	else:
		print ('ηρεμία')
