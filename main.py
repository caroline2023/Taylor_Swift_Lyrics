# for making gui

# could add 1. choose song?

# ok why are there so many songs where they have weird spaces how am i supposed to catch them sob
# not the russian e in fearless
# might want to just say if its not any of these characters (alphabet + .,?!():'") maybe
# cant scroll with two fingers on mac, seems to be a tkinter thing
# sometimes you might manage to type "in" before "i" and yes, the system is just not fast enough ig
# add in singles like only the young
# have rest of words that i didn't guess show up in red maybe
# number of words put in before i guessed?

import tkinter as tk
from tkinter import ttk
import random
import functionality
from PIL import ImageTk, Image
import song_mappings
import play_data
import time
# if i want a timer, could consider threading to allow for lots of things to happen at once

start_time = time.time()

albums = [
    "taylor_swift", "fearless", "speak_now", "red", "1989",
    "reputation", "lover", "folklore", "evermore", "midnights"
]
colors = [
    "#edfaf5", "#c49d27", "#8a14c9", "#a30b25", "#0099f2",
    "black", "#f7e4f5", "#cfc8be", "#dec9a4", "#160775"
]
FONT = "Lao MN"
text_font = (FONT, 15)

# write_to_data = False
# song_list = ["illicit-affairs", "our-song"]
# all-too-well-10-minute-version-taylors-version-from-the-vault

song_list = []
for album in albums:
    with open(f"songs_list/{album}.txt", "r") as file:
        for song in file:
            song_list.append(song.strip())

random.shuffle(song_list)
write_to_data = True


rules_text = ""
with open("rules.txt", "r") as file:
    for line in file:
        rules_text += line
# print(rules_text)


def rules_hover(event):
    """
    hovering over the question mark, will see that clicking it gives rules
    """
    rules.place(width=60)
    rules.config(text="Rules")


def rules_unhover(event):
    """
    not hovering over question mark
    """
    rules.place(width=30)
    rules.config(text="?")


def cancel():
    skip_window.destroy()


def skip(labels):
    """
    skip the song
    """
    skip_window.destroy()
    text_entry.place_forget()
    lyrics_canvas.destroy()
    scrollbar.destroy()
    skip_button.place_forget()
    for i in labels:
        i.destroy()
    start_game()


def skip_screen(labels):
    """
    skip screen
    """
    global skip_window
    skip_window = tk.Toplevel(window)
    skip_window.title("")
    skip_window.geometry("300x200")
    skip_window.config(background=colors[7])

    areusure = tk.Label(skip_window, text="Are you sure?")
    areusure.config(
        font=(FONT, 20),
        highlightthickness=0,
        background=colors[7],
        foreground=colors[9]
    )
    areusure.place(x=50, y=30, width=200, height=20)
    yes_skip = tk.Button(skip_window, text="Yes")
    yes_skip.config(
        font=(FONT, 20),
        highlightbackground=colors[3],
        fg=colors[3],
        command=lambda: skip(labels)
    )
    yes_skip.place(x=100, y=80, width=100, height=30)
    nevermind = tk.Button(skip_window, text="Cancel")
    nevermind.config(
        font=(FONT, 20),
        highlightbackground=colors[3],
        fg=colors[3],
        command=cancel
    )
    nevermind.place(x=100, y=130, width=100, height=30)

    skip_window.mainloop()


def show_rules():
    """
    new window pops up when button clicked that shows rules
    would like to implement a scrolling thing, and text will be from rules.txt
    havent written, implement later
    """
    rules_window = tk.Toplevel()
    rules_window.title("Rules")
    rules_window.geometry("500x400")
    rules_window.config(background=colors[7])
    rules = tk.Label(
        rules_window,
        text=rules_text,
        background=colors[7],
        foreground=colors[9],
        wraplength=460,
        justify="left",
        font=(FONT, 14)
    )
    rules.config(anchor="w")
    rules.pack(padx=20, pady=20)
    rules_image = Image.open("tay.jpeg")  # 1600 x 900
    rules_image = rules_image.resize((320, 180))  # Resize the image if needed
    rules_photo = ImageTk.PhotoImage(rules_image)
    rules_pic = tk.Label(rules_window, image=rules_photo, background=colors[4])
    rules_pic.place(x=90, y=180)
    rules_window.mainloop()


def modify_text(word):
    lowercase = "abcdefghijklmnopqrstuvwxyz0123456789"
    ans = ""
    for char in word.lower():
        if char in lowercase:
            ans += char
    return ans


def song_guessed():
    """
    add to data
    """
    global start_time
    elapsed_time = time.time() - start_time
    # print(elapsed_time)
    play_data.guess(elapsed_time)
    guess_button.place_forget()


def win(song, labels):
    """
    flash a congrats sign and prompts continue
    """
    global start_time
    elapsed_time = time.time() - start_time
    # print(elapsed_time)
    if write_to_data:
        play_data.finish(elapsed_time)
    skip_button.place_forget()
    title.config(text=f"The song was {song_mappings.song_dict[song]}!")
    text_entry.place_forget()
    lyrics_canvas.destroy()
    scrollbar.destroy()
    for i in labels:
        i.destroy()
    congrats.place(x=300, y=140)
    start_button.place(x=450, y=640, width=300, height=100)
    start_button.config(text="Play Again?")


def text_entered(event, song, tree, lyrics, labels, words_left):
    """
    when we've detected that text has been entered
    :return:
    """
    text = modify_text(text_entry.get())
    node = tree[text]
    if node is None:
        return
    text_entry.delete(0, tk.END)
    indices = node.get_indices()
    for i in indices:
        words_left[0] -= 1
        labels[i].config(text=lyrics[i])
    tree.remove(text)
    # print(text + " has been removed")
    # print([i.get_word() for i in tree])
    if words_left[0] == 0:
        win(song, labels)
    else:
        return


def start_game():
    """
    gets song, creates boxes, tree
    """
    global start_time, write_to_data, lyrics_canvas, scrollbar
    start_button.place_forget()
    congrats.place_forget()
    if len(song_list) == 0:
        title.config(text="Congrats...? You finished all of them...\n Now please go touch some grass...")
        title.place(x=300, y=300, width=600, height=200)
        return
    title.config(text="Guess the Taylor Swift Song Lyrics!")
    text_entry.place(x=450, y=125, width=300, height=30)
    text_entry.focus_set()
    cur_song = song_list.pop()
    # print(cur_song)
    lyrics = functionality.get_lyrics(cur_song)
    lyrics_canvas = tk.Canvas(window)
    scrollbar = ttk.Scrollbar(
        lyrics_canvas,
        orient=tk.VERTICAL,
        command=lyrics_canvas.yview,
        style="Vertical.TScrollbar"
    )
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
    skip_button.place(x=1000, y=100, width=80, height=30)
    skip_button.config(command=lambda: skip_screen(lyrics_labels))
    # has to go after i put in labels for some reason

    tree = functionality.Tree()
    tree.populate(functionality.modified_lyrics(lyrics))
    if write_to_data:
        guess_button.place(x=100, y=100, width=120, height=30)
        play_data.add_row(cur_song)
        start_time = time.time()
        # print(cur_song)

    text_entry.bind("<KeyRelease>", lambda event: text_entered(event, cur_song, tree, lyrics, lyrics_labels, words_left))


window = tk.Tk()
window.geometry("1200x800")
window.configure(background=colors[7])
window.title("")

title = tk.Label(window, text="Guess the Taylor Swift Song Lyrics!")
title.place(x=0, y=30, width=1200, height=80)
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

rules = tk.Button(window, text="?", highlightbackground=colors[7],
                  command=show_rules, font=(FONT, 20), highlightthickness=15, fg=colors[3])
rules.place(x=10, y=10, width=30, height=30)
rules.bind("<Enter>", rules_hover)
rules.bind("<Leave>", rules_unhover)

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
global lyrics_canvas, scrollbar

skip_button = tk.Button(window)
skip_button.config(
    text="SKIP",
    highlightbackground=colors[3],
    fg=colors[3],
    font=(FONT, 20)
)

guess_button = tk.Button(window)
guess_button.config(
    text="I've guessed it!",
    highlightbackground=colors[3],
    fg=colors[3],
    font=(FONT, 15),
    command=song_guessed
)

global skip_window


window.mainloop()
