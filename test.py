import requests
from bs4 import BeautifulSoup
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


url = "https://www.sec.gov/Archives/edgar/data/1652044/000165204418000007/goog10-kq42017.htm"
html = requests.get(url)
soup = BeautifulSoup(html.text,"html.parser")

# kill all script and style elements
 # rip it out

# get text
text = soup.get_text()
print(text)
"""# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
#text = '\n'.join(chunk for chunk in chunks if chunk)
"""
"""tokens = word_tokenize(text)
#we'll create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';',':','[',']',',']
#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
stop_words = stopwords.words('english')
#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
"""
def getStatementNames(text):
    pass


test_text = 'estimation.44Table of ContentsAlphabet Inc.ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA45Item 9.Alphabet Inc.INDEX TO CONSOLIDATED FINANCI FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA'
Item_8_H = 'FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA'
Item_8_L = 'Financial Statements and Supplementary Data'
item_8_len = len(Item_8_H)
phrase_builder = ''
phrase_count = 0
string_count = 0

for letter in text:
    string_count += 1
    #print(letter)
    #print(string_count)
    #print(phrase_builder)
    if letter.isalpha() or letter.isdigit() is False:
        phrase_builder += letter
    else:
        phrase_builder = ''
    if len(phrase_builder) == item_8_len:
        if phrase_builder == Item_8_H or phrase_builder == Item_8_L:
            #print(string_count)
            #print(phrase_builder)
            #tester_text = text[string_count:string_count+20]
            #print(tester_text)
            newtext = re.findall(r'[A-Za-z]+|\d+', text[string_count:string_count+100])
            print(newtext)
            if 'Consolidated' not in newtext or 'CONSOLIDATED' not in newtext:
                print("Wrong set")
                phrase_builder = ''
                phrase_count = 0
            else:
                print("Success")
                print(phrase_builder)
                print(string_count)
                print(text[string_count:])


        else:
            for x in phrase_builder:
                phrase_count += 1
                #print(x)
                if x.isalpha() is False:
                    phrase_builder = phrase_builder[phrase_count:]
                    phrase_count = 0
                    break

