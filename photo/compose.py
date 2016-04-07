# compose.py
import requests
import simplejson

url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&q=barack%20obama')

r = requests.get(url)
# response = urllib.urlopen(request)

# Process the JSON string.
results = simplejson.load(r)
print(results)
# now have some fun with the results...