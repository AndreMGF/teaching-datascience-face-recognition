import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import face_recognition
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import os
import datetime
import glob
import json

app = Flask(__name__)
CORS(app)

# Carregar dados de reconhecimento de faces
#print('Carregando o modelo')
#model = pickle.load(open('model.pkl','rb'))



# Convert Base64 to Image
def convertBase64ToPILImage(base64Data):
    buff = BytesIO(base64.b64decode(base64Data))
    return Image.open(buff)

def convertBase64ToFaceRecognitionImage(base64Image):
	'''
	This function convert an image in base64 format
	in a face recognition image
	'''
	buff = BytesIO(base64.b64decode(base64Image))
	return face_recognition.load_image_file(buff)

def removeBase64HTMLStringPrefix(base64HTMLString):
	'''

	'''	
	return base64HTMLString.decode().split(',')[1]

def converBase64StringToBase64(base64String):
	'''
	
	'''
	return base64String.encode();

def prepareImage(request_data):
	'''
	
	'''	
	x = removeBase64HTMLStringPrefix(request_data)
	x = converBase64StringToBase64(x)
	return x 

def drawFaces(image, faceLocations):
	'''
	
	'''
	pil_image = Image.fromarray(image)
	draw = ImageDraw.Draw(pil_image)
	for (top, right, bottom, left) in faceLocations:
		draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
	del draw
	return pil_image;

def cropFace(image, faceLocation):
	'''
	
	'''
	pil_image = Image.fromarray(image)
	top, right, bottom, left = faceLocation
	return pil_image.crop(( left, top, right, bottom ))

def convertImageToBase64String(image):
	'''
	
	'''	
	buff = BytesIO()
	image.save(buff, format="PNG")
	img_str = base64.b64encode(buff.getvalue())
	return img_str

def saveImage(image, filepath):	
	with open(filepath, "wb") as fh:
		fh.write(base64.decodebytes(image))

def loadImages():
	from pathlib import Path
	filenames = [] 
	encodings = []	
	for filename in Path('images').glob('**/faceimg_*.png'):		
		x = face_recognition.load_image_file(filename)
		x = face_recognition.face_encodings(x)
		filenames.append(filename)
		encodings.append(x[0])	
	return filenames, encodings	

def saveInfo(info, filepath):
	with open(filepath, 'w') as outfile:
		json.dump(info, outfile)

def loadInfo(filepath):
	with open(filepath, 'r') as outfile:
		return json.load(outfile)

filenames, all_encodings = loadImages()

@app.route('/facedetection', methods=['POST'])
def facedetection():

	print('Recebendo os dados via POST')

	image = prepareImage(request.data);

	face_recognition_image = convertBase64ToFaceRecognitionImage(image)

	face_locations = face_recognition.face_locations(face_recognition_image)

	image_with_faces = drawFaces(face_recognition_image, face_locations)

	image_with_faces_str = convertImageToBase64String(image_with_faces);

	return image_with_faces_str

@app.route('/getname', methods=['POST'])
def getname():

	print('Recebendo os dados via POST')

	image = prepareImage(request.data);

	face_recognition_image = convertBase64ToFaceRecognitionImage(image)

	face_locations = face_recognition.face_locations(face_recognition_image)
	#print(face_locations)
	face_encodings = face_recognition.face_encodings(face_recognition_image, face_locations)

	results = face_recognition.compare_faces(all_encodings,face_encodings[0])

	print([filenames[i] for i in range(len(filenames)) if results[i] ])
 


	image_face = cropFace(face_recognition_image, face_locations[0])

	image_face_str = convertImageToBase64String(image_face)

	return image_face_str


@app.route('/facecrop', methods=['POST'])
def facecrop():

	print('Recebendo os dados via POST')

	image = prepareImage(request.data);

	face_recognition_image = convertBase64ToFaceRecognitionImage(image)

	face_locations = face_recognition.face_locations(face_recognition_image)
	
	#face_encodings = face_recognition.face_encodings(image, face_locations)

	#print(face_recognition.compare_faces(face_encodings,face_encodings[1] ))

	image_face = cropFace(image, face_locations[0])

	image_face_str = convertImageToBase64String(image_face)

	return image_face_str


@app.route('/createface', methods=['POST'])
def createface():

	print('Recebendo os dados via POST')
	data = request.get_json(force=True)	
	form_name = data['name']
	form_img = data['img']

	base64Image = prepareImage(form_img.encode());
			
	dirpath = 'images/' + form_name 
	try:
		os.mkdir(dirpath)
	except:		
		print('Diretório já existente')

	filename = '/img_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
	filepath = dirpath + filename
	saveImage(base64Image, filepath)

	face_recognition_image = convertBase64ToFaceRecognitionImage(base64Image)
	
	face_locations = face_recognition.face_locations(face_recognition_image)	
	
	image_face = cropFace(face_recognition_image, face_locations[0])
		
	image_face_str = convertImageToBase64String(image_face)
	
	#base64ImageFace = converBase64StringToBase64(image_face_str)
	
	filename = '/faceimg_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
	filepath = dirpath + filename
	saveImage(image_face_str, filepath)

	output = jsonify(0)
	return output
	

@app.route('/person/add', methods=['POST'])
def person_add():

	print('Recebendo os dados via POST')
	data = request.get_json(force=True)	

	form_info = data['info']
	print(form_info)
	form_name = form_info['nome']
	form_img = data['img']

	base64Image = prepareImage(form_img.encode());
			
	dirpath = 'images/' + form_name 
	try:
		os.mkdir(dirpath)
	except:		
		print('Diretório já existente')

	filename = '/img_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
	filepath = dirpath + filename
	saveImage(base64Image, filepath)

	face_recognition_image = convertBase64ToFaceRecognitionImage(base64Image)
	
	face_locations = face_recognition.face_locations(face_recognition_image)	
	
	image_face = cropFace(face_recognition_image, face_locations[0])
		
	image_face_str = convertImageToBase64String(image_face)
		
	filename = '/faceimg_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
	filepath = dirpath + filename
	saveImage(image_face_str, filepath)

	filepath = dirpath + "/info.json"
	saveInfo(form_info, filepath)

	output = jsonify(0)
	return output
    
@app.route('/recognize', methods=['POST'])
def recognize():

	print('Recebendo os dados via POST')

	data = request.get_json(force=True)	
	form_img = data['img']

	base64Image = prepareImage(form_img.encode());

	face_recognition_image = convertBase64ToFaceRecognitionImage(base64Image)

	face_locations = face_recognition.face_locations(face_recognition_image)

	if (len(face_locations) == 0):
		return jsonify({
			'result' : 'error',
			'msg' : 'Não foi encontrada nenhuma face na imagem'
			});

	if (len(face_locations) > 1):
		return jsonify({
			'result' : 'error',
			'msg' : 'Foram encontradas mais do que uma face na imagem'
			});

	face_encodings = face_recognition.face_encodings(face_recognition_image, face_locations)

	faces_comparison = face_recognition.compare_faces(all_encodings,face_encodings[0])

	filenames_true = [filenames[i] for i in range(len(filenames)) if faces_comparison[i] ]
	dirnames_true = [os.path.dirname(filename) for filename in filenames_true]
	print('dirnames_true', dirnames_true)
	print('dirnames_true set', set(dirnames_true) )
	persons = set(dirnames_true)

	if (len(persons) == 0) :
		return jsonify({
			'result' : 'error',
			'msg' : 'O rosto encontrado não foi encontrado na base de dados'
			});

	if (len(persons) > 1):
		return jsonify({
			'result' : 'error',
			'msg' : 'Foram encontradas mais do que uma face parecida para esse rosto'
			});

	dirpath = dirnames_true[0]
	filepath = dirpath + "/info.json"
		
	info = loadInfo(filepath)

	return jsonify({
		'result' : 'success',
		'info' : info
		})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
