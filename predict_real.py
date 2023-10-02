import glob
import os
import pickle
import sys

from dataset_preparation import get_features

no_genres = pickle.load(open("no_genres.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
features = get_features("features_ext.pkl")


for path in no_genres:
    predictions = []
    for file in glob.glob(path + "/*", recursive=True):
        if not os.path.isfile(file):
            continue
        if file not in features.keys():
            continue
        predictions.append(model.predict([features[file]])[0])
    if len(predictions) > 0:
        print(f"{max(predictions, key=predictions.count):12}{os.path.basename(path)}")
