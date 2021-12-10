import sys
import cv2
import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QComboBox, QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib

class BlemishDetectionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Blemish Detection Tuner")
        self._createWidgets()
        self._initPara()
        self._updateEditTextVisibility(self.cboxDetectionMode.currentIndex())


    def _initPara(self):
        self._isDUTLoaded = False
        self._isRefLoaded = False
        self._isAppliedThreshold = False
        self.dutImagePath = None
        self.refImagePath = None

    def _createWidgets(self):
        hboxLayout = QHBoxLayout()
        vboxLayout = QVBoxLayout()

        self.cboxDetectionMode = QComboBox()
        self.cboxDetectionMode.addItem("Single Mode")
        self.cboxDetectionMode.addItem("Dual Mode")
        self.cboxDetectionMode.currentIndexChanged[int].connect(self._updateEditTextVisibility)

        self.btnLoadDUTImage = QPushButton("Load DUT Image")
        self.btnLoadDUTImage.clicked.connect(self._loadDUTImage)
        self.btnLoadDUTImage.setCheckable(True)
        self.btnLoadDUTImage.setChecked(False)
        self.labelDUTImagePath = QLabel("")
        self.btnLoadRefImage = QPushButton("Load Ref Image")
        self.btnLoadRefImage.clicked.connect(self._loadRefImage)
        self.labelRefImagePath = QLabel("")

        self.cboxFilterType = QComboBox()
        self.cboxFilterType.addItem("ButterWorth")
        self.cboxFilterType.addItem("Gaussian")
        self.cboxFilterType.addItem("LoG")
        self.cboxFilterType.currentIndexChanged[int].connect(self._updateEditTextVisibility)

        self.cboxFilterBW = QComboBox()
        self.cboxFilterBW.addItem("Low Pass")
        self.cboxFilterBW.addItem("High Pass")
        self.cboxFilterBW.addItem("Band Pass")
        self.cboxFilterBW.currentIndexChanged[int].connect(self._updateEditTextVisibility)

        self.lineEditCutInFrequency = QLineEdit()
        self.lineEditCutOffFrequency = QLineEdit()
        self.lineEditThreshold = QLineEdit()
        self.lineEditSigmaX = QLineEdit()
        self.lineEditSigmaY = QLineEdit()
        self.lineEditSigmaX2 = QLineEdit()
        self.lineEditSigmaY2 = QLineEdit()
        self.labelCutIn = QLabel("Cut in")
        self.labelCutOff = QLabel("Cut off")
        self.labelSigmaX = QLabel("Sigma X")
        self.labelSigmaY = QLabel("Sigma Y")
        self.labelSigmaX2 = QLabel("Sigma X2")
        self.labelSigmaY2 = QLabel("Sigma Y2")
        self.labelLogDir = QLabel("Direction")
        self.cboxLoGDir = QComboBox()
        self.cboxLoGDir.addItem("Virtical")
        self.cboxLoGDir.addItem("Horzontal")
        self.cboxLoGDir.addItem("Circular")
        self.labelTreshold = QLabel("Threshold")

        detectionModeHboxLayout = QGridLayout()
        detectionModeHboxLayout.addWidget(QLabel("Detection Mode:"), 0, 1, 1, 1)
        detectionModeHboxLayout.addWidget(self.cboxDetectionMode, 0, 2, 1, 1)
        detectionModeHboxLayout.addWidget(QLabel(""), 0, 3, 1, 5)
        
        '''
            TODO: Fix bug: btnLoadDUTImage keeps being pressed
        '''
        loadImageHboxLayout = QGridLayout()
        loadImageHboxLayout.addWidget(self.btnLoadDUTImage, 0, 1, 1, 1)
        loadImageHboxLayout.addWidget(self.labelDUTImagePath, 0, 2, 1, 7)
        loadImageHboxLayout.addWidget(self.btnLoadRefImage, 1, 1, 1, 1)
        loadImageHboxLayout.addWidget(self.labelRefImagePath, 1, 2, 1, 7)

        '''
            dual mode parameter
        '''
        dualModeParaGridLayout = QGridLayout()
        self.labelRatio = QLabel("Ratio")
        self.lineEditRatio = QLineEdit("0.99")
        self.labelRoiW = QLabel("ROI Width")
        self.lineEditRoiW = QLineEdit("100")
        dualModeParaGridLayout.addWidget(self.labelRatio, 0, 1, 1, 1)
        dualModeParaGridLayout.addWidget(self.lineEditRatio, 0, 2, 1, 1)
        dualModeParaGridLayout.addWidget(self.labelRoiW, 0, 3, 1, 1)
        dualModeParaGridLayout.addWidget(self.lineEditRoiW, 0, 4, 1, 1)
        dualModeParaGridLayout.addWidget(QLabel(""), 0, 5, 1, 4)

        hboxLayout.addWidget(QLabel("Filter Type:"))
        hboxLayout.addWidget(self.cboxFilterType)
        hboxLayout.addWidget(QLabel("Band Option:"))
        hboxLayout.addWidget(self.cboxFilterBW)
        hboxLayout.addWidget(self.labelCutIn)
        hboxLayout.addWidget(self.lineEditCutInFrequency)
        hboxLayout.addWidget(self.labelCutOff)
        hboxLayout.addWidget(self.lineEditCutOffFrequency)
        hboxLayout.addWidget(self.labelSigmaX)
        hboxLayout.addWidget(self.lineEditSigmaX)
        hboxLayout.addWidget(self.labelSigmaY)
        hboxLayout.addWidget(self.lineEditSigmaY)       
        hboxLayout.addWidget(self.labelSigmaX2)
        hboxLayout.addWidget(self.lineEditSigmaX2)
        hboxLayout.addWidget(self.labelSigmaY2)
        hboxLayout.addWidget(self.lineEditSigmaY2)  
        hboxLayout.addWidget(self.labelLogDir)
        hboxLayout.addWidget(self.cboxLoGDir)
        hboxLayout.addWidget(self.labelTreshold)
        hboxLayout.addWidget(self.lineEditThreshold)

        vboxLayout.addLayout(detectionModeHboxLayout)
        vboxLayout.addLayout(loadImageHboxLayout)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(dualModeParaGridLayout)
        figuresLayout = self._createCanvasLayout()
        vboxLayout.addLayout(figuresLayout)
        
        self.btnCalculate = QPushButton("Detect")
        self.btnCalculate.clicked.connect(self._calculate)
        vboxLayout.addWidget(self.btnCalculate)
        self.setLayout(vboxLayout)

    def _updateEditTextVisibility(self, option):
        filterType = self.cboxFilterType.currentIndex()
        filterBW = self.cboxFilterBW.currentIndex()
        self.labelSigmaX.setVisible(False)
        self.lineEditSigmaX.setVisible(False)
        self.labelSigmaY.setVisible(False)
        self.lineEditSigmaY.setVisible(False)
        self.labelSigmaX2.setVisible(False)
        self.lineEditSigmaX2.setVisible(False)
        self.labelSigmaY2.setVisible(False)
        self.lineEditSigmaY2.setVisible(False)
        self.labelCutIn.setVisible(False)
        self.labelCutOff.setVisible(False)
        self.lineEditCutInFrequency.setVisible(False)
        self.lineEditCutOffFrequency.setVisible(False)
        self.labelLogDir.setVisible(False)
        self.cboxLoGDir.setVisible(False)
        self.lineEditThreshold.setVisible(False)
        self.labelTreshold.setVisible(False)
        self.btnLoadRefImage.setVisible(True)
        self.labelRefImagePath.setVisible(True)

        if filterType == 2 or filterType == 1:
            self.labelSigmaX.setVisible(True)
            self.lineEditSigmaX.setVisible(True)
            self.labelSigmaY.setVisible(True)
            self.lineEditSigmaY.setVisible(True)
            if filterType == 2: #log filter needs direction, but only needs one sigma
                self.cboxLoGDir.setVisible(True)
                self.labelLogDir.setVisible(True)
            if filterBW == 2:
                self.labelSigmaX2.setVisible(True)
                self.lineEditSigmaX2.setVisible(True)
                self.labelSigmaY2.setVisible(True)
                self.lineEditSigmaY2.setVisible(True)
            return 
        
        elif filterType == 0:
            if filterBW == 0 or filterBW == 1:
                self.labelCutIn.setVisible(True)
                self.labelCutOff.setVisible(False)
                self.lineEditCutInFrequency.setVisible(True)
                self.lineEditCutOffFrequency.setVisible(False)
            elif filterBW == 2:
                self.labelCutIn.setVisible(True)
                self.labelCutOff.setVisible(True)
                self.lineEditCutInFrequency.setVisible(True)
                self.lineEditCutOffFrequency.setVisible(True)

        if self.cboxDetectionMode.currentIndex() == 0: # single mode
            self.labelTreshold.setVisible(True)
            self.lineEditThreshold.setVisible(True)
            self.btnLoadRefImage.setVisible(False)
            self.labelRefImagePath.setVisible(False)

    '''
        @TODO: Refine functions
    '''
    def _createCanvasLayout(self):
        '''
            self.figures[i]
            i == 0: filtered_Ref
            i == 1: filtered_DUT
            i == 2: applied_threshold
        '''
        font = {'family' : 'normal',
                'size'   : 5}
        matplotlib.rc('font', **font)
        self.figures = []
        self.canvases = []
        self.axs = []
        self.btns = []
        hbox = QHBoxLayout()
        for i in range(3):
            fig = plt.figure(figsize=(10,10))
            canvas = FigureCanvas(fig)
            self.figures.append(fig)
            self.canvases.append(canvas)
            toolbar = NavigationToolbar(canvas, self)
            
            if i == 0:
                ax = fig.add_subplot(111)
            else:
                ax = fig.add_subplot(111, sharex=self.axs[0], sharey=self.axs[0])

            self.axs.append(ax)

            vbox = QVBoxLayout()
            vbox.addWidget(toolbar)
            vbox.addWidget(canvas)
            hbox.addLayout(vbox)

        return hbox

    def _updateImagePaths(self):
        if self._isDUTLoaded:
            self.labelDUTImagePath.setText(self.dutImagePath) 
        if self._isRefLoaded:
            self.labelRefImagePath.setText(self.refImagePath)
# --------------------------------------------------
# signal functions
# --------------------------------------------------
    def _loadDUTImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath:
            self.rawImage = cv2.imread(imagePath)
            if self.rawImage is not None:
                self._isDUTLoaded = True
                self.dutImagePath = imagePath
            else:
                self._isDUTLoaded = False
                QMessageBox.warning("Invalid image file")

        self._updateImagePaths()

    def _loadRefImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath:
            self.rawImage = cv2.imread(imagePath)
            if self.rawImage is not None:
                self._isRefLoaded = True
                self.refImagePath = imagePath
            else:
                self._isRefLoaded = False
                QMessageBox.warning("Invalid image file")
                
        self._updateImagePaths()
    
    '''
        TODO: Start calculate and add service layer
    '''
    def _calculate(self):
        pass

def run():
    app = QApplication(sys.argv)
    window = BlemishDetectionWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()