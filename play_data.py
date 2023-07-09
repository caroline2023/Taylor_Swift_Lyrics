# every time i play, time it takes to guess song, time it takes to complete song, song
# if incomplete, percentage of lyrics?

import pandas as pd
import song_mappings
import os


def add_row(song):
    """
    adds row to csv
    """
    # check if file exists, if it doesnt, create csv, else read data and add in
    file_path = 'game_data.csv'
    if not os.path.exists(file_path):
        data = {
            "Game #": [0],
            "Song": [song_mappings.song_dict[song]],
            "Guess time": [pd.NA],
            "Play time": [pd.NA]
        }
        df = pd.DataFrame(data)
        df.to_csv('game_data.csv', index=False)
        return
    df = pd.read_csv('game_data.csv')
    n = len(df)
    new_row = [n, song_mappings.song_dict[song], pd.NA, pd.NA]
    df.loc[n] = new_row
    df.to_csv("game_data.csv", index=False)


def guess(time):
    df = pd.read_csv('game_data.csv')
    n = len(df) - 1
    df.at[n, "Guess time"] = time
    df.to_csv("game_data.csv", index=False)


def finish(time):
    df = pd.read_csv('game_data.csv')
    n = len(df) - 1
    df.at[n, "Play time"] = time
    df.to_csv("game_data.csv", index=False)

