"""
    Fetches images from a URL and saves them in /out.
"""
import sys
import os
import requests

url = sys.argv[1] # get the website
r = requests.get(url) # get the html
page = r.content

# Check to see if there's an output directory
os.makedirs("out/", exist_ok=True)

from html.parser import HTMLParser

class ImageParser(HTMLParser):
    def __init__(self):
        super(ImageParser, self).__init__() # call super init
        self.image_count = 0

    def handle_starttag(self, tag, attrs):
        if (tag != 'img'): return # don't do anything for non-image tags
        img_url = ""
        for (key, val) in attrs:
            if (key == 'src'):
                img_url = val # get the image url

        if img_url != "": # if the image isn't blank, write the file
            spl = img_url.split("/")
            if (spl[0] != 'http:' and spl[0] != "https:"): # no http protocol?
                if ("." not in img_url.split("/")[0]): # no domain?
                    img_url = url + img_url[1:] # remove that first slash
                else:
                    img_url = "http://" + img_url

            print("img: " + str(img_url))
            f = open("out/image_" + str(self.image_count) + ".jpg", "wb") # save the image
            img = requests.get(img_url).content # get raw data
            f.write(img) # write the image data
            f.close() # close the file

            self.image_count += 1 # increment the image count

IP = ImageParser()
IP.feed(str(page))
