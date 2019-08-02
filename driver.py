from bs4 import BeautifulSoup
from requests import get
import re
import urllib.request
from time import time

start = time()
def getSoup(url):
    hdrs = {'user-agent': 'Chrome/75.0'}
    r = get(url, headers = hdrs)
    return BeautifulSoup(r.text, 'html.parser')


# gets all the links to the comments so we can retrieve image from the post
def getPostLinks(url):
    retList = []
    soup = getSoup(url)
    urlToSearch = url + "comments"
    for post in soup.find_all('a', attrs={'href': re.compile("^"+re.escape(urlToSearch))}):
        retList.append(post.get('href'))
    return retList

#gets a singular link to the image source
def getImgSource(url):
    soup = getSoup(url)
    for img in soup.find_all('img', alt=True):
        if img['alt'] == 'Post image':
            return img['src']

#given the list of links to the images, downloads all images in the list
def downloadImgs(imgLinkList):
    ctr = 0
    for img in imgLinkList:
        if img is None:
            continue
        else:
            urllib.request.urlretrieve(img, "post" + str(ctr) + ".jpg")
            ctr += 1
    print("downloaded " + str(ctr) + " images")

linkList = getPostLinks('https://www.reddit.com/r/pics/')
picLinkList = []
for link in linkList:
    picLinkList.append(getImgSource(link))
downloadImgs(picLinkList)

