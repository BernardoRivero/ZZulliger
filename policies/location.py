import cv2
import imutils
import numpy as np
import os
import google_drive_api as drive
import correlation

class Location():
    def __init__(self):
        self._location = [[],[],[]]

    def process_response_location(self, user_name, responses_lamina1, responses_lamina2, responses_lamina3):
        drive.download_files(user_name)

        for lamina in range(1,4):
            if lamina == 1: limit = len(responses_lamina1)
            elif lamina == 2: limit = len(responses_lamina2)
            else: limit = len(responses_lamina3)

            for i in range(1, limit):
                marked_image = cv2.imread(user_name + "_" + lamina + "_" + i + ".png")
                cuts = self.cut_contour(marked_image, './files/images/lamina' + lamina)

                for cutout in cuts: 
                    pass
                    # recorrer imagenes globales y comparar,
                    # si es global corto, localizacion = 'W'
                    # si no ver respuesta y comparar con rtas usuales
                    # si matchea con una corto localizacion = 'D'
                    # sino es inusual. localizacion = 'Dd'

                    # recorrer imagenes con blanco
                    # si hay blanco agrego 'S' a la localización

                self._location[lamina-1][i-1]  
                os.remove(user_name + "_" + lamina + "_" + i + ".png")

        
    def cut_contour(self, image, path):
        
        original = cv2.imread(path + "/original.png")

        image_grayscale = self.convert_image_to_grayscale(image)

        width = int(image_grayscale.shape[1])
        height = int(image_grayscale.shape[0])
        dim = (width, height)
        original = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)    

        # Convert from BGR to HSV color space
        hsv = cv2.cvtColor(image_grayscale, cv2.COLOR_BGR2HSV)

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

    def convert_image_to_grayscale(self, image):
        # Read image
        #image = cv2.imread(image_src)
        image = imutils.resize(image, width=640)

        # BGR images are converted to: GRAY and HSV
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageGray = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)
        imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        light_blue = np.array([110,50,50])
        dark_blue = np.array([130,255,255])

        # Detect the blue color
        mask = cv2.inRange(imageHSV, light_blue, dark_blue)
        blueDetected = cv2.bitwise_and(image,image, mask= mask)

        # Background in grays
        invMask = cv2.bitwise_not(mask)
        bgGray = cv2.bitwise_and(imageGray,imageGray,mask=invMask)

        # Add bgGray y blueDetected
        finalImage = cv2.add(bgGray,blueDetected)

        # Return the final image
        return finalImage

   
    






