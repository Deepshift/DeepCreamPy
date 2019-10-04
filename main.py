#!/usr/bin/python3

#tooltips
# Please read this tutorial on how to prepare your images for use with DeepCreamPy.
# The greater the number of variations, the longer decensoring process will be.

import sys
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QDesktopWidget, QApplication, QAction, qApp, QApplication, QMessageBox, QRadioButton, QPushButton, QLabel, QSizePolicy
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont

from decensor import Decensor

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		grid_layout = QGridLayout()
		grid_layout.setSpacing(10)
		self.setLayout(grid_layout)

		#Tutorial
		self.tutorialLabel = QLabel()
		self.tutorialLabel.setText("Welcome to DeepCreamPy!\nIf you're new to DCP, please read the manual.")
		self.tutorialLabel.setAlignment(Qt.AlignCenter)
		self.tutorialLabel.setFont(QFont('Sans Serif', 13))

		#Censor type group
		self.censorTypeGroupBox = QGroupBox('Censor Type')

		barButton = QRadioButton('Bar censor')
		mosaicButton = QRadioButton('Mosaic censor')
		barButton.setChecked(True)

		censorLayout = QVBoxLayout()
		censorLayout.addWidget(barButton)
		censorLayout.addWidget(mosaicButton)
		# censorLayout.addStretch(1)
		self.censorTypeGroupBox.setLayout(censorLayout)

		#Variation count group
		self.variationsGroupBox = QGroupBox('Number of Decensor Variations')

		var1Button = QRadioButton('1')
		var2Button = QRadioButton('2')
		var3Button = QRadioButton('4')
		var1Button.setChecked(True)

		varLayout = QVBoxLayout()
		varLayout.addWidget(var1Button)
		varLayout.addWidget(var2Button)
		varLayout.addWidget(var3Button)
		# varLayout.addStretch(1)
		self.variationsGroupBox.setLayout(varLayout)

		#button
		decensorButton = QPushButton('Decensor Your Images')
		decensorButton.clicked.connect(self.decensorClicked)
		decensorButton.setSizePolicy(
    		QSizePolicy.Preferred,
    		QSizePolicy.Preferred)

		#put all groups into grid
		grid_layout.addWidget(self.tutorialLabel, 0, 0, 1, 2)
		grid_layout.addWidget(self.censorTypeGroupBox, 1, 0, 1, 1)
		grid_layout.addWidget(self.variationsGroupBox, 1, 1, 1, 1)
		grid_layout.addWidget(decensorButton, 2, 0, 1, 2)

		#window size settings
		self.resize(300, 300)
		self.center()
		self.setWindowTitle('DeepCreamPy v2.2.0')
		self.show()

	def decensorClicked(self):
		decensor = Decensor()
		#https://stackoverflow.com/questions/42349470/pyqt-find-checked-radiobutton-in-a-group
		#set decensor to right settings
		#censor type
		censorTypeElements = self.censorTypeGroupBox.children()
		censorButtons = [elem for elem in censorTypeElements if isinstance(elem, QRadioButton)]
		for cb in censorButtons:
			if cb.isChecked():
				censorType = cb.text()
		if censorType == 'Bar censor':
			decensor.is_mosaic = False
		else:
			decensor.is_mosaic = True

		#variations count
		variationsElements = self.variationsGroupBox.children()
		variationsButtons = [elem for elem in variationsElements if isinstance(elem, QRadioButton)]
		for vb in variationsButtons:
			if vb.isChecked():
				variations = int(vb.text())
		decensor.variations = variations

		decensor.decensor_all_images_in_folder()

	# def showAbout(self):
	# 	QMessageBox.about(self, 'About', "DeepCreamPy v2.2.0 \n Developed by deeppomf")
		
	# #centers the main window
	def center(self):
		
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())