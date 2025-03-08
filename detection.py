
#importation de bibliothéque 
import cv2 
import os
import sqlite3 
import numpy as np
from PIL import Image
print(cv2.__version__)
print(dir(cv2.face))

from projectdetectionfaceID.settings import BASE_DIR


detector = cv2.CascadeClassifier(BASE_DIR+'/Face_Detection/haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()




import sqlite3

#Create a connection with databse
conn = sqlite3.connect('db.sqlite3')
if conn != 0:
    print("Connection Successful")
else:
    print('Connection Failed')
    exit()

# Creating table if it doesn't already exists
conn.execute('''create table if not exists facedata ( id int primary key, name char(20) not null)''')

class FaceRecognition:    

    def faceDetect(self, Entry1,):
        face_id = Entry1
        cam = cv2.VideoCapture(0)
        

        count = 0

        while(True):

            ret, img = cam.read()
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1

                #Enregistrez l'image capturée dans le dossier des ensembles de données
                cv2.imwrite(BASE_DIR+'/Face_Detection/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff # Appuyez sur « ESC » pour quitter la vidéo
            if k == 27:
                break
            elif count >= 30: # Prenez 30 échantillons de visage et arrêtez la vidéo
                break
    
    
        cam.release()
        cv2.destroyAllWindows()

    
    def trainFace(self):
        # Path for face image database
        path = BASE_DIR+'/Face_Detection/dataset'

        # function to get the images and label data
        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                img_numpy = np.array(PIL_img,'uint8')

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])
                print("face_id",face_id)
                faces = detector.detectMultiScale(img_numpy)

                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(face_id)

            return faceSamples,ids

        print ("\n Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.save(BASE_DIR+'/Face_Detection/trainer/trainer.yml') # reconnaître.save() a fonctionné sur Mac, mais pas sur Pi

        # Imprimer le nombre de visages entraînés et terminer le programme
        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))


    def recognizeFace(self):
        recognizer.read(BASE_DIR+'/Face_Detection/trainer/trainer.yml')
        cascadePath = BASE_DIR+'/Face_Detection/haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0
        cam = cv2.VideoCapture(0)

        #Définir la taille minimale de la fenêtre pour être reconnu comme un visage
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:

            ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                face_id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                #Vérifiez si la confiance est inférieure à 100 ==> "0" correspond parfaitement
                if (confidence < 100):
                    name = 'Detected'
                else:
                    name = "this face is unknoun"
                
                cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('Detect Face',img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            if confidence > 50:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()
        print(face_id)
        return face_id