from PIL import Image

def convert(output):
    try:
        img.save(str(output) + ".ico",format = 'ICO', sizes=[(128,128)])
    except:
        print("output compyling error")
inpath = "logo.png"
outpath = "logo"
try:
    img = Image.open(inpath)
    convert(outpath)
except:
    print("Failed")
