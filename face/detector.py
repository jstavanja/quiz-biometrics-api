# Inspired by Brandon Amos's demo of comparison of pictures from the openface library
#
# Authors: Jaka Stavanja

import argparse
import os
# import openface
# import cv2
import numpy as np

class Detector():

  def __init__(self, base_image, new_image):
    '''
    base_image => the one, that is the correct face image of the person that owns an account
    new_image => the picture, which we need to compare to the base image, so that we can compute a distance between faces
    '''
    self.base_image = base_image
    self.new_image = new_image

    '''
    Paths needed to find the necessary model and the image size (precision) definition
    '''
    self.model_directory = os.path.realpath('/root/openface/models')
    self.openface_model_directory = os.path.join(self.model_directory, 'openface')
    self.dlib_model_directory = os.path.join(self.model_directory, 'dlib')
    self.dlib_face_predictor = os.path.join(self.dlib_model_directory, "shape_predictor_68_face_landmarks.dat")
    self.network_model = os.path.join(self.openface_model_directory, 'nn4.small2.v1.t7')
    self.image_size_px = 96

    '''
    Setup of the openface functionalities needed to fetch representations of faces on pictures
    '''
    self.aligner = openface.AlignDlib(self.dlib_face_predictor)
    self.network = openface.TorchNeuralNet(self.network_model, self.image_size_px)


  '''
  Function returns a representation of a face found on the image with path image_path
  '''
  def get_face_representation(image_path):
    # read images into cv2
    image = cv2.imread(image_path)

    if image is None:
      raise Exception("Cannot read image. Image path: " + image_path)

    # convert to rgb
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # get the bounding box for the biggest face, detected on the picture
    rgb_face_bounding_box = self.aligner.getLargestFaceBoundingBox(image_rgb)
    if rgb_face_bounding_box is None:
      raise Exception("Cannot find a face in the image. Image path: " + image_path)

    # align face on the image
    aligned_face = self.aligner.align(image_size_px, image_rgb, rgb_face_bounding_box, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if aligned_face is None:
      raise Exception("Cannot align the face in the image. Image path: " + image_path)

    # get repr
    return self.network.forward(aligned_face)

    def get_distance(self):
      '''
      Calculation of the difference
      '''
      # get representations for both pictures
      repr_base = get_face_representation(self.base_image)
      repr_new = get_face_representation(self.new_image)

      # get distance
      distance = repr_new - repr_base

      # get the squared dot product and get rid of negatives
      dot = np.dot(distance, distance)

      # print distance
      return dot


