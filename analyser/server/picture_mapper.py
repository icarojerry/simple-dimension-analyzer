from django.core.files import File 
from analyser.parameters.config import server
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from .models import Picture, MappedObject
import numpy as np
import argparse
import imutils
import cv2
import os

class PictureMapper:

	def midpoint(self, ptA, ptB):
		return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

	def process(self, picture : Picture):
		distance = picture.distance * 10
        
		densityA= 460.4 - 2.053 * float(distance) + 0.002865 * float(distance) ** 2
		densityB= 831.7 - 3.702 * float(distance) + 0.005146 * float(distance) ** 2

		image = cv2.imread('.' + server['dir_img'] + picture.file.name)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
		gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGBA )
		#gray = cv2.cvtColor(gray, cv2.COLOR_RGBA2BGR )
		#cv2.imshow("Image3", gray)
		#gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
		#cv2.imshow("Image4", gray)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)

		# perform edge detection, then perform a dilation + erosion to
		# close gaps in between object edges
		edged = cv2.Canny(gray, 50, 100)
		edged = cv2.dilate(edged, None, iterations=1)
		edged = cv2.erode(edged, None, iterations=1)

		# find contours in the edge map
		cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# sort the contours from left-to-right and initialize the
		# 'pixels per metric' calibration variable
		#pixelsPerMetric = None
		(cnts, _) = contours.sort_contours(cnts)

		mapped_objects = []
		# loop over the contours individually
		for c in range(len(cnts)):
			# if the contour is not sufficiently large, ignore it
			if cv2.contourArea(cnts[c]) < 100:
				continue

			# compute the rotated bounding box of the contour
			orig = image.copy()
			box = cv2.minAreaRect(cnts[c])
			box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
			box = np.array(box, dtype="int")

			# # order the points in the contour such that they appear
			# # in top-left, top-right, bottom-right, and bottom-left
			# # order, then draw the outline of the rotated bounding
			# # box
			box = perspective.order_points(box)
			cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

			# # loop over the original points and draw them
			for (x, y) in box:
				cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

			# # unpack the ordered bounding box, then compute the midpoint
			# # between the top-left and top-right coordinates, followed by
			# # the midpoint between bottom-left and bottom-right coordinates
			(tl, tr, br, bl) = box
			(tltrX, tltrY) = self.midpoint(tl, tr)
			(blbrX, blbrY) = self.midpoint(bl, br)

			# # compute the midpoint between the top-left and top-right points,
			# # followed by the midpoint between the top-righ and bottom-right
			(tlblX, tlblY) = self.midpoint(tl, bl)
			(trbrX, trbrY) = self.midpoint(tr, br)
			
			# # draw the midpoints on the image
			cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
			cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
			cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
			cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

			# # draw lines between the midpoints
			cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
				(255, 0, 255), 2)
			cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
				(255, 0, 255), 2)

			# # compute the Euclidean picture.distance between the midpoints
			dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
			dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

			# # if the pixels per metric has not been initialized, then
			# # compute it as the ratio of pixels to supplied metric
			# # (in this case, inches)
			# if pixelsPerMetric is None:
			# 	pixelsPerMetric = dB / pictureWidth
    
			print('distance- '+ str(float(distance)))
			# # compute the size of the object
			#densidadeVertical
			dimA = (dA/(densityA)/25.4)*48
			print('dimA- ' + str(dimA))
			print('densityA- ' + str(densityA))
			print('dA- ' + str(dA))

            #densidadeHorizontal
			dimB = (dB/(densityB)/25.4)*88
			print('dimB- ' + str(dimB))
			print('densityB- ' + str(densityB))
			print('dB- ' + str(dB))
			
			# # draw the object sizes on the image
			cv2.putText(orig, "{:.1f} inch".format(dimA),
				(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (255, 255, 255), 2)
			cv2.putText(orig, "{:.1f} inch".format(dimB),
				(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (255, 255, 255), 2)

			area = float(dimA) * float(dimB)
			cv2.putText(orig, "{:.2f} inch^2".format(area),
				(int(trbrX + 30), int(trbrY + 30)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (255, 255, 255), 2)

			cv2.putText(orig, "Object: " + str(c + 1),
				(int(tltrX - 30), int(tltrY - 30)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (255, 255, 255), 2)

			#
			mapped_object_path = '.' + server['dir_img'] + str(c) + '_' + os.path.basename(picture.file.name)
			mapped_object = MappedObject(file = File(cv2.imwrite(mapped_object_path, orig)), item_number = c, picture = picture, area = area)
			mapped_object.save()
			mapped_objects.append(mapped_object)

		return mapped_objects
