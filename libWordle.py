import json
import random


wordPath = "./words.json"


def init():
    with open(wordPath, 'rb') as f:
        data = json.load(f)
        return data


def gameInit(wordList):
    return wordList[random.randint(0, len(wordList) - 1)]


def validateWord(wordList, allowGuesses, word):
    word = word.upper()
    if(word in wordList):
        return True
    elif(word in allowGuesses):
        return True
    else:
        return False


def checkWord(word, puzzle):
    word = word.upper()
    result = ""
    green = "🟩"
    yellow = "🟨"
    white = "⬜"
    for i in range(len(word)):
        if(word[i] == puzzle[i]):
            result += (green)
        elif(word[i] in puzzle):
            result += (yellow)
        else:
            result += (white)
    return result


def process(word, puzzle, wordList, allowGuesses):
    if(len(word) != 5):
        errMsg = "Please enter a 5 letter word."
        return [False, errMsg, False]
    if(not validateWord(wordList, allowGuesses, word)):
        errMsg = "This word is not in the list."
        return [False, errMsg, False]
    result = checkWord(word, puzzle)
    if(result.count("🟩") == 5):
        return [True, result, True]
    else:
        return [False, result, True]
