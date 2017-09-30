import face_recognition
import time
import os
import json
from pathlib import Path
import numpy as np
import math


def recipSum(scores):
    return sum(list(map(lambda val: math.exp(1.0/val), scores)))

def softmax(score, denom):
    return math.exp(1.0/score)/denom

# current_milli_time = lambda: int(round(time.time() * 1000)) # Function to calculate the time
# start = current_milli_time()

known_face_dictionary = {}
cache = Path("cache.txt")  # Load from cache if it's there
if cache.exists():
    with open('cache.txt') as file:
        data = json.load(file)
        known_face_dictionary = dict(map(lambda item: (item[0], np.array(item[1])), data.items()))
        # print("Loaded from cache")

badPics = open('badPics.txt', 'w+')

known_pictures_dir = "known_pictures"
if not known_face_dictionary: # if empty
    for filename in os.listdir(known_pictures_dir):
        # print(known_pictures_dir + "/" + filename)
        if filename[:1] == "." :  # For .DS_Store
            continue
        face_name = filename.replace(".jpg", "")
        face_image = face_recognition.load_image_file(known_pictures_dir + "/" + filename)
        try:
            known_face_dictionary[face_name] = face_recognition.face_encodings(face_image)[0] # Only get the first face
        except Exception as e:
            print (e)
            badPics.write(face_name + "\n")
            badPics.flush()

unknown_pictures_dir = "unknown_pictures"
unknown_face_dictionary = {}
for filename in os.listdir(unknown_pictures_dir):
    unknown_face_name = filename.replace(".jpg", "")
    unknown_face_image = face_recognition.load_image_file(unknown_pictures_dir + "/" + filename)
    unknown_face_dictionary[unknown_face_name] = face_recognition.face_encodings(unknown_face_image)[0]


#Check unknown faces
known_face_encodings = list(known_face_dictionary.values())
known_face_names = list(known_face_dictionary.keys())

for unknown_face in unknown_face_dictionary.keys():
    unknown_face_encoding = unknown_face_dictionary[unknown_face]
    results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
    results_distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)
    positive_result_indicies = [k for k,v in enumerate(results) if v == True]
    recip_sum = recipSum([results_distances[index] for index in positive_result_indicies])
    normed_res = {}
    for index in positive_result_indicies:
        normed_res[known_face_names[index]]=softmax(results_distances[index], recip_sum)

    if normed_res:
        print(json.dumps(normed_res))


# Write to cache
with open('cache.txt', 'w') as file:
    file.write(json.dumps(dict(map(lambda item: (item[0], item[1].tolist()), known_face_dictionary.items()))))
