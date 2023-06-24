# for cleaning the songs

albums = [
    "taylor_swift", "fearless", "speak_now", "red", "1989",
    "reputation", "lover", "folklore", "evermore", "midnights"
]

alphabet = "abcdefghijklmnopqrstuvwxyz-0123456789"

for title in albums:
    song_list = []
    with open(f"{title}.txt", "r") as file:
        for line in file:
            begin_i = 0
            end_i = len(line) - 1
            for i, letter in enumerate(line):
                if letter == "\"":
                    if begin_i == 0:
                        begin_i = i + 1
                    else:
                        end_i = i
            song_list.append(line[begin_i:end_i])
    with open(f"{title}.txt", "w") as file:
        for line in song_list:
            song = ""
            for char in line.lower().replace(" ", "-"):
                if char in alphabet:
                    song += char
                elif char == "&":
                    song += "and"
            file.write(song + "\n")
        file.write("\n")

# for title in ("fearless", "red"):
#     song_list = []
#     with open(f"{title}.txt", "r") as file:
#         for line in file:
#             song_list.append(line[:-1] + "-taylors-version\n")
#     with open(f"{title}.txt", "w") as file:
#         for line in song_list:
#             file.write(line)
#         file.write("\n")
