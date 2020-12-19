from flask import Flask, render_template
import requests, json
from flask_bootstrap import Bootstrap
from PIL import Image 
import numpy as np

app = Flask(__name__)
bootstrap = Bootstrap(app)

# better to replace this with your own key from https://api.nasa.gov/
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'

payload = {
  'api_key': my_key,
  'start_date': '2020-11-05',
  'end_date': '2020-11-08'
}

endpoint = 'https://api.nasa.gov/planetary/apod'

endpoint2 = 'http://www.boredapi.com/api/activity/'

@app.route('/')
def main():
    try:
        #r = requests.get(endpoint, params=payload)
        r = requests.get(endpoint2)
        data = r.json()
        print(data)
    except:
        print('please try again')
    return render_template('boredapi.html', data=data)




# Daisy's code
def shrink_image(your_image):
    source3 = Image.open(your_image)
    w,h = source3.width, source3.height

    # target is where I want to move my images to
    # We don't need this if we aren't moving the image anywhere
    # the w, h above is the size of the canvas
    # canvas = Image.new('RGB', (w, h))

    w_image = input ("Enter a value to reduce your image's width (Between 0 - 5): ")
    h_image = input ("Enter a new height (Between 0 - 5): ")

    # this will shrink a picture
    target_x = 0                                                # Position of the image on the x axis in which we start
    for source_x in range(0, source3.width, w_image):           # source3 is the image we are resizing
        target_y = 0                                            # position of the image on the y axis in which we start
        for source_y in range(0, source3.height, h_image):      # source3 is the 
            pixel = source3.getpixel((source_x, source_y))      # gets pixel by pixel from the image, stores that specific image in "pixel"
            canvas = Image.new('RGB', (round(w/w_image), round(h/h_image))) # I think here I'm creating this canvas and it will be the size that the image is shrinking to
            canvas.putpixel((target_x, target_y), pixel)        # places pixel in the canvas
            target_y += 1
        target_x += 1
    canvas.show()




# Another way to resize an image --  online example
# here I installed the following " pip install python-resize-image "
def resize_up_down(your_image):

    # opens an image
    image = Image.open(your_image)

    # We ask the user what size he wants to resize the image to
    w = input ("Enter a new width for the image: ")
    h = input ("Enter a new height: ")
    resized_image = image.resize(w, h)
    # resized_image.save('bb3_resized.jpg')
    resized_image.show()




# Scaling up
def scaling_up(your_image):
    source = Image.open(your_image)
    mf = input ("Enter a value to enlarge your image (Between 2 - 4): ")
    w, h = source.width * mf, source.height * mf
    target = Image.new('RGB', (w,h))

    target_x = 0
    for source_x in np.repeat(range(source.width), mf):
        target_y = 0
        for source_y in np.repeat(range(source.height), mf):
            pixel = source.getpixel((int(source_x), int(source_y)))
            target.putpixel((target_x, target_y), pixel)
            target_y += 1
        target_x += 1
    target.show()




# Grayscale
def grayscale(p):
    new_red = int(p[0] * 0.299)
    new_green = int(p[1] * 0.587)
    new_blue = int(p[2] * 0.114)
    lumi = new_red + new_green + new_blue
    return(lumi,) * 3

def gray_list(pic):
    gray_list = [grayscale(p) for p in pic.getdata()]
    return gray_list


# Grayscale -- Online
def grayscale2(your_image):
    image = Image.open(your_image)
    greyscale_image = image.convert('L')
    greyscale_image.show()




# Negative
def negative(your_image):
    img = Image.open(your_image)
    image_a = np.array(img)
    max_value = 255
    image_a = max_value - image_a
    inverted_image = Image.fromarray(image_a)
    inverted_image.show()