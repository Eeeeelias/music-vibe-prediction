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


def combine_features(feature_dicts: list[dict]):
    # combine all feature dicts that are stored in a list into one dict
    combined = {}
    for key in feature_dicts[0].keys():
        combined[key] = np.array([x for f in feature_dicts for x in f[key]])
    return combined


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


def get_train_test_split(restict_to=None, input_features="features_ext.pkl", input_labels="split_genres.pkl"):
    features_raw = get_features(input_features)
    labels_raw = get_labels(input_labels, restrict_to=restict_to)

    # mfcc = get_features("features_ext.pkl")
    # chroma = get_features("features_chroma.pkl")

    # features_raw = combine_features([mfcc, chroma])

    features = []
    labels = []

    for i in labels_raw.keys():
        labels.append(labels_raw[i])
        features.append(features_raw[i])

    return train_test_split(features, labels, test_size=0.2, random_state=42, shuffle=True)


def get_most_prevalent_genres(n=6):
    genres = pickle.load(open("split_genres.pkl", "rb"))
    genre_count = {}
    for genre in genres.keys():
        genre_count[genre] = len(genres[genre])
    genre_count = {k: v for k, v in sorted(genre_count.items(), key=lambda item: item[1], reverse=True)}
    # print the first n genres as well as the number of songs associated with them
    for genre in list(genre_count.keys())[:n]:
        print(f"{genre}: {genre_count[genre]}", end=" ")
    return list(genre_count.keys())[:n]


if __name__ == '__main__':
    pass