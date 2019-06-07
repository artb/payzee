# import the necessary packages
from imutils.video import VideoStream
from picamera import PiCamera
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

#imports raspberry hardware
pinoVerde = 18
buzzer = 23
pinoVermelho = 24

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinoVerde,GPIO.OUT)
GPIO.setup(pinoVermelho,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

#Variavel pra n deixar que o mesmo qrcode seja lido em varios segundos
qrCodeLido = 0

#Funcoes de controle dos componentes	
def piscaSucesso():
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho
	GPIO.output(pinoVerde,GPIO.HIGH) #acendo verde
	GPIO.output(buzzer,GPIO.HIGH) #apito
	time.sleep(1)
	GPIO.output(buzzer,GPIO.LOW) #desapito
	GPIO.output(pinoVerde,GPIO.LOW) #apago verde
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho

def piscaFracasso():
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho
	GPIO.output(buzzer,GPIO.HIGH) #apito
	time.sleep(1)
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho
	time.sleep(1)
	GPIO.output(pinoVermelho,GPIO.LOW) #apago vermelho
	time.sleep(1)
	GPIO.output(pinoVermelho,GPIO.HIGH) #acendo vermelho
	GPIO.output(buzzer,GPIO.LOW) #apito

# construct the argument parser and parse the arguments - infelizmente precisa disso
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# init da camera
print("[RASPBERRY] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()
GPIO.output(pinoVermelho,GPIO.HIGH)
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)
		# loop over the detected barcodes
	for barcode in barcodes:
		# the barcode data is a bytes object so if we want to draw it
		# on our output image we need to convert it to a string first
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		if(qrCodeLido != barcodeData):
			qrCodeLido = barcodeData
			#aqui eu vou mandar a requisicao pra API
			piscaFracasso()
			print(barcodeData)

		# if the barcode text is currently not in our CSV file, write
		# the timestamp + barcode to disk and update the set
		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# close the output CSV file do a bit of cleanup
print("[RASPBERRY] Encerrando servico")
csv.close()
cv2.destroyAllWindows()
vs.stop()
