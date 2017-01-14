#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Takes Disqus Export xml and converts posts into yaml 
https://help.disqus.com/customer/portal/articles/472149-comments-export

Matched format for how I have Staticman configured for comments.  I then use Hugo to generate the page.

Generates the following folder structure:

comments
└── slug
    └── comment-{timestamp}.yml

'''
from xml.dom.minidom import parse
import dateutil.parser
import xml.dom.minidom
import hashlib
import os
import codecs
import time

linkPrefix = "https://mrmatt57.org/"
directory = "comments"
commentsfile = "comments.xml"

def getThreadName(threads, id):
    for thread in threads:
        if(thread.getAttribute("dsq:id") == id):
            link = thread.getElementsByTagName('link')[0].childNodes[0].data
            slug = link.replace(linkPrefix, "")[:-1]
            return slug

scriptdir = os.path.dirname(__file__)
tree = xml.dom.minidom.parse(commentsfile)
collection = tree.documentElement
threads = collection.getElementsByTagName("thread")
posts = collection.getElementsByTagName("post")

## Setup output folder
if not os.path.exists(directory):
    os.makedirs(directory)

for post in posts:
    ## Only get visible posts
    isDeleted = post.getElementsByTagName('isDeleted')[0].childNodes[0].data
    if isDeleted == "false":
        
        ## Get comment attributes
        id = post.getElementsByTagName('id')[0].childNodes[0].data
        threadid = post.getElementsByTagName('thread')[0].getAttribute("dsq:id")
        threadname = getThreadName(threads, threadid)
        author = post.getElementsByTagName('author')[0]
        name =  author.getElementsByTagName('name')[0].childNodes[0].data
        email = author.getElementsByTagName('email')[0].childNodes[0].data
        md5 = hashlib.md5(email.encode('utf-8')).hexdigest()
        message = post.getElementsByTagName('message')[0].childNodes[0].data
        date = post.getElementsByTagName('createdAt')[0].childNodes[0].data
        formateddate = str(int(time.mktime(dateutil.parser.parse(date).timetuple())))

        ## Setup post comment folder
        postfolder = "comments/" + threadname
        commentrelative = postfolder + "/comment-" + formateddate + ".yml"
        filepath = os.path.join(scriptdir, commentrelative)
        if not os.path.exists(postfolder):
            os.makedirs(postfolder)
        
        ## Write File
        file = codecs.open(filepath, 'w+', "utf-8")
        file.truncate()
        file.write("id: " + id + "\n")
        file.write("name: " + name + "\n")
        file.write("email: " + md5 + "\n")
        file.write("date: " + date + "\n")
        file.write("message: | \n    " + message + "\n")
        file.close()

        print(commentrelative)