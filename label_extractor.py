import glob
import os
import pickle
import re
from bs4 import BeautifulSoup
import mutagen
import requests
from mutagen.easyid3 import EasyID3
from tqdm import tqdm


# endings = [".mp3", ".m4a", ".flac", ".wav", ".wma", ".opus", ".ogg", ".wv"]
#
# path = "P:\\Music\\Music"
# counter = 0
# ignored = set()
# for file in glob.glob(path + "\\**\\*", recursive=True):
#     if not os.path.isfile(file):
#         continue
#     if os.path.splitext(file)[1] in endings:
#         counter += 1
#     else:
#         ignored.add(os.path.splitext(file)[1])
# print(counter)
# print(ignored)


def genre_from_file(path):
    try:
        tag = mutagen.File(path, easy=True)
        genre = tag.get('genre')[0]
    except:
        return None
    return genre


def mood_from_file(path):
    try:
        tag = mutagen.File(path, easy=True)
        mood = tag.get('mood')[0]
    except:
        return None
    return mood


def copy_unsynced_lyrics_to_lyrics(path):
    mp3_files = [file for file in os.listdir(path) if file.endswith('.mp3')]

    for file in mp3_files:
        mp3_path = os.path.join(path, file)

        try:
            tag = mutagen.File(mp3_path, easy=True)
            print(tag.keys())
        except:
            return

        # try:
        #     audio = EasyID3(mp3_path)
        #     print(audio.keys())
        #     if 'unsynced lyrics' in audio.keys():
        #         lyrics = audio['unsyncedlyrics'][0]
        #         audio['lyrics'] = lyrics
        #         audio.save()
        #         print(f'Lyrics copied for {file}')
        #     else:
        #         print(f'No "unsynced lyrics" tag found for {file}')
        # except Exception as e:
        #     print(f'Error processing {file}: {e}')


def all_audio_files():
    extension_dict = {'.mp3': 0, '.flac': 0, '.m4a': 0, '.ogg': 0, '.wav': 0, '.wma': 0}
    extension_dict_count = {'.mp3': 0, '.flac': 0, '.m4a': 0, '.ogg': 0, '.wav': 0, '.wma': 0}
    count = 0
    all_extensions = set()
    all_files = []
    for artist in glob.glob("P:/Music/Music/*"):
        if not os.path.isdir(artist):
            continue
        for album in glob.glob(artist + "/**/*", recursive=True):
            if not os.path.isfile(album):
                continue
            extension = os.path.splitext(album)[1]
            all_extensions.add(extension)
            if extension not in extension_dict.keys():
                continue
            extension_dict[extension] = extension_dict[extension] + os.path.getsize(album)
            extension_dict_count[extension] = extension_dict_count[extension] + 1
            all_files.append(album)
            count+=1
    print(all_extensions)
    print(f"{count} files in total")
    return extension_dict, extension_dict_count, all_files


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'B'


def get_audio_title(path):
    try:
        tag = mutagen.File(path, easy=True)
        title = tag.get('title')[0]
        if tag.get('mood') is not None:
            print(path)
    except:
        print(path)
        return None
    return title


def sort_dict(dictionary: dict):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}


def go_through_all_files():
    extension_dict = {'.mp3': 0, '.flac': 0, '.m4a': 0, '.ogg': 0, '.wav': 0, '.wma': 0}#
    genre_dict = {}
    no_genres = set()
    count = 0
    all = 0
    for artist in tqdm(glob.glob("P:/Music/Music/*")):
        if not os.path.isdir(artist):
            continue
        for album in glob.glob(artist + "/**/*", recursive=True):
            if not os.path.isfile(album):
                continue
            extension = os.path.splitext(album)[1]
            if extension not in extension_dict.keys():
                continue
            genre = genre_from_file(album)
            try:
                genre_dict[genre] = genre_dict.get(genre) + [album]
                if genre is not None:
                    all += 1
                else:
                    no_genres.add(os.path.split(album)[0])
            except:
                genre_dict[genre] = [album]
    print("Skipped: ", count, "Genre found: ", all)
    print("No genre: ", no_genres)
    pickle.dump(no_genres, open("no_genres.pkl", "wb"))
    return genre_dict


def split_gernes(file, split=","):
    genres = pickle.load(open(file, "rb"))
    split_genres = {}
    for genre in genres.keys():
        if genre is None:
            continue
        split_genre = genre.split(split)
        if len(split_genre) > 1:
            for g in split_genre:
                # if label already exists, don't overwrite it
                if g.strip() in split_genres.keys():
                    split_genres[g.strip()] = split_genres[g.strip()] + genres[genre]
                else:
                    split_genres[g.strip()] = genres[genre]
        else:
            split_genres[genre] = genres[genre]
    return split_genres


if __name__ == "__main__":
    genres = go_through_all_files()
    pickle.dump(genres, open("genres.pkl", "wb"))

    genres = split_gernes("genres.pkl")

    pickle.dump(genres, open("split_genres.pkl", "wb"))
    print(genres.keys())
    features = pickle.load(open("features.pkl", "rb"))
    print(features[:5])