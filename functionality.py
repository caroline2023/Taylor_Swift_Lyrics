# functions for the program

# probably should clean things up a bit and make it nicer 
# because tree and node can be combined, use functions to finish the rest?

import requests
from bs4 import BeautifulSoup

uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_lyrics(song):
    """
    get the lyrics for the song
    :param song: title
    :return: list of lyrics?
    """
    address = f"https://genius.com/Taylor-swift-{song}-lyrics"
    # Send a GET request to the website
    response = requests.get(address)
    # Create a BeautifulSoup object from the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the specific element(s) containing the desired text
    # For example, let's extract the text from all <p> elements
    paragraphs = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-5 Dzxov')

    words = []

    # Iterate over the found elements and extract the text
    for paragraph in paragraphs:
        text = paragraph.get_text()
        # print(text)
        start = 0
        index = 0
        quote = False
        while index != len(text):
            if text[index] == "[":
                if start != index:
                    words.append(text[start:index])
                while text[index] != "]":
                    index += 1
                index += 1
                start = index
            elif text[index] in (" ", "\u2005", "\u205f"):
                words.append(text[start:index])
                index += 1
                start = index
            elif text[index] == "\"":
                quote = not quote
                index += 1
            elif text[index] == "é":
                text = text[:index] + "e" + text[index + 1:]
            elif text[index] in uppercase and not (
                    text[index - 1] == " " or
                    (text[index - 1] in ("\"", "\'", "(") and text[index - 2] == " ")):
                if text[index - 1] == "(":
                    if start != index - 1:
                        words.append(text[start:index-1])
                    start = index - 1
                elif text[index - 1] == "\"":
                    if quote:
                        if start != index - 1:
                            words.append(text[start:index-1])
                        start = index - 1
                    else:
                        if start != index:
                            words.append(text[start:index])
                        start = index
                elif text[index - 1] == "\'":
                    if text[index-3:index-1] == "in":
                        if start != index:
                            words.append(text[start:index])
                        start = index
                    else:
                        if start != index - 1:
                            words.append(text[start:index-1])
                        start = index - 1
                elif start != index:
                    words.append(text[start:index])
                    start = index
                index += 1
            else:
                index += 1
        words.append(text[start:index])
    return words


def modified_lyrics(lyrics):
    """
    change all lyrics to be lowercase and no punctuation
    punctuation does not matter
    :param lyrics: original
    :return: modified, not original
    """
    modified = []
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    for word in lyrics:
        add = ""
        for char in word.lower():
            if char in lowercase:
                add += char
        modified.append(add)
    return modified


class Node:
    """
    for each word in the song, think of it as a tree node
    """
    def __init__(self, letter, parent):
        self.letter = letter
        self.children = {}
        self.indices = set()
        self.parent = parent

    def get_letter(self):
        return self.letter

    def get_children(self):
        return self.children

    def get_indicies(self):
        return self.indices

    def get_parent(self):
        return self.parent

    def add_child(self, letter):
        self.children[letter] = Node(letter, self)

    def add_index(self, i):
        self.indices.add(i)

    def get_word(self):
        """
        just to return the word the node actually represents
        :return: str
        """
        arr = []
        cur = self
        while cur.parent is not None:
            arr.append(cur.get_letter())
            cur = cur.parent
        ans = ""
        for i in range(len(arr) - 1, -1, -1):
            ans += arr[i]
        return ans

    def __str__(self):
        return str(
            {
                "word": self.get_word(),
                "children": [i for i in self.children],
                "indices": [i for i in self.indices]
            }
        )

    def __iter__(self):
        if len(self.children) == 0:
            if len(self.get_indicies()) > 0:
                yield self
            return
        if len(self.indices) > 0:
            yield self
        for child in self.children.values():
            for i in child:
                yield i


class Tree:
    """
    to store all the words
    also yes i am aware that i should just be storing the tree as a node
    because after all, all nodes are graphs, but its fineeeee i might do it later
    """
    def __init__(self):
        self.root = Node("", None)

    def __iter__(self):
        for i in self.root:
            yield i

    def populate(self, words):
        """
        add the nodes to the tree
        :param words: list of words
        :return:
        """
        for i, word in enumerate(words):
            cur = self.root
            for letter in word:
                cur = cur.get_children().setdefault(letter, Node(letter, cur))
            cur.add_index(i)

    def __getitem__(self, item):
        """
        get the node in the tree
        :param item: word
        :return:
        """
        cur = self.root
        for i in item:
            try:
                cur = cur.get_children()[i]
            except KeyError:
                # print("Word is not in tree")
                return
        if len(cur.get_indicies()) == 0:
            return
        return cur

    def remove(self, key):
        node = self[key]
        if node is None:
            # print("Word is not in tree")
            return
        node.indices = set()
        while len(node.get_children()) == 0 and node.parent is not None:
            if len(node.get_indicies()) > 0:
                break
            key = node.get_letter()
            node = node.get_parent()
            node.get_children().pop(key)


# pls = Tree()
# # pls.populate(modified_lyrics(get_lyrics("illicit-affairs")))
# print(get_lyrics("champagne-problems"))
# #
# pls.remove("a")
# # print(pls["a"])
# print([i.get_word() for i in pls])
#
# print(get_lyrics("anti-hero"))
# print(modified_lyrics(get_lyrics("mine")))
