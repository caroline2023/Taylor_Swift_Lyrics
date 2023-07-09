# make tables

# each time i play, first 20 words i guess, their frequencies, time it takes to complete

import pandas as pd
import song_mappings
import functionality

data = {
    "Word": [],
    "Total": []
}
# each key in dict is a song title, corresponds to columns

df = pd.DataFrame(data)

word_indices = {}

for song, title in song_mappings.song_dict.items():
    # you get warnings that dataframe is very fragmented,
    # should be fine since i ended up making a copy?
    n = len(word_indices)
    df[title] = [0] * n
    tree = functionality.lyric_tree(song)
    for word_node in tree:
        word = word_node.get_word()
        num = len(word_node.get_indices())
        if word in word_indices:
            df.at[word_indices[word], title] = num
            df.at[word_indices[word], "Total"] += num
        else:
            new_row = [word, num]
            for _ in range(len(df.columns) - 2):
                new_row.append(0)
            new_row[-1] = num
            df.loc[n] = new_row
            word_indices[word] = n
            n += 1

df = df.copy()
df = df.sort_values("Total", ascending=False)
df.to_csv('song_lyrics.csv', index=False)
