#!/usr/bin/python3

#tooltips
# Please read this tutorial on how to prepare your images for use with DeepCreamPy.
# The greater the number of variations, the longer decensoring process will be.

import sys, time
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QDesktopWidget, QApplication, QAction, qApp, QApplication, QMessageBox, QRadioButton, QPushButton, QTextEdit, QLabel, QSizePolicy,QMainWindow
from PySide2.QtCore import Qt, QObject
from PySide2.QtGui import QFont, QTextCursor

from decensor import Decensor

from progressWindow import ProgressWindow

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
		self.tutorialLabel.setText("Welcome to DeepCreamPy!\n\nIf you're new to DCP, please read the README.\nThis program does nothing without the proper setup of your images.\n\nReport any bugs you encounter to me on Github or Twitter @deeppomf.")
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

		#Decensor button
		self.decensorButton = QPushButton('Decensor Your Images')
		self.decensorButton.clicked.connect(self.decensorClicked)
		self.decensorButton.setSizePolicy(
    		QSizePolicy.Preferred,
    		QSizePolicy.Preferred)

		#Progress message
		# self.progressGroupBox = QGroupBox('Progress')

		self.progressMessage = QTextEdit()
		self.progressCursor = QTextCursor(self.progressMessage.document())
		self.progressMessage.setTextCursor(self.progressCursor)
		self.progressMessage.setReadOnly(True)
		self.progressCursor.insertText("After you prepared your images, click on the decensor button once to begin decensoring.\nPlease be patient.\nDecensoring will take time.\n")

		#put all groups into grid
		grid_layout.addWidget(self.tutorialLabel, 0, 0, 1, 2)
		grid_layout.addWidget(self.censorTypeGroupBox, 1, 0, 1, 1)
		grid_layout.addWidget(self.variationsGroupBox, 1, 1, 1, 1)
		grid_layout.addWidget(self.decensorButton, 2, 0, 1, 2)
		grid_layout.addWidget(self.progressMessage, 3, 0, 4, 2)

		#window size settings
		self.resize(500, 500)
		self.center()
		self.setWindowTitle('DeepCreamPy v2.2.0-beta')
		self.show()

	def decensorClicked(self):
		self.decensorButton.setEnabled(False)
		self.progressMessage.clear()
		self.progressCursor.insertText("Decensoring has begun!\n")

		decensor = Decensor(text_edit = self.progressMessage, text_cursor = self.progressCursor, ui_mode = True)
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


		self.decensorButton.setEnabled(True)
		self.hide()
		self.progress = ProgressWindow(self, decensor = decensor)
		# decensor.decensor_all_images_in_folder()

		# self.progress.hide()
		# self.show()

	# def showAbout(self):
	# 	QMessageBox.about(self, 'About', "DeepCreamPy v2.2.0 \n Developed by deeppomf")

	# #centers the main window
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__ == '__main__':
	import os
    # you could remove this if statement if there's no error without this
	if os.name == 'nt':
		import PySide2
		pyqt = os.path.dirname(PySide2.__file__)
		QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
