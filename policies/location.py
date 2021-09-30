import cv2
import imutils
import os
import numpy as np
import math
from google_drive_api import *

class LocationProcessor():
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
        self._image_usual_lamina2 = [['usual_1_1.png', 'usual_1_2.png', 'usual_1_3.png'],['usual_2_1.png','usual_2_2.png'],['usual_3_1.png'],['usual_4_1.png'],['usual_5_1.png']]

        usual_lamina3_1 = ["fuego", "mariposa", "fogata"]
        usual_lamina3_2 = ["duendes", "enanos", "gnomos", "indios", "aborigenes", "muñecos"]
        usual_lamina3_3 = ["personas", "persona", "futbolistas", "futbolista"]
        self._usual_lamina3 = [usual_lamina3_1, usual_lamina3_2, usual_lamina3_3]
        self._image_usual_lamina3 = [['usual_1_1.png'],['usual_2_1.png','usual_2_2.png'], ['usual_3_1.png','usual_3_2.png']]


    # def process_response_location(self, user_name, responses):
    #     print('En process_response_location')
    #     download_files(user_name)

    #     for lamina in range(1, 4):           

    #         for i in range(1, len(responses[lamina-1])+1):
                                
    #             global_correlation = 0
    #             usual_correlation = 0
    #             location = ''

    #             print('Respuesta del usuario: ' + responses[lamina-1][i-1])
    #             marked_image = cv2.imread(user_name + "_" + str(lamina) + "_" + str(i) + ".png")
    #             cuts = self.cut_contour(marked_image, './files/images/lamina' + str(lamina))
    #             print('Image: ' + user_name + "_" + str(lamina) + "_" + str(i) + ".png")
                    
    #             if location == '':    
    #                 # verifico si el recorte es global, el usuario marcó la imagen entera.
    #                 if len(cuts) == 1:
    #                     path_global = "./files/images/lamina"+str(lamina)+"/global/"
    #                     files = os.listdir(path_global)
    #                     for file in files:
    #                         img = cv2.imread(path_global + file)
    #                         print('Comparando con la imagen: ' + path_global + file)
    #                         correlation = calculate_correlation_coefficient(img, cuts[0])
    #                         print('correlacion global: ', correlation)
    #                         if correlation > 0.7:
    #                             location = 'W'
    #                         else: global_correlation = max(global_correlation, correlation)

    #             if location == '':
    #                 # verifico si el recorte es de detalle usual
    #                 path_usual = "./files/images/lamina"+str(lamina)+"/usual/"
    #                 if lamina == 1: 
    #                     usual = self._usual_lamina1
    #                     usual_images = self._image_usual_lamina1
    #                 elif lamina == 2: 
    #                     usual = self._usual_lamina2
    #                     usual_images = self._image_usual_lamina2
    #                 else: 
    #                     usual = self._usual_lamina3
    #                     usual_images = self._image_usual_lamina3

    #                 for index in range(len(usual)):
    #                     for word in usual[index]:
    #                         # Si la respuesta del usuario es usual, verifico si lo que marco coincide con la zona usual.
    #                         if word in responses[lamina-1][i-1]:
    #                             print('Reconocio la palabra: ' + word)
    #                             images_file = usual_images[index]
    #                             for file in images_file:
    #                                 img = cv2.imread(path_usual + file)
    #                                 print('Comparando con la imagen: ' + path_usual + file)
    #                                 for cutout in cuts: 
    #                                     correlation = calculate_correlation_coefficient(img, cutout)
    #                                     print('correlacion usual: ', correlation)
    #                                     if correlation > 0.7:
    #                                         location = 'D'
    #                                         break
    #                                     else: usual_correlation = max(usual_correlation, correlation)
    #                                 if location != '': break
    #                         if location != '': break
                             
    #             if location == '':
    #                 if global_correlation > usual_correlation and global_correlation > 0.5:
    #                     location = 'W'
    #                 elif global_correlation < usual_correlation and usual_correlation > 0.5:
    #                     location = 'D'
    #                 else:
    #                     location = 'Dd' 
                
    #             # Verifico si tienen zonas blancas 
    #             n_white_pix = np.sum(marked_image == 255)
    #             if n_white_pix/marked_image.size > 0.8:
    #                 location = location + 'S'
                
    #             print('localización: ' + location)
    #             self._location[lamina-1].append(location)

    #             print('Deleting the image: ' + user_name + "_" + str(lamina) + "_" + str(i) + ".png")
    #             os.remove(user_name + "_" + str(lamina) + "_" + str(i)+ ".png")

    #     print(self._location)

    def process_response_location(self, user_name, response, lamina, response_number):
        print('En process response location')
        download_files(user_name + "_" + str(lamina) + "_" + str(response_number))
                                
        global_correlation = 0
        usual_correlation = 0
        location = ""

        print('Respuesta del usuario: ' + response)
        marked_image = cv2.imread(user_name + "_" + str(lamina) + "_" + str(response_number) + ".png")
        cuts = self.cut_contour(marked_image, './files/images/lamina' + str(lamina))
        print('Image: ' + user_name + "_" + str(lamina) + "_" + str(response_number) + ".png")
            
        if location == '':    
            # verifico si el recorte es global, el usuario marcó la imagen entera.
            if len(cuts) == 1:
                path_global = "./files/images/lamina"+str(lamina)+"/global/"
                files = os.listdir(path_global)
                for file in files:
                    img = cv2.imread(path_global + file)
                    print('Comparando con la imagen: ' + path_global + file)
                    correlation = self.calculate_correlation_coefficient(img, cuts[0])
                    print('correlacion global: ', correlation)
                    if correlation > 0.7:
                        location = 'W'
                    else: global_correlation = max(global_correlation, correlation)

        if location == '':
            # verifico si el recorte es de detalle usual
            area = ''
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
                    if word in response:
                        print('Reconocio la palabra: ' + word)
                        images_file = usual_images[index]
                        for file in images_file:
                            img = cv2.imread(path_usual + file)
                            print('Comparando con la imagen: ' + path_usual + file)
                            for cutout in cuts: 
                                correlation = self.calculate_correlation_coefficient(img, cutout)
                                print('correlacion usual: ', correlation)
                                if correlation > 0.7:
                                    location = 'D'+ str(index)
                                    break
                                else:
                                    if usual_correlation < correlation:
                                        usual_correlation = correlation
                                        area = str(index) 
                            if location != '': break
                    if location != '': break
                  
        if location == '':
            if global_correlation > usual_correlation and global_correlation > 0.5:
                location = 'W'
            elif global_correlation < usual_correlation and usual_correlation > 0.5:
                location = 'D'+area
            else:
                location = 'Dd' 
        
        # Verifico si tienen zonas blancas 
        for cutout in cuts:

            #img = cv2.imread(user_name + "_" + str(lamina) + "_" + str(response_number) + ".png", cv2.IMREAD_GRAYSCALE)
            # thresholding
            cutout = cv2.cvtColor(cutout, cv2.COLOR_RGB2GRAY)  
            ret,th = cv2.threshold(cutout,0,255,cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)
            # find number of white pixels
            white_pix = cv2.countNonZero(th)
            print('Porcentaje de blanco: ', white_pix/cutout.size)
            if white_pix/cutout.size > 0.8:
                location = location + 'S'
        
        print('Location: ' + location)

        print('Deleting the image: ' + user_name + "_" + str(lamina) + "_" + str(response_number) + ".png")
        os.remove(user_name + "_" + str(lamina) + "_" + str(response_number)+ ".png")

        return location

      
    def cut_contour(self, image, path):    
        original = cv2.imread(path + "/original.png")
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

    def media(self, x):
        rows = x.shape[0]
        columns = x.shape[1]
        sum = 0
        for row in x:
            for elem in row:
                sum += elem
        return float(sum) / (rows*columns)

    def standard_deviation(self, x):
        rows = x.shape[0]
        columns = x.shape[1]
        assert rows*columns > 0
        med_x = self.media(x)
        sum = 0
        for i in range(0,rows):
            for j in range(0,columns):
                sum += math.pow(x[i][j] - med_x, 2)
        return math.sqrt((sum/(rows*columns)))

    def covariance(self, x, y):
        rows_x = x.shape[0]
        columns_x = x.shape[1]
        assert rows_x*columns_x > 0
        med_x = self.media(x)
        med_y = self.media(y)
        sum = 0
        for i in range(0,rows_x):
            for j in range(0,columns_x):
                sum += ((x[i][j] - med_x)*(y[i][j] - med_y))
        return (sum/(rows_x*columns_x))

    def calculate_correlation_coefficient(self, imageA, imageB):
        if imageA.size > imageB.size:
            width = int(imageB.shape[1])
            height = int(imageB.shape[0])
            dim = (width, height)
            imageA = cv2.resize(imageA, dim, interpolation = cv2.INTER_AREA)
        else: 
            width = int(imageA.shape[1])
            height = int(imageA.shape[0])
            dim = (width, height)
            imageB = cv2.resize(imageB, dim, interpolation = cv2.INTER_AREA)

        # Extract red channel
        red_channel_im1 = imageA[:,:,2]
        red_channel_im2 = imageB[:,:,2]

        x = np.asarray(red_channel_im1)
        y = np.asarray(red_channel_im2)

        covariance_xy = self.covariance(x,y)
        deviation_x = self.standard_deviation(x)
        deviation_y = self.standard_deviation(y)
        return covariance_xy / (deviation_x * deviation_y)