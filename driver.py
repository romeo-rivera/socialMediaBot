from bs4 import BeautifulSoup
from requests import get
import re
import urllib.request
from instapy_cli import client
import random


def getsoup(url):
    hdrs = {'user-agent': 'Chrome/75.0'}
    r = get(url, headers = hdrs)
    return BeautifulSoup(r.text, 'html.parser')


# gets all the links to the comments sections of the post so we can retrieve images from the post
def getpostlinks(url):
    retList = []
    soup = getsoup(url)
    urlToSearch = url + "comments"
    # every post has the url followed by comments, we can get this by using regex
    for post in soup.find_all('a', attrs={'href': re.compile("^"+re.escape(urlToSearch))}):
        retList.append(post.get('href'))
    return retList


# gets a singular link to the image source
def getimgsource(url):
    soup = getsoup(url)
    # images in the comment portion of posts have the img tag, we find the source this way
    print('getting imgsource')
    for img in soup.find_all('img', alt=True):
        if img['alt'] == 'Post image':
            return img['src']
    print('completed getting imgsource')


# given the list of links to the images, downloads all images in the list
def downloadimgs(imgLinkList):
    ctr = 0
    print('beginning to download images')
    for img in imgLinkList:
        # sometimes, the bot retrieves a pinned post from the reddit so we skip image source if we encounter it
        if img is None:
            continue
        else:
            urllib.request.urlretrieve(img, "post" + str(ctr) + ".jpg")
            ctr += 1
    print("downloaded " + str(ctr) + " images")


def gettitle(url):
    soup = getsoup(url)
    print('getting title')
    for s in soup.find_all('h1'):
        return s.text


def posttoinstagram(username, password, image, text):
    print('Beginning to post to instagram')
    with client(username, password) as cli:
        cli.upload(image, text)
    print('Successfully posted to instagram')



linkList = getpostlinks('https://www.reddit.com/r/pics/')
# pops the pinned post (not that great of a solution but will work for now)
linkList.pop(0)
picLinkList = []
titleLinkList = []
for index, link in enumerate(linkList):
    picLinkList.append(getimgsource(link))
    titleLinkList.append(gettitle(link))
downloadimgs(picLinkList)

# TODO, Find out if post is a "pinned post" and completely ignore that post
# TODO, Change to OOP because it is far more elegant than this current design (later)

username = str(input('Username login: '))
password = str(input('Password login: '))
randNum = random.randint(0, 6)
image = 'post' + str(randNum) + '.jpg'
text = titleLinkList[randNum]

posttoinstagram(username, password, image, text)
# Remove post so it isn't possible to post again
titleLinkList.pop(randNum)
picLinkList.pop(randNum)
