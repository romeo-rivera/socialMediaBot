from bs4 import BeautifulSoup
from requests import get
import re
import urllib.request
from instapy_cli import client

def getsoup(url):
    hdrs = {'user-agent': 'Chrome/75.0'}
    r = get(url, headers = hdrs)
    return BeautifulSoup(r.text, 'html.parser')


# gets all the links to the comments so we can retrieve image from the post
def getpostlinks(url):
    retList = []
    soup = getsoup(url)
    urlToSearch = url + "comments"
    for post in soup.find_all('a', attrs={'href': re.compile("^"+re.escape(urlToSearch))}):
        retList.append(post.get('href'))
    return retList


# gets a singular link to the image source
def getimgsource(url):
    soup = getsoup(url)
    for img in soup.find_all('img', alt=True):
        if img['alt'] == 'Post image':
            return img['src']


# given the list of links to the images, downloads all images in the list
def downloadimgs(imgLinkList):
    ctr = 0
    for img in imgLinkList:
        if img is None:
            continue
        else:
            urllib.request.urlretrieve(img, "post" + str(ctr) + ".jpg")
            ctr += 1
    print("downloaded " + str(ctr) + " images")

#TODO, GET TITLE OF POST YOU ARE SCRAPING

'''
linkList = getpostlinks('https://www.reddit.com/r/pics/')
picLinkList = []
for link in linkList:
    picLinkList.append(getimgsource(link))
downloadimgs(picLinkList)
'''

# ok it posts to Instagram but i need to automate it, and you kinda need to download the images in the
# local directory
username = str(input('giv username: '))
password = str(input('giv pass: '))
image = 'post0.jpg'
text = 'please post'

with client(username, password) as cli:
    cli.upload(image,text)
