# CelebrityImageScraper

Hackathon project that can be used to recognize celebrity faces against a database of 5000 celebrities scraped from IMDB.

Uses github user ageitgey's face_recognition API which exposes a pre-trained Neural Network that creates a numerical matrix representation 
of input faces. New faces can be fed into the Neural Network and compared to our database of existing faces, classified by the Euclidian
distance of the matrix representations.

This is the python and API portion of the project that I worked on, see https://github.com/jaybooth4/HuskyHacks2017 for the full project.
