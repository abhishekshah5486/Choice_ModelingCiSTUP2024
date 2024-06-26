# -*- coding: utf-8 -*-
"""ChoiceModeling_ProjectCiSTUP2024IISc.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QBnCnomRKderqHfTpdJPbTlcNyFuJtv7
"""

import numpy as np
import pandas as pd

# Parameters : Dictionary parameters containing the B(Beta) coefficients given
parameters = {
    'b_01' : 0.1,
    'b1' : -0.5,
    'b2' : -0.4,
    'b_02' : 1,
    'b_03' : 0,
    'bS1_13' : 0.33,
    'bS1_23' : 0.58
}
#
data = {
    'X1' : [2,1,3,4,2,1,8,7,3,2],
    'X2' : [8,7,4,1,4,7,2,2,3,1],
    'Sero': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'S1': [3,8,4,7,1,6,5,9,2,3],
    'AV1' : [1,1,1,1,1,0,0,1,1,0],
    'AV2' : [1,1,1,0,0,1,1,1,0,1],
    'AV3' : [1,1,0,0,1,1,1,1,1,1]
}

# Functions for deterministic utilities
def calc_V1(data, parameters):
  #V1 = β01 + β1*X1 + βS1,13*S1
  temp = parameters['b_01'] + (parameters['b1'] * np.array(data['X1']) )  + parameters['bS1_13'] * np.array(data['S1'])
  return temp

def calc_V2(data, parameters):
  #V2 = β02 + β2*X2 + βS1,23*S1
  temp = parameters['b_02'] + (parameters['b2'] * np.array(data['X2']) )  + parameters['bS1_23'] * np.array(data['S1'])
  return temp

def calc_V3(data, parameters):
  #V3 = β03 + β1*Sero + β2*Sero
  temp = parameters['b_03'] + (parameters['b1'] * np.array(data['Sero']) )  + parameters['b2'] * np.array(data['Sero'])
  return temp

# Utilities: A list of functions that define the deterministic utilities for each alternative based on
# the given parameters and data.
utilities = [calc_V1, calc_V2, calc_V3]

def calculate_probabilities(parameters, data, utilities):

  probabilities = {}
  # Caculating the exponent e^Vn for every utility using numpy(np.exp() function)
  # Storing the exponents of utilities (e^Vn) in another list exp_utilities
  exp_utilities = [];

  for utility_fn in utilities:
    exp_temp = np.exp(utility_fn(data, parameters))
    exp_utilities.append(exp_temp)

  #AV1 × exp(V1) + AV2 × exp(V2) + AV3 × exp(V3)
  p_denominator = 0
  for j in range(len(utilities)):
    p_denominator = p_denominator + (np.array(data[f'AV{j+1}']) * exp_utilities[j])

  for j in range(len(utilities)):
    temp_prob = (np.array(data[f'AV{j+1}']) * exp_utilities[j]) / p_denominator
    probabilities[f'P{j+1}'] = temp_prob

  return probabilities


# Saving the output of the function calculate_probabilities() in .txt file
def save_probabilities(probabilities, filename='probabilities.txt'):
  with open (filename, "w") as file:
    for key, value in probabilities.items():
      file.write(f'{key} : {value}\n')
      file.write("\n")

  file.close()

# Error Handling
try :
  probabilities = calculate_probabilities(parameters, data, utilities)
  save_probabilities(probabilities)
except (KeyError, ValueError, RuntimeError) as e:
    print("Error:", e)

