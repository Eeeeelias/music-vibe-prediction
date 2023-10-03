import pickle
import sys

import numpy as np


def get_labels(file):
    raw = pickle.load(open(file, "rb"))
    label_dict = {}
    for genre in raw:
        for song in raw[genre]:
            label_dict[song] = genre
    print(f"Got {len(label_dict.keys())} labels")
    return label_dict


def get_features(file):
    raw = pickle.load(open(file, "rb"))
    feature_dict = {}
    for song in raw:
        feature_dict[song[0]] = np.array(song[1]).flatten()
    print(f"Got {len(feature_dict.keys())} features")
    return feature_dict


def make_data_sheets():
    features = get_features("features_all.pkl")
    labels = get_labels("split_genres.pkl")

    feature_sheet = []
    label_sheet = []
    for n, label in enumerate(labels.keys()):
        f_row = [n, features[label]]
        l_row = [n, label, labels[label]]

        feature_sheet.append(f_row)
        label_sheet.append(l_row)

    # write both sheets to a tsv file
    with open("features.tsv", "w", encoding='utf-8') as f:
        for row in feature_sheet:
            f.write("\t".join([str(x) for x in row]) + "\n")

    try:
        with open("labels.tsv", "w", encoding='utf-8') as f:
            for row in label_sheet:
                f.write("\t".join([str(x) for x in row]) + "\n")
    except:
        print(row)
        sys.exit(1)


if __name__ == '__main__':
    make_data_sheets()