from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, qApp, QFrame, QDialog, QComboBox, QLineEdit, QAction, QMessageBox
from PyQt5.QtGui import QCursor, QPainter, QPen, QColor
from PyQt5.QtCore import Qt

from sys import exit, argv

class Knot():
	ids = 0
	def __init__(self, name, left=False, right=False):
		self.name = name
		self.ids = Knot.ids
		Knot.ids += 1
		self.left = left
		self.right = right
		self.label = None

	def getLen(self):
		l = 1
		if self.left: l += self.left.getLen()
		if self.right: l += self.right.getLen()
		return l

	def getAlt(self):
		a, l, r = 1, 0, 0
		if self.left: l = self.left.getAlt()
		if self.right: r = self.right.getAlt()
		return a+l if l > r else a+r

	def isLeaf(self):
		return False if self.left or self.right else True

	def setLabel(self, r=1):
		self.y = int(self.i * (600 / (self.parent.tree.alt+1)))
		self.r = r
		if not self.isLeaf():
			lc = self.left.setLabel(2*self.r-1)
			rc = self.right.setLabel(2*self.r)
			self.x = int((lc[0] + rc[0]) / 2)

			if self.left.name == 'Temp': self.left = False
			if self.right.name == 'Temp': self.right = False
		else:
			self.x = int((r-.5) * (600 / 2**(self.parent.tree.alt)))

		if self.name != 'Temp':
			if self.label:
				self.label.setParent(None)
				self.label = None
			self.label = QLabel(self.name, self.parent.frameTree)
			self.label.setAlignment(Qt.AlignCenter)
			self.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			self.label.setToolTip(f"Name: {self.name}\nLC: {self.left if self.left else 'N/A'}, RC: {self.right if self.right else 'N/A'}\nAltitude: {self.i}\nRank: {self.r}")
			self.label.setGeometry(self.x-10, self.y+10, 20, 20)
			self.label.show()

		return self.x, self.y

	def traceTree(self):
		if self.left:
			self.parent.knotCoordinates.append((self.x, self.y+30, self.left.x, self.left.y+10))
			self.left.traceTree()
		if self.right:
			self.parent.knotCoordinates.append((self.x, self.y+30, self.right.x, self.right.y+10))
			self.right.traceTree()

	def search(self, toFind):
		if self.name == toFind: return (True, self)
		if self.left:
			l = self.left.search(toFind)
			if l[0]: return l
		if self.right:
			r = self.right.search(toFind)
			if r[0]: return r
		return [False]

	def setInfos(self, parent, i=0, parentKnot=None):
		self.parent = parent
		self.parentKnot = parentKnot
		self.i = i
		if i < self.parent.tree.alt:
			if not self.left: self.left = Knot('Temp')
			if not self.right: self.right = Knot('Temp')
			self.left.setInfos(parent, i+1, self)
			self.right.setInfos(parent, i+1, self)

	def removeKnot(self, toFind):
		if self.left:
			if self.left.name == toFind:
				self.left.clearChildren()
				self.left = None
			else: self.left.removeKnot(toFind)

		if self.right:
			if self.right.name == toFind:
				self.right.clearChildren()
				self.right = None
			else: self.right.removeKnot(toFind)

	def clearChildren(self):
		self.label.setParent(None)
		# del self.label
		if self.left: self.left.clearChildren()
		if self.right: self.right.clearChildren()




class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Tree Viewer")
		self.setFixedHeight(600)
		self.setFixedWidth(800)

		self.actionUp = QAction()
		self.actionUp.triggered.connect(self.selecUp)
		self.actionUp.setShortcut('Z')
		self.actionDown = QAction()
		self.actionDown.triggered.connect(self.selecDown)
		self.actionDown.setShortcut('S')
		self.actionLeft = QAction()
		self.actionLeft.triggered.connect(self.selecLeft)
		self.actionLeft.setShortcut('Q')
		self.actionRight = QAction()
		self.actionRight.triggered.connect(self.selecRight)
		self.actionRight.setShortcut('D')
		self.actionAddKnot = QAction()
		self.actionAddKnot.triggered.connect(self.addKnot)
		self.actionAddKnot.setShortcut('A')
		self.actionRemoveKnot = QAction()
		self.actionRemoveKnot.triggered.connect(self.removeKnot)
		self.actionRemoveKnot.setShortcut('R')

		self.addAction(self.actionUp)
		self.addAction(self.actionDown)
		self.addAction(self.actionLeft)
		self.addAction(self.actionRight)
		self.addAction(self.actionAddKnot)
		self.addAction(self.actionRemoveKnot)


		self.tree = Knot('A', left=Knot('B', left=Knot('D'), right=Knot('E')), right=Knot('C', left=Knot('F'), right=Knot('G')))
		self.setUI()

	def setUI(self):
		self.frameInfos = QFrame(self)
		self.frameInfos.setGeometry(600, 0, 200, 600)
		self.frameInfos.setStyleSheet(".QFrame{border: 2px solid rgb(144,144,144);\nborder-radius: 10px;}")

		self.frameTree = QFrame(self)
		self.frameTree.setGeometry(0, 0, 600, 600)
		self.frameTree.setStyleSheet(".QFrame{border: 2px solid rgb(144,144,144);\nborder-radius: 10px;}")
		
		self.updateTree()

		self.windowAddKnot = QDialog(self, Qt.Drawer)
		self.windowAddKnot.setFixedWidth(400)
		self.windowAddKnot.setFixedHeight(200)
		self.windowAddKnot.labelKnotName = QLabel(f'Knot Name: {self.selected.name}', self.windowAddKnot)
		self.windowAddKnot.labelKnotName.setAlignment(Qt.AlignCenter)
		self.windowAddKnot.labelKnotName.setGeometry(110, 10, 180, 20)
		self.windowAddKnot.labelSide = QLabel('Choose which child side:', self.windowAddKnot)
		self.windowAddKnot.labelSide.setGeometry(10, 40, 180, 20)
		self.windowAddKnot.comboSide = QComboBox(self.windowAddKnot)
		self.windowAddKnot.comboSide.addItems(['left', 'right'] if not self.selected.left and not self.selected.right else ['left'] if self.selected.right else ['right'])
		self.windowAddKnot.comboSide.setGeometry(210, 40, 180, 20)
		self.windowAddKnot.labelKnot = QLabel('Choose Knot\'s name:', self.windowAddKnot)
		self.windowAddKnot.labelKnot.setGeometry(10, 70, 180, 20)
		self.windowAddKnot.entryKnot = QLineEdit(self.windowAddKnot)
		self.windowAddKnot.entryKnot.setGeometry(210, 70, 180, 20)
		self.windowAddKnot.buttonValidate = QPushButton('Add Knot', self.windowAddKnot)
		self.windowAddKnot.buttonValidate.setGeometry(110, 130, 180, 20)
		self.windowAddKnot.buttonValidate.clicked.connect(lambda: self.verifyAddition(self.windowAddKnot.comboSide.currentText(), self.windowAddKnot.entryKnot.text()))

		self.windowError = QMessageBox()
		self.windowError.setIcon(QMessageBox.Information)


		self.labelKnotName = QLabel(f'Knot Name: {self.selected.name}', self.frameInfos)
		self.labelKnotName.setStyleSheet('border: 2px solid rgb(144,144,144);\nborder-radius: 15px;')
		self.labelKnotName.setGeometry(10, 10, 180, 30)
		self.labelKnotName.setAlignment(Qt.AlignCenter)
		self.labelKnotLeaf = QLabel(f'Knot is leaf: {self.selected.isLeaf()}', self.frameInfos)
		self.labelKnotLeaf.setGeometry(10, 40, 180, 20)
		self.labelKnotAlt = QLabel(f'Knot Altitude: {self.selected.i}', self.frameInfos)
		self.labelKnotAlt.setGeometry(10, 70, 180, 20)
		self.labelKnotRank = QLabel(f'Knot Rank: {self.selected.r}', self.frameInfos)
		self.labelKnotRank.setGeometry(10, 100, 180, 20)

		self.labelKnotParent = QLabel(f'Parent Name: {self.selected.parentKnot.name}' if self.selected.parentKnot else 'Root Knot', self.frameInfos)
		self.labelKnotParent.setGeometry(10, 150, 180, 20)
		self.labelKnotChildLeft = QLabel(f'Left Child Name: {self.selected.left.name}' if self.selected.left else 'No Left Child', self.frameInfos)
		self.labelKnotChildLeft.setGeometry(10, 180, 180, 20)
		self.labelKnotChildRight = QLabel(f'Right Child Name: {self.selected.right.name}' if self.selected.right else 'No Right Child', self.frameInfos)
		self.labelKnotChildRight.setGeometry(10, 210, 180, 20)

		self.buttonRemoveKnot = QPushButton('Remove Knot', self.frameInfos)
		self.buttonRemoveKnot.setFocusPolicy(Qt.NoFocus)
		self.buttonRemoveKnot.setGeometry(10, 240, 180, 20)
		self.buttonRemoveKnot.clicked.connect(self.removeKnot)

		self.buttonAddKnot = QPushButton('Add Child', self.frameInfos)
		self.buttonAddKnot.setFocusPolicy(Qt.NoFocus)
		self.buttonAddKnot.setGeometry(10, 270, 180, 20)
		self.buttonAddKnot.clicked.connect(self.addKnot)

	def removeKnot(self):
		if self.selected == self.tree:
			self.showError('Cannot remove root knot', 'Root Error')
		else:
			self.knotCoordinates = []
			self.tree.removeKnot(self.selected.name)
			self.tree.traceTree()
			self.selected = self.tree
			self.selectKnot()
			self.frameTree.update()

	def addKnot(self):
		if self.selected.left and self.selected.right:
			self.showError('Knot has already two children', 'Children Error')
		else:
			self.windowAddKnot.comboSide.clear()
			self.windowAddKnot.comboSide.addItems(['left', 'right'] if (not self.selected.left and not self.selected.right) else ['left'] if self.selected.right else ['right'])
			self.windowAddKnot.labelKnotName.setText(f'Knot Name: {self.selected.name}')
			self.windowAddKnot.setWindowModality(Qt.ApplicationModal)
			self.windowAddKnot.setFocusPolicy(Qt.StrongFocus)
			self.windowAddKnot.activateWindow()
			self.windowAddKnot.setFocus(True)
			self.windowAddKnot.raise_()
			self.windowAddKnot.show()

	def verifyAddition(self, side, name):
		if name:
			s = self.tree.search(name)
			if not s[0]:
				if side == 'left': self.selected.left = Knot(name)
				else: self.selected.right = Knot(name)
				self.windowAddKnot.hide()
			elif s[1] != self.tree:
				buttonReply = QMessageBox.question(self.windowAddKnot, f'{name} is already in use', f"Do you want to transfer children to {self.selected.name} ?\n{name} wille be the {side} child of {self.selected.name}", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if buttonReply == QMessageBox.Yes:
					if side == 'left':
						if s[1].parentKnot.left:
							if s[1].parentKnot.left.name == name:
								self.selected.left = s[1].parentKnot.left
								s[1].parentKnot.left = None
						if s[1].parentKnot.right:
							if s[1].parentKnot.right.name == name:
								self.selected.left = s[1].parentKnot.right
								s[1].parentKnot.right = None
						self.selected.left.parent = self.selected

					else:
						if s[1].parentKnot.left and s[1].parentKnot.left.name == name:
							self.selected.right = s[1].parentKnot.left
							s[1].parentKnot.left = None

						elif s[1].parentKnot.right and s[1].parentKnot.right.name == name:
							self.selected.right = s[1].parentKnot.right
							s[1].parentKnot.right = None
						self.selected.right.parent = self.selected
					self.windowAddKnot.hide()
			else:
				self.showError('You can\'t modify tree root', 'Root Error')

			self.activateWindow()
			self.updateTree()
			self.selectKnot()

	def updateTree(self):
		self.knotCoordinates = []
		self.selected = self.tree
		self.tree.alt = self.tree.getAlt()-1
		self.tree.setInfos(self)
		self.tree.setLabel()
		self.tree.traceTree()
		self.frameTree.update()
		self.tree.label.setStyleSheet("border: 2px solid rgb(0,0,144);\nborder-radius:10px;")

	def paintEvent(self, e):
		self.painter = QPainter(self)
		for cos in self.knotCoordinates:
			if self.selected.x == cos[0] and self.selected.y+30 == cos[1]:
				self.painter.setPen(QPen(QColor(144,0,0), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
			elif self.selected.x == cos[2] and self.selected.y+10 == cos[3]:
				self.painter.setPen(QPen(QColor(0,144,0), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
			else:
				self.painter.setPen(QPen(QColor(0,0,144), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
			self.painter.drawLine(cos[0], cos[1], cos[2], cos[3])
		self.painter.end()

	def mousePressEvent(self, event):
		pos = QCursor.pos()
		w = app.widgetAt(pos)
		if w != self.frameTree and w is not self.selected.label and 0 <= pos.x() <= 600 and 0 <= pos.y() <= 600:
			self.selected.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			s = self.tree.search(w.text())
			self.selected = s[1]
			self.selectKnot()

	def selectKnot(self):
		self.selected.label.setStyleSheet("border: 2px solid rgb(0,0,144);\nborder-radius:10px;")
		self.labelKnotName.setText(f"Knot Name: {self.selected.name}")
		self.labelKnotLeaf.setText(f"Knot is Leaf: {self.selected.isLeaf()}")
		self.labelKnotAlt.setText(f"Knot Altitude: {self.selected.i}")
		self.labelKnotRank.setText(f"Knot Rank: {self.selected.r}")
		self.labelKnotParent.setText(f'Parent Name: {self.selected.parentKnot.name}' if self.selected.parentKnot else 'Root Knot')
		self.labelKnotChildLeft.setText(f"Left Child Name: {self.selected.left.name}" if self.selected.left else f"No Left Child")
		self.labelKnotChildRight.setText(f"Right Child Name: {self.selected.right.name}" if self.selected.right else f"No Right Child")
		self.update()

	def selecUp(self):
		if self.selected.parentKnot:
			self.selected.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			self.selected = self.selected.parentKnot
			self.selectKnot()
	def selecLeft(self):
		if self.selected.parentKnot and self.selected.r != 1:
			k = self.selected.parentKnot
			checked = [self.selected.name]
			while self.selected.i != k.i:
				last = k
				if k.right and (k.right.name not in checked and k.right.r < self.selected.r):
					checked.append(k.name)
					k = k.right
				elif k.left and (k.left.name not in checked):
					checked.append(k.name)
					k = k.left
				elif k.parentKnot and (k.parentKnot.name not in checked):
					checked.append(k.name)
					k = k.parentKnot
				elif last == k:
					k = self.selected
			self.selected.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			self.selected = k
			self.selectKnot()
	def selecRight(self):
		if self.selected.parentKnot and self.selected.r != 2**self.selected.i:
			k = self.selected.parentKnot
			checked = [self.selected.name]
			while self.selected.i != k.i:
				last = k
				if k.left and (k.left.name not in checked and k.left.r > self.selected.r):
					checked.append(k.name)
					k = k.left
				elif k.right and (k.right.name not in checked):
					checked.append(k.name)
					k = k.right
				elif k.parentKnot and (k.parentKnot.name not in checked):
					checked.append(k.name)
					k = k.parentKnot
				elif last == k:
					k = self.selected
			self.selected.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			self.selected = k
			self.selectKnot()
	def selecDown(self):
		if self.selected.left:
			self.selected.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			self.selected = self.selected.left
			self.selectKnot()
		elif self.selected.right:
			self.selected.label.setStyleSheet("border: 2px solid rgb(144,144,144);\nborder-radius:10px;")
			self.selected = self.selected.right
			self.selectKnot()


	def showError(self, text, title):
		self.windowError.setText(text)
		self.windowError.setWindowTitle(title)
		self.windowError.show()
app = QApplication(argv)

mw = MainWindow()
mw.show()

exit(app.exec_())