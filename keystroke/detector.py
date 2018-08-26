import numpy as np
import pandas as pd
import json
import sys

# returns the average timing vector for a test (gets column means)
def sessionAverage(matrix):
  return np.mean(np.array(matrix), axis=0)

class Detector:

  def __init__(self, base_matrix, last_matrix):
    self.base_matrix = base_matrix
    self.last_matrix = last_matrix

  def get_euclidean_distance(self):

    if (len(self.base_matrix) == 0):
      return 'Not enough data'

    else:
      # compute column means for the previous test's means
      previousSessionsAvg = sessionAverage(self.base_matrix)

      # compute column means for the last (current) session's timing matrix
      lastSessionAvg = sessionAverage(self.last_matrix)

      percent_matches = [min(prev, last)/max(prev,last) for prev, last in zip(previousSessionsAvg, lastSessionAvg)]
      percent_total_match = (sum(percent_matches) / len(percent_matches)) * 100

      return percent_total_match
