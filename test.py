from urllib.request import urlopen

url = 'http://thebibleofetailing.com/'
for i in range(10000):
    try:
        website = urlopen(url)
    except Exception:
       pass