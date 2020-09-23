import time
import random
import os
import requests
import traceback
from bs4 import BeautifulSoup
"""
THIS PROGRAM EXISTS WITHOUT WARRANTY OR REPUTATION
PottyMouth is designed to scrape user comments from pornhub photo albums.
The NaughtyRobot then reposts these comments randomly for comedic effect.
"""
class PottyMouth:

    commentsList = []
    linksList = {}
    link = {"link": "X", "title": "X"}
    linksList2 = []
    linksList3 = []
    photoCount = 0
    comments=[]

    def __init__(self):
        d_url = "https://pornhub"
        urls = {
                #Notice the difference between mv and page 2.
                #
                "{d_url}.com/girls_pics_MV": 'female-straight-uncategorized?o=mv',
                "{d_url}.com/girls_pics_MV_pages":"albums/female-straight-uncategorized?o=mv&page=2",
                "{d_url}.com/gaytrans_pics_MV": 'albums/gay-misc-transgender-uncategorized?o=mv',
                "{d_url}.com/all_pic_categories": "albums/female-gay-male-straight-transgender-uncategorized?o=mv&page=7",
                }
        url = 'https://pornhub.com'
        #Maximum number of pages per search category
        maxPages = {
                "girls_pics_MV": 800,
                "gaytrans_pics_MV": 150,
                "all_pic_categories": 1000,
                "/album/30480621": 5
        }
        #Connect to URL
        response=requests.get(urls["all_pic_categories"], timeout=10)
        #Parse HTML ans save as BS object
        soup = BeautifulSoup(response.text, "html.parser")
         #Find all a tags
        #for line in soup.find_all('a', href=True):
        for album in soup.select('a[href*="/album/"]'):
            newURL =album["href"]
            newTitle = album.select('.title-album')[0].get_text()
            #print(newURL+"   "+str(newTitle))
            if newTitle not in self.linksList.keys():
                self.linksList[newTitle] = newURL
        links2 = self.linksList.copy()
        self.linksList.clear()
        for link in links2.keys():
            #print(links2)
            time.sleep(3)
            response = requests.get(str(url+links2[link]), timeout=10)
            bs1 = BeautifulSoup(response.text, "html.parser")
            for photo in bs1.select('.photoAlbumListContainer'):
                url2 = photo.select('a[href*="/photo/"]')
                x = photo.find('div')
                albumtitle =x["title"]
                photoURL = url2[0]["href"]
                #self.linksList[albumtitle]=photoURL
                self.linksList2.append({"album":albumtitle,"url":photoURL})
    #####################################################################
            links3 = self.linksList2.copy()
            self.linksList2.clear()
            #print(links3.keys())
            #for link3 in links3.keys():
            for link3 in links3:
                #print(url + link3["url"]+" "+link3["album"])######
                sleeptime = random.randint(1,5)
                time.sleep(2)
                self.photoCount = self.photoCount + 1
                #response = requests.get(url+links3[link3])
                print(str(url)+str(link3["url"]))
                try:
                    response = requests.get(url + link3["url"], timeout=10)
                except Exception as e:
                    print(e)
                    print("Sleeping for 30 seconds.")
                    time.sleep(30)
                    continue
                bs2 = BeautifulSoup(response.text, "html.parser")
                #print(bs2.prettify())
                f = bs2.select('div[class="commentMessage"]')
                for comments in f:
                    v = comments.find('span').get_text()
                    if "[[commentMessage]]" not in v:
                        commentFound = {"album":link3["album"],"picture":link3["url"],"comment":v}
                        print(v)
                        with open(os.path.join(os.getcwd(), "PH_Comments.txt"), 'a',encoding='utf8') as PHLOG:
                            PHLOG.write(str(commentFound)+"\n")
        print("###############PHOTO COUNT #################")
        print(self.photoCount)

def mostDirtyWords():
    try:
        mostWords = {}
        print(os.getcwd())
        with open("PH_Comments.txt", encoding='utf-8') as f:
            lines = f.readlines()
            for entry in lines:
                line = eval(entry)

                comment = line['comment']
                words = comment.split()
                #print(words)
                for word in words:
                    word = word.lower()
                    try:
                         if word not in mostWords:
                             mostWords[word] = 1
                         else:
                             mostWords[word] = mostWords[word] + 1
                    except Exception as e:
                        print(traceback.format_exc())

        sort_words = sorted(mostWords.items(), key=lambda x: x[1], reverse=True)
        mostWords = sort_words[10:]
        for dirtyWords in sort_words:
            print(dirtyWords)
    except Exception as e:
        print(traceback.format_exc())

if __name__ == '__main__':
    #c = PottyMouth()
    mostDirtyWords()
