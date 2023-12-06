def convertToList(arr):
    wordAr = arr.replace(" ", "").lower().split(",")
    items = [x for x in wordAr if x]
    return list(set(items))

def lowerArray(arr):
    wordAr = [x.lower() for x in arr]
    return wordAr

def cleanInput(word):
    newWord = word.lower()
    return newWord