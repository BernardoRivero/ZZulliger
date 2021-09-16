import cv2
import imutils
import numpy as np
import os
from google_drive_api import *
from correlation import *

class Location():
    def __init__(self):
        self._location = [[],[],[]]

        # respuestas usuales:
        self._usual_lamina1 = []
        self._image_usual_lamina1 = []
        
        usual_lamina2_1 = ["dos animales"]
        usual_lamina2_2 = ["vegetacion", "algas", "ojos verdes"]
        usual_lamina2_3 = ["fuego", "animal", "cerebro"]
        usual_lamina2_4 = ["fuego en un bosque", "bosque", "animal entre vegetacion", "selva", "ecosistema"]
        usual_lamina2_5 = ["totem", "columna", "templo"]
        self._usual_lamina2 = [usual_lamina2_1, usual_lamina2_2, usual_lamina2_3, usual_lamina2_4, usual_lamina2_5]
        self._image_usual_lamina2 = [['usual_1_1.png'],['usual_2_1.png','usual_2_2.png'],['usual_3_1.png'],['usual_4_1.png'],['usual_5_1.png']]

        usual_lamina3_1 = ["fuego", "mariposa", "fogata"]
        usual_lamina3_2 = ["duendes", "enanos", "gnomos", "indios", "aborigenes", "muñecos"]
        self._usual_lamina3 = [usual_lamina3_1, usual_lamina3_2]
        self._image_usual_lamina3 = [['usual_1_1.png'],['usual_2_1.png','usual_2_2.png']]


    def process_response_location(self, user_name, responses, lamina):
        print('En process_response_location')
        download_files(user_name + "_" + str(lamina))

        for i in range(1, len(responses)+1):
            print('Respuesta del usuario: ' + responses[i-1])
            marked_image = cv2.imread(user_name + "_" + str(lamina) + "_" + str(i) + ".png")
            cuts = self.cut_contour(marked_image, './files/images/lamina' + str(lamina))
            print('Image: ' + user_name + "_" + str(lamina) + "_" + str(i) + ".png")
                
            # verifico si el recorte es global, el usuario marcó la imagen entera.
            if len(cuts) == 1:
                path_global = "./files/images/lamina"+str(lamina)+"/global/"
                files = os.listdir(path_global)
                for file in files:
                    img = cv2.imread(path_global + file)
                    print('Comparando con la imagen: ' + file)
                    print('correlacion global: ', calculate_correlation_coefficient(img, cuts[0]))

            # verifico si el recorte es de detalle usual
            path_usual = "./files/images/lamina"+str(lamina)+"/usual/"
            if lamina == 1: 
                usual = self._usual_lamina1
                usual_images = self._image_usual_lamina1
            elif lamina == 2: 
                usual = self._usual_lamina2
                usual_images = self._image_usual_lamina2
            else: 
                usual = self._usual_lamina3
                usual_images = self._image_usual_lamina3

            for index in range(len(usual)):
                for word in usual[index]:
                    # Si la respuesta del usuario es usual, verifico si lo que marco coincide con la zona usual.
                    if word in responses[i-1]:
                        print('Reconocio la palabra: ' + word)
                        images_file = usual_images[index]
                        for file in images_file:
                            img = cv2.imread(path_usual + file)
                            print('Comparando con la imagen: ' + file)
                            for cutout in cuts: 
                                print('correlacion usual: ', calculate_correlation_coefficient(img, cutout))

            # Verifico si el recorte tiene partes blancas
            path_white = "./files/images/blanco/"
            files = os.listdir(path_white)
            for file in files:
                img = cv2.imread(path_white + file)
                print('Comparando con la imagen: ' + file)
                for cutout in cuts:                    
                    print('correlacion blanco: ', calculate_correlation_coefficient(img, cutout))
            
            print('Deleting the image: ' + user_name + "_" + str(lamina) + "_" + str(i) + ".png")
            os.remove(user_name + "_" + str(lamina) + "_" + str(i)+ ".png")

        
    def cut_contour(self, image, path):    
        original = cv2.imread(path + "/original.png")
        #image_grayscale = self.convert_image_to_grayscale(image)

        width = int(image.shape[1])
        height = int(image.shape[0])
        dim = (width, height)
        original = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)    

        # Convert from BGR to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Get the saturation plane - all black/white/gray pixels are zero, and colored pixels are above zero.
        s = hsv[:, :, 1]

        # Apply threshold on s - use automatic threshold algorithm (use THRESH_OTSU).
        ret, thresh = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Find contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = imutils.grab_contours(contours) 

        cuts = []
        for c in contours:
            if cv2.contourArea(c) > 1500:  #  Ignore very small contours
                x, y, w, h = cv2.boundingRect(c)
                out = original[y:y+h, x:x+w, :].copy()
                cuts.append(out)
        return cuts

    # def convert_image_to_grayscale(self, image):
    #     image = imutils.resize(image, width=640)

    #     # BGR images are converted to: GRAY and HSV
    #     imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     imageGray = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)
    #     imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #     light_blue = np.array([110,50,50])
    #     dark_blue = np.array([130,255,255])

    #     # Detect the blue color
    #     mask = cv2.inRange(imageHSV, light_blue, dark_blue)
    #     blueDetected = cv2.bitwise_and(image,image, mask= mask)

    #     # Background in grays
    #     invMask = cv2.bitwise_not(mask)
    #     bgGray = cv2.bitwise_and(imageGray,imageGray,mask=invMask)

    #     # Add bgGray y blueDetected
    #     finalImage = cv2.add(bgGray,blueDetected)

    #     # Return the final image
    #     return finalImage
