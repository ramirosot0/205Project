


from PIL import Image
import sys
from PySide2.QtWidgets import (QApplication, QLabel, QWidget, 
				QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox)
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPixmap
from PIL.ImageQt import ImageQt
import random


def search(what):
	from pixabay import Image
	import requests

	API_KEY = '19574412-bdfe5103ad8975a5b45f2da02'

	# image operations
	image = Image(API_KEY)

	# default image search
	image.search()

	# custom image search
	ims = image.search(q= what,
	         image_type='photo',
	         orientation='horizontal',
	         safesearch='true',
	         order='latest')

	#random number of pictures 
	randompic = random.randint(0, 19)


	ph = ims["hits"][randompic]["webformatURL"]

	print(ims["hits"][randompic])

	img_data = requests.get(ph).content
	with open('image_name.jpg', 'wb') as handler:
	    handler.write(img_data)



#--- this function checks what combo box option is chosen by the index number
def manipulation(number):
	if number == 1:
		return sepia()
		
	elif number == 2:
		return negative()
		
	elif number == 3:
		return grayscale()
		
	elif number == 4:
		return thumbnail()

	else:
		return none()
		
#-------- sepia function ---------
def sepia():
	im2 = Image.open('image_name.jpg')
	width, height = im2.size
	sepiaImg = im2.copy()
	
	for x in range(width):
		for y in range(height):
			red, green, blue = im2.getpixel((x,y))
			new_val = (0.3 * red + 0.59 * green + 0.11 * blue)

			new_red = int(new_val * 2)
			if new_red > 255:
				new_red = 255
			new_green = int(new_val * 1.5)
			if new_green > 255:
				new_green = 255
			new_blue = int(new_val)
			if new_blue > 255:
				new_blue = 255

			sepiaImg.putpixel((x,y), (new_red, new_green, new_blue))
	#turn PIL image to Qimage so we can use it in the GUI		
	if sepiaImg.mode == 'RGB':
		sepiaImg = sepiaImg.convert('RGBA')
	qimage = toqimage(sepiaImg)

	return QPixmap.fromImage(qimage)
	
#--------- negative function -----------
def negative():
	im2 = Image.open('image_name.jpg')
	width, height = im2.size
	neg_image = im2.copy()
	
	for x in range(width):
			for y in range(height):
				red, green, blue = im2.getpixel((x,y))
				new_red = 255 - red
				new_green = 255 - green
				new_blue = 255 - blue
				neg_image.putpixel((x,y), (new_red, new_green, new_blue))
	#turn PIL image to Qimage so we can use it in the GUI				
	if neg_image.mode == 'RGB':
		neg_image = neg_image.convert('RGBA')
	qimage = toqimage(neg_image)

	return QPixmap.fromImage(qimage)
	
#------ GrayScale function ----------	
def grayscale():
	im2 = Image.open('image_name.jpg')
	new_list =  [((a[0]*299 + a[1]*587 + a[2]*114 )//1000,) * 3
	for a in im2.getdata()]

	im2.putdata(new_list)
	
	#turn PIL image to Qimage so we can use it in the GUI	
	if im2.mode == 'RGB':
		im2 = im2.convert('RGBA')
	qimage = toqimage(im2)
	
	return QPixmap.fromImage(qimage)

#------To QImage function ------------
def toqimage(im):
	return ImageQt(im)
	
#------ thumbnail function -------
def thumbnail():
	im2 = Image.open('image_name.jpg')
	w, h = im2.width,im2.height
	target = Image.new('RGB', (w, h), 'aliceblue')
	
	target_x = 0
	for source_x in range(0, im2.width, 2):
		target_y = 0
		for source_y in range(0, im2.height, 2):
			pixel = im2.getpixel((source_x, source_y))
			target.putpixel((target_x, target_y), pixel)
			target_y += 1
		target_x += 1
	#turn PIL image to Qimage so we can use it in the GUI		
	if target.mode == 'RGB':
		target = target.convert('RGBA')
	qimage = toqimage(target)

	return QPixmap.fromImage(qimage)

	
#---------none function return the same picture ----------
def none():
	im2 = Image.open('image_name.jpg')
	
	if im2.mode == 'RGB':
		im2 = im2.convert('RGBA')
	qimage = toqimage(im2)

	return QPixmap.fromImage(qimage)



#-------------------
class MyWindow(QWidget):
	def __init__(self):
		super().__init__()
		
		vbox = QVBoxLayout()
		hbox = QHBoxLayout()
		#-- QLineEdit widget to search for an image
		self.my_lineedit = QLineEdit("Enter Key Words To Search Images..")
		self.my_lineedit.setMinimumWidth(250)
		self.my_lineedit.selectAll()
		
		#---QComboBox to allo allow user to select image manipulations
		self.my_manipulation = ["Pick a manupulation", "Sepia", "Negative", "Grayscale","Thumbnail","None"]
		self.my_combo_box = QComboBox()
		self.my_combo_box.addItems(self.my_manipulation)
		self.my_combo_box.currentIndexChanged.connect(self.update_ui)
		
		#---button to display images 
		self.my_btn = QPushButton("Search or press Return")
		self.my_btn.clicked.connect(self.on_submit)
		self.my_lineedit.returnPressed.connect(self.on_submit)
		
		#--- picture label 
		self.image_label = QLabel()

		#---adding widgets to the box layout
		hbox.addWidget(self.my_combo_box)
		vbox.addWidget(self.my_lineedit)
		vbox.addWidget(self.my_btn)
		vbox.addWidget(self.image_label)
		
		
		#---outer layer
		main_layout = QHBoxLayout()
		#add previous inner layouts 
		main_layout.addLayout(vbox)
		main_layout.addLayout(hbox)
		
		#---set outer layout as a main layout of the widget
		self.setLayout(main_layout)
		
		#---window title and background color
		self.setWindowTitle("Pixabay Search Engine")
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.darkCyan)
		self.setPalette(p)

		
	#---when the button is pressed we begin to load our new directory
	#---search if the input string matches with ouir records
	#---counts the matches for a better result and sort the matches
	@Slot()
	def on_submit(self):
		your_picture = self.my_lineedit.text().lower()							

		search(your_picture)
		#---dysplay the best match image to the image widget 
		pixmap = QPixmap('image_name.jpg')
		pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
		self.image_label.setPixmap(pixmap)

		
	@Slot()
	def update_ui(self):
		#---update the manipuled image by the index chosen
		my_index = self.my_combo_box.currentIndex()
		#--call the manipulation function and updates the image
		pixmap = manipulation(my_index)
		pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
		self.image_label.setPixmap(pixmap)


app = QApplication([])
my_win = MyWindow()
my_win.show()
app.exec_()