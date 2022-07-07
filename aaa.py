import requests

url = "https://res.cloudinary.com/ds5ubialh/image/upload/v1655775979/vp2psssngwmypvostxlh.pdf"
r = requests.get(url)
with open("meupdf.pdf", 'wb') as f:
    f.write(r.content) 