from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QGraphicsDropShadowEffect, QPushButton, QStyle, QLineEdit, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QThread, QRegExp

from sys import exit, argv
from time import sleep

class sortedKnot():
	def __init__(self, value, r=1, i=0, parent=None, parentKnot=None):
		self.left, self.right = None, None
		self.value = value
		self.parentKnot = parentKnot
		self.i, self.r = i, r
		self.parentWindow = parent
		s = QGraphicsDropShadowEffect()
		s.setColor(QColor("#000000"))
		s.setBlurRadius(5)
		s.setOffset(1,1)
		self.label = QLabel(str(self.value), self.parentWindow.frameTree)
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setObjectName("Layer2")
		self.label.setFont(QFont("Arial", self.parentWindow.fontSize))
		self.label.setGraphicsEffect(s)

	def getMaxAltitude(self):
		a, l, r = 1, 0, 0
		if self.left: l = self.left.getMaxAltitude()
		if self.right: r = self.right.getMaxAltitude()
		return a+l if l > r else a+r


	def addLeft(self, k):
		if not self.left:
			self.left = sortedKnot(k, 2*self.r-1, self.i+1, self.parentWindow, self)
		else:
			k = sortedKnot(k, 2*self.r-1, self.i+1, self.parentWindow, self)
			k.left = self.left
			self.left.parentKnot = k
			self.left.moveDown(self.left.i+1, 2*k.r-1)
			self.left = k

	def moveDown(self, i, r):
		self.i = i
		self.r = r
		if self.left:
			self.left.moveDown(i+1, 2*r-1)
		if self.right:
			self.right.moveDown(i+1, 2*r)

	def addRight(self, k):
		if not self.right:
			self.right = sortedKnot(k, 2*self.r, self.i+1, self.parentWindow, self)
		else:
			k = sortedKnot(k, 2*self.r, self.i+1, self.parentWindow, self)
			k.right = self.right
			self.right.parentKnot = k
			self.right.moveDown(self.right.i+1, 2*k.r)
			self.right = k

	def addSorted(self, k):
		if k == self.value:
			self.parentWindow.showError("The value you tried to insert is already taken", "Value Error")
		elif k < self.value:
			if self.left:
				self.left.addSorted(k)
			else:
				self.addLeft(k)

		elif k > self.value:
			if self.right:
				self.right.addSorted(k)
			else:
				self.addRight(k)


	def update(self):
		if not self.parentKnot:
			self.parentWindow.knotCoordinates = []
			self.maxI = self.getMaxAltitude()-1


		self.y = int(self.i * ((self.parentWindow.frameTree.height()-100) / (self.parentWindow.rootTree.maxI+1)))+50
		if self.i < self.parentWindow.rootTree.maxI:
			if not self.left : self.left  = sortedKnot(-1, 2*self.r-1, self.i+1, self.parentWindow, self)
			if not self.right: self.right = sortedKnot(-1, 2*self.r  , self.i+1, self.parentWindow, self)

			lx = self.left .update()
			rx = self.right.update()
			
			self.x = int((lx+rx) / 2)

			if self.left.value == -1:
				self.left.delete()
			else:
				self.parentWindow.knotCoordinates.append((self.x, self.y, self.left.x, self.left.y))
			if self.right.value == -1:
				self.right.delete()
			else:
				self.parentWindow.knotCoordinates.append((self.x, self.y, self.right.x, self.right.y))
		else:
			self.x = int((self.r-.5) * ((self.parentWindow.frameTree.width()-20) / 2**(self.parentWindow.rootTree.maxI))) + 10


		self.label.setGeometry(self.x-int(self.parentWindow.knotsSize/2), self.y-int(self.parentWindow.knotsSize/2)+15, self.parentWindow.knotsSize, self.parentWindow.knotsSize)
		self.label.setToolTip(f"Value: {self.value}\nParent: {self.parentKnot.value if self.parentKnot else 'No parent'}\nLeft Child: {self.left.value if self.left else 'No Left Child'} | Right Child: {self.right.value if self.right else 'No Right Child'}\nAltitude: {self.i} | Rank: {self.r}")
		self.label.setText(str(self.value))
		return self.x

	def delete(self):
		if self.label:
			self.label.setParent(None)
		if self.left:
			self.left.delete()
		if self.right:
			self.right.delete()
		if self.parentKnot.left == self:
			self.parentKnot.left = None
		elif self.parentKnot.right == self:
			self.parentKnot.right = None

	def search(self, toFind):
		if self.value == toFind:
			return self
		if self.value > toFind:
			if self.left:
				l = self.left.search(toFind)
				if l: return l
		if self.value < toFind:
			if self.right:
				r = self.right.search(toFind)
				if r: return r
		return False

	def __str__(self):
		return f"{('('+str(self.left)+')') if self.left else '' }{self.value}{('('+str(self.right)+')') if self.right else '' }"


class visualAddThread(QThread):
	def __init__(self, parent, toAdd):
		super().__init__()
		self.parentWindow = parent
		self.toAdd = toAdd

	def run(self):
		k = self.parentWindow.rootTree
		self.added = False
		while not self.added:
			sleep(.5)
			if self.toAdd == k.value:
				break
			elif self.toAdd < k.value:
				if k.left:
					self.parentWindow.selected = [k.x, k.y, k.left.x, k.left.y]
					self.parentWindow.update()
					sleep(.5)
					k = k.left
				else:
					self.added = (k, 'left')
			elif self.toAdd > k.value:
				if k.right:
					self.parentWindow.selected = [k.x, k.y, k.right.x, k.right.y]
					self.parentWindow.update()
					sleep(.5)
					k = k.right
				else:
					self.added = (k, 'right')

class visualRemoveThread(QThread):
	def __init__(self, parent, toRemove):
		super().__init__()
		self.parentWindow = parent
		self.toRemove = toRemove

	def run(self):
		k = self.parentWindow.rootTree.search(self.toRemove)
		if k.parentKnot.left == k:
			k.parentKnot.left = None
		else:
			k.parentKnot.right = None
		ks = [k]
		self.labels = []
		if k:
			while ks != []:
				sleep(.5)
				k = ks.pop(0)
				if k.label:
					self.labels.append(k.label)
				if k.left:
					self.parentWindow.selected = [k.x, k.y, k.left.x, k.left.y]
					self.parentWindow.update()
					sleep(.5)
					ks.append(k.left)
					k.left = None
				if k.right:
					self.parentWindow.selected = [k.x, k.y, k.right.x, k.right.y]
					self.parentWindow.update()
					sleep(.5)
					ks.append(k.right)
					k.right = None

			self.deleted = True
		else:
			self.deleted = False


class visualSearchThread(QThread):
	def __init__(self, parent, toFind):
		super().__init__()
		self.parentWindow = parent
		self.toFind = toFind

	def run(self):
		k = self.parentWindow.rootTree
		while k.value != self.toFind and (k.left or k.right):
			sleep(.5)
			if k.value > self.toFind and k.left:
				self.parentWindow.selected = [k.x, k.y, k.left.x, k.left.y]
				self.parentWindow.update()
				sleep(.5)
				k = k.left
			elif k.value < self.toFind and k.right:
				self.parentWindow.selected = [k.x, k.y, k.right.x, k.right.y]
				self.parentWindow.update()
				sleep(.5)
				k = k.right
			else:
				break
		self.found = True if k.value == self.toFind else False

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Tree Viewer v2")
		self.setGeometry(0,0,800,600)
		self.setObjectName("Layer1")

		self.offsets = [0, 35, 0, 2]
		self.removeThread = None
		self.searchThread = None
		self.addThread = None
		self.selected = None
		self.knotsSize = 30
		self.fontSize = 10

		self.windowError = QMessageBox()
		self.windowError.setIcon(QMessageBox.Information)
		self.windowError.setObjectName("Error")

		self.setUI()

	def setUI(self):
		s = QGraphicsDropShadowEffect()
		s.setColor(QColor("#000000"))
		s.setBlurRadius(5)
		s.setOffset(1,1)
		self.frameTree = QFrame(self)
		self.frameTree.setGeometry(0, 0, 600, 600)

		self.defaultTree()

		self.frameInfo = QFrame(self)
		self.frameInfo.setGeometry(605, 5, 190, 590)
		self.frameInfo.setObjectName("Layer2")
		self.frameInfo.setGraphicsEffect(s)

		self.labelAddKnot = QLabel("Add Knot:", self.frameInfo)
		self.labelAddKnot.setGeometry(10, 150, 60, 30)
		self.labelAddKnot.setAlignment(Qt.AlignCenter)
		self.labelAddKnot.setObjectName("Layer2NoBG")
		self.labelAddKnot.setFont(QFont("Arial", 15))
		self.entryAddKnot = QLineEdit(self.frameInfo)
		self.entryAddKnot.setGeometry(120, 150, 60, 30)
		self.entryAddKnot.setAlignment(Qt.AlignCenter)
		self.entryAddKnot.setObjectName("Layer2")
		self.entryAddKnot.setFont(QFont("Arial", 15))
		self.entryAddKnot.setValidator(QRegExpValidator(QRegExp("[0-9]+"), self.entryAddKnot))
		self.buttonAddKnot = QPushButton(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton), '', self.frameInfo)
		self.buttonAddKnot.setGeometry(180, 150, 60, 30)
		self.buttonAddKnot.setObjectName("Layer2")
		self.buttonAddKnot.clicked.connect(self.addKnot)

		self.labelVisualizeKnot = QLabel("Search for:", self.frameInfo)
		self.labelVisualizeKnot.setGeometry(10, 300, 60, 30)
		self.labelVisualizeKnot.setAlignment(Qt.AlignCenter)
		self.labelVisualizeKnot.setObjectName("Layer2NoBG")
		self.labelVisualizeKnot.setFont(QFont("Arial", 15))
		self.entryVisualizeKnot = QLineEdit(self.frameInfo)
		self.entryVisualizeKnot.setGeometry(70, 300, 60, 30)
		self.entryVisualizeKnot.setAlignment(Qt.AlignCenter)
		self.entryVisualizeKnot.setObjectName("Layer2")
		self.entryVisualizeKnot.setFont(QFont("Arial", 15))
		self.entryVisualizeKnot.setValidator(QRegExpValidator(QRegExp("[0-9]+"), self.entryVisualizeKnot))
		self.buttonVisualizeStartPause = QPushButton(QApplication.style().standardIcon(QStyle.SP_MediaPlay), '', self.frameInfo)
		self.buttonVisualizeStartPause.setGeometry(130, 300, 60, 30)
		self.buttonVisualizeStartPause.setObjectName("Layer2")
		self.buttonVisualizeStartPause.clicked.connect(self.startSearch)

		self.labelRemoveKnot = QLabel("Remove\nKnot:", self.frameInfo)
		self.labelRemoveKnot.setGeometry(10, 450, 60, 40)
		self.labelRemoveKnot.setAlignment(Qt.AlignCenter)
		self.labelRemoveKnot.setObjectName("Layer2NoBG")
		self.labelRemoveKnot.setFont(QFont("Arial", 15))
		self.entryRemoveKnot = QLineEdit(self.frameInfo)
		self.entryRemoveKnot.setGeometry(70, 450, 60, 30)
		self.entryRemoveKnot.setAlignment(Qt.AlignCenter)
		self.entryRemoveKnot.setObjectName("Layer2")
		self.entryRemoveKnot.setFont(QFont("Arial", 15))
		self.entryRemoveKnot.setValidator(QRegExpValidator(QRegExp("[0-9]+"), self.entryRemoveKnot))
		self.buttonRemoveKnot = QPushButton(QApplication.style().standardIcon(QStyle.SP_TrashIcon), '', self.frameInfo)
		self.buttonRemoveKnot.setGeometry(130, 450, 60, 30)
		self.buttonRemoveKnot.setObjectName("Layer2")
		self.buttonRemoveKnot.clicked.connect(self.deleteKnot)

		self.labelSize = QLabel("Change Knots Size:", self.frameInfo)
		self.labelSize.setGeometry(10, 540, 180, 30)
		self.labelSize.setAlignment(Qt.AlignCenter)
		self.labelSize.setObjectName("Layer2NoBG")
		self.labelSize.setFont(QFont("Arial", 15))
		self.buttonMinusSize = QPushButton("-", self.frameInfo)
		self.buttonMinusSize.setGeometry(10, 560, 90, 30)
		self.buttonMinusSize.setObjectName("Layer2")
		self.buttonMinusSize.setFont(QFont("Arial", 20))
		self.buttonMinusSize.clicked.connect(lambda: self.changeSize('-'))
		self.buttonMinusSize.setAutoRepeat(True)
		self.buttonPlusSize = QPushButton("+", self.frameInfo)
		self.buttonPlusSize.setGeometry(170, 560, 90, 30)
		self.buttonPlusSize.setObjectName("Layer2")
		self.buttonPlusSize.setFont(QFont("Arial", 20))
		self.buttonPlusSize.clicked.connect(lambda: self.changeSize('+'))
		self.buttonPlusSize.setAutoRepeat(True)

	def defaultTree(self):
		self.rootTree = sortedKnot(20, parent=self)
		self.rootTree.addSorted(5)
		self.rootTree.addSorted(3)
		self.rootTree.addSorted(12)
		self.rootTree.addSorted(8)
		self.rootTree.addSorted(6)
		self.rootTree.addSorted(13)
		self.rootTree.addSorted(25)
		self.rootTree.addSorted(21)
		self.rootTree.addSorted(28)
		self.rootTree.addSorted(29)
		self.rootTree.addSorted(24)
		self.rootTree.update()

	def deleteKnot(self):
		if self.entryRemoveKnot.text():
			if int(self.entryRemoveKnot.text()) != self.rootTree.value:
				if not self.removeThread:
					self.buttonRemoveKnot.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogDiscardButton))
					self.removeThread = visualRemoveThread(self, int(self.entryRemoveKnot.text()))
					self.removeThread.finished.connect(self.deleteRemoveThread)
					self.removeThread.start()
				else:
					self.deleteRemoveThread()
			else:
				self.showError("You can't remove the root", "Deletion Error")
		else:
			self.showError("You have to enter a valid value to remove", "Deletion Error")


	def startSearch(self):
		if self.entryVisualizeKnot.text():
			if not self.searchThread:
				self.buttonVisualizeStartPause.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaStop))
				self.searchThread = visualSearchThread(self, int(self.entryVisualizeKnot.text()))
				self.searchThread.finished.connect(self.deleteSearchThread)
				self.searchThread.start()
			else:
				self.deleteSearchThread()
		else:
			self.showError("You have to enter a valid value to search for", "Search Error")

	def addKnot(self):
		if self.entryAddKnot.text():
			if not self.addThread:
				self.buttonAddKnot.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
				self.addThread = visualAddThread(self, int(self.entryAddKnot.text()))
				self.addThread.finished.connect(self.deleteAddThread)
				self.addThread.start()
			else:
				self.deleteAddThread()
		else:
			self.showError("You have to enter a valid value to insert", "Insertion Error")

	def deleteRemoveThread(self):
		if self.removeThread:
			self.buttonRemoveKnot.setIcon(QApplication.style().standardIcon(QStyle.SP_TrashIcon))
			for i in self.removeThread.labels: i.setParent(None)
			self.showError("The knot you wanted to remove has been succesfully annihilated", "Knot Deleted") if self.removeThread.deleted else self.showError("The knot you tried to remove encountered an error", "Deletion Error")
			if self.removeThread.isRunning(): self.removeThread.terminate()
			self.removeThread = None
			self.selected = None
			self.rootTree.update()
			self.update()

	def deleteAddThread(self):
		if self.addThread:
			self.buttonAddKnot.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton))
			if self.addThread.added:
				self.addThread.added[0].addLeft(self.addThread.toAdd) if self.addThread.added[1] == 'left' else self.addThread.added[0].addRight(self.addThread.toAdd)
				self.addThread.added[0].left.label.show() if self.addThread.added[1] == 'left' else self.addThread.added[0].right.label.show()
				self.showError("Your knot has been added with success", "Added Knot")
			else:
				self.showError("The value you tried to insert is already taken", "Value Error")
			if self.addThread.isRunning(): self.addThread.terminate()
			self.addThread = None
			self.selected = None
			self.rootTree.update()
			self.update()

	def deleteSearchThread(self):
		if self.searchThread:
			self.buttonVisualizeStartPause.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))
			self.showError("The knot you were searching for has been found", "Knot Found") if self.searchThread.found else self.showError("The knot you were searching for was not found", "Knot Not Found")
			if self.searchThread.isRunning(): self.searchThread.terminate()
			self.searchThread = None
			self.selected = None
			self.update()

	def changeSize(self, mode):
		if mode == '-':
			if self.fontSize-2 >= 10:
				self.fontSize -= 2
				self.knotsSize -= 4
				for i in self.frameTree.children():
					i.setGeometry(i.x()+2, i.y()+2, self.knotsSize, self.knotsSize)
					i.setFont(QFont("Arial", self.fontSize))
					self.offsets[0] -= 0
					self.offsets[1] -= .18
					self.offsets[2] += 0
					self.offsets[3] += .18
		elif mode == '+':
			if self.fontSize+2 <= 42:
				self.fontSize += 2
				self.knotsSize += 4
				for i in self.frameTree.children():
					i.setGeometry(i.x()-2, i.y()-2, i.width()+4, i.height()+4)
					i.setFont(QFont("Arial", self.fontSize))
					self.offsets[0] += 0
					self.offsets[1] += .18
					self.offsets[2] -= 0
					self.offsets[3] -= .18
		self.update()

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(QPen(QColor(3,218,197), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
		for cos in self.knotCoordinates:
			painter.drawLine(int(cos[0]+self.offsets[0]), int(cos[1]+self.offsets[1]), int(cos[2]+self.offsets[2]), int(cos[3]+self.offsets[3]))
		if self.selected:
			painter.setPen(QPen(QColor("#D8DEE9"), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
			painter.drawLine(int(self.selected[0]+self.offsets[0]), int(self.selected[1]+self.offsets[1]), int(self.selected[2]+self.offsets[2]), int(self.selected[3]+self.offsets[3]))
		painter.end()

	def resizeEvent(self, event):
		self.frameTree.setGeometry(0, 0, int(6*(self.width()/8)), self.height())
		self.frameInfo.setGeometry(int(6*(self.width()/8))+5, 10, int(2*(self.width()/8))-10, self.height()-20)

		self.labelAddKnot.setGeometry(10, int(self.frameInfo.height()/4)-30, int((self.frameInfo.width()-20)/3), 30)
		self.entryAddKnot.setGeometry(10 + int((self.frameInfo.width()-20)/3), int(self.frameInfo.height()/4)-30, int((self.frameInfo.width()-20)/3), 30)
		self.buttonAddKnot.setGeometry(10 + 2*int((self.frameInfo.width()-20)/3), int(self.frameInfo.height()/4)-30, int((self.frameInfo.width()-20)/3), 30)

		self.labelVisualizeKnot.setGeometry(10, int(self.frameInfo.height()/2), int((self.frameInfo.width()-20)/3), 30)
		self.entryVisualizeKnot.setGeometry(10 + int((self.frameInfo.width()-20)/3), int(self.frameInfo.height()/2), int((self.frameInfo.width()-20)/3), 30)
		self.buttonVisualizeStartPause.setGeometry(10 + 2*int((self.frameInfo.width()-20)/3), int(self.frameInfo.height()/2), int((self.frameInfo.width()-20)/3), 30)

		self.labelRemoveKnot.setGeometry(10, 3*int(self.frameInfo.height()/4)-10, int((self.frameInfo.width()-20)/3), 50)
		self.entryRemoveKnot.setGeometry(10 + int((self.frameInfo.width()-20)/3), 3*int(self.frameInfo.height()/4), int((self.frameInfo.width()-20)/3), 30)
		self.buttonRemoveKnot.setGeometry(10 + 2*int((self.frameInfo.width()-20)/3), 3*int(self.frameInfo.height()/4), int((self.frameInfo.width()-20)/3), 30)

		self.labelSize.setGeometry(10, self.frameInfo.height()-70, self.frameInfo.width()-30, 30)
		self.buttonPlusSize.setGeometry(int((self.frameInfo.width()-20)/2+10), self.frameInfo.height()-40, int((self.frameInfo.width()-30)/2), 30)
		self.buttonMinusSize.setGeometry(10, self.frameInfo.height()-40, int((self.frameInfo.width()-30)/2), 30)

		self.rootTree.update()

	def showError(self, text, title):
		self.windowError.setText(text)
		self.windowError.setWindowTitle(title)
		self.windowError.show()





app = QApplication(argv)
mainwindow = MainWindow()
with open("darkTheme.css", "r") as file: mainwindow.setStyleSheet(file.read())
# with open("lightTheme.css", "r") as file: mainwindow.setStyleSheet(file.read())
mainwindow.showMaximized()

exit(app.exec_())
