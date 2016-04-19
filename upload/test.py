# test.py
from PIL import Image
import os
print (os.path.getsize("../images/eiffel.jpg"))
im = Image.open("../images/eiffel.jpg")
width, height = im.size
print(width, height)
format = im.format
print(format.lower())

# import urllib
# resource = urllib.urlopen("http://www.digimouth.com/news/media/2011/09/google-logo.jpg")
# output = open("file01.jpg","wb")
# output.write(resource.read())
# output.close()