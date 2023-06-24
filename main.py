# for making gui

# could add 1. timer 2. say the song title after u guess it 3. give up button 4. choose song?

# ok why are there so many songs where they have weird spaces how am i supposed to catch them sob
# might want to just say if its not any of these characters (alphabet + .,?!():'") maybe
# cant scroll with two fingers on mac, seems to be a tkinter thing
# sometimes you might manage to type "in" before "i" and yes, the system is just not fast enough ig
# add a button for rules

import tkinter as tk
from tkinter import ttk
import random
import functionality
from PIL import ImageTk, Image

albums = [
    "taylor_swift", "fearless", "speak_now", "red", "1989",
    "reputation", "lover", "folklore", "evermore", "midnights"
]
colors = [
    "#edf7f3", "#c49d27", "#8a14c9", "#a30b25", "#0099f2",
    "black", "#f7e4f5", "#cfc8be", "#dec9a4", "#0a0647"
]
FONT = "Lao MN"
text_font = (FONT, 15)


song_list = []
for album in albums:
    with open(f"songs_list/{album}.txt", "r") as file:
        for song in file:
            song_list.append(song.strip())

random.shuffle(song_list)


def modify_text(word):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    ans = ""
    for char in word.lower():
        if char in lowercase:
            ans += char
    return ans


def win():
    """
    flash a congrats sign and prompts continue
    """
    text_entry.place_forget()
    lyrics_canvas.place_forget()
    scrollbar.pack_forget()
    if len(song_list) == 0:
        title.config(text="Congrats...? You finished all of them...\n Now please go touch some grass...")
        title.place(x=300, y=300, width=600, height=200)
        return
    congrats.place(x=300, y=140)
    start_button.place(x=450, y=640, width=300, height=100)
    start_button.config(text="Play Again?")


def text_entered(event, tree, lyrics, labels, words_left):
    """
    when we've detected that text has been entered
    :return:
    """
    text = modify_text(text_entry.get())
    node = tree[text]
    if node is None:
        return
    text_entry.delete(0, tk.END)
    indices = node.get_indicies()
    for i in indices:
        words_left[0] -= 1
        labels[i].config(text=lyrics[i])
    tree.remove(text)
    print(text + " has been removed")
    print([i.get_word() for i in tree])
    if words_left[0] == 0:
        win()
    else:
        return


def start_game():
    """
    gets song, creates boxes, tree
    """
    start_button.place_forget()
    congrats.place_forget()
    text_entry.place(x=450, y=125, width=300, height=30)
    text_entry.focus_set()
    cur_song = song_list.pop()
    # print(cur_song)
    lyrics = functionality.get_lyrics(cur_song)
    lyrics_canvas.place(x=150, y=200, width=900, height=550)
    lyrics_canvas.configure(highlightbackground=colors[4])
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollable_frame = tk.Frame(lyrics_canvas)
    scrollable_frame.configure(
        background=colors[6]
    )
    lyrics_canvas.create_window((0, 30), window=scrollable_frame, anchor=tk.NW)
    for i in range(4):
        scrollable_frame.columnconfigure(i, minsize=221)
    num_of_words = len(lyrics)
    words_left = [num_of_words]
    num_rows = (num_of_words + 3) // 4
    lyrics_labels = []
    for i in range(num_of_words):
        label = tk.Label(
            scrollable_frame,
            background=colors[0],
            foreground=colors[1],
            width=20
        )
        # label.configure()
        # label.place(x=0, y=(10*i))
        label.grid(row=i%num_rows, column=i//num_rows, padx=0, pady=5)
        lyrics_labels.append(label)
    scrollable_frame.update_idletasks() # bruh i was missing this line thats why the scroll bar didnt show
    lyrics_canvas.configure(yscrollcommand=scrollbar.set, scrollregion=lyrics_canvas.bbox("all"))
    # has to go after i put in labels for some reason

    tree = functionality.Tree()
    tree.populate(functionality.modified_lyrics(lyrics))

    text_entry.bind("<KeyRelease>", lambda event: text_entered(event, tree, lyrics, lyrics_labels, words_left))


window = tk.Tk()
window.geometry("1200x800")
window.configure(background=colors[7])
window.title("")

title = tk.Label(window, text="Guess the Taylor Swift Song Lyrics!")
title.place(x=300, y=30, width=600, height=80)
title.config(
    font=(FONT, 30),
    highlightthickness=0,
    background=colors[7],
    foreground=colors[9]
)

start_button = tk.Button(window, text="START")
start_button.config(
    font=(FONT, 30),
    highlightbackground=colors[3],
    fg=colors[3],
    command=start_game
)
start_button.place(x=500, y=375, width=200, height=100)

text_entry = tk.Entry(window)
text_entry.config(
    font=(FONT, 15),
    foreground=colors[2],
    background=colors[8],
    highlightbackground=colors[3]
)

image = Image.open("congrats.jpg") # 600 x 450
# image = image.resize((200, 200))  # Resize the image if needed
photo = ImageTk.PhotoImage(image)
congrats = tk.Label(window, image=photo)

# for i in font.families():
#     print(i)

lyrics_canvas = tk.Canvas(window)
scrollbar = ttk.Scrollbar(
    lyrics_canvas,
    orient=tk.VERTICAL,
    command=lyrics_canvas.yview,
    style="Vertical.TScrollbar"
)


window.mainloop()
