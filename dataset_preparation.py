import pickle

import numpy as np
from sklearn.model_selection import train_test_split


def get_features(file):
    raw = pickle.load(open(file, "rb"))
    feature_dict = {}
    for song in raw:
        feature_dict[song[0]] = np.array(song[1]).flatten()
    print(f"Got {len(feature_dict.keys())} features")
    return feature_dict


def get_labels(file, restrict_to=None):
    raw = pickle.load(open(file, "rb"))
    label_dict = {}
    # restrict length of the majority class to be more in line with the rest of the classes
    classical_length = len(raw['Classical']) // 2
    for genre in raw:
        if genre == "None" or (restrict_to is not None and genre not in restrict_to):
            continue
        count = 0
        for song in raw[genre]:
            if genre == "Classical":
                count += 1
            if count > classical_length:
                continue
            label_dict[song] = genre
    print(f"Got {len(label_dict.keys())} labels")
    return label_dict


def get_train_test_split(restict_to=None):
    features_raw = get_features("features_ext.pkl")
    labels_raw = get_labels("split_genres.pkl", restrict_to=restict_to)

    features = []
    labels = []

    for i in labels_raw.keys():
        labels.append(labels_raw[i])
        features.append(features_raw[i])

    return train_test_split(features, labels, test_size=0.2, random_state=42, shuffle=True)


if __name__ == '__main__':
    # get the list of genres, sort them by count and display them
    genres = pickle.load(open("split_genres.pkl", "rb"))
    genre_count = {}
    for genre in genres.keys():
        genre_count[genre] = len(genres[genre])
    genre_count = {k: v for k, v in sorted(genre_count.items(), key=lambda item: item[1], reverse=True)}
    print(genre_count)
    print(genre_count['Rock'])