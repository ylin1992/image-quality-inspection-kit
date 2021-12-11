import sys
import cv2
from matplotlib import widgets
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

from backend.service.DetectionService import BlemishDetectionService
from backend.service import FilterService

class BlemishDetectionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Blemish Detection Tuner")
        self._createWidgets()
        self._initPara()
        self._updateEditTextVisibility(self.cboxDetectionMode.currentIndex())

        
    def _initPara(self):
        self.BWs = ['lp', 'hp', 'bp']
        self._isDUTLoaded = False
        self._isRefLoaded = False
        self._isAppliedThreshold = False
        self._isFilterLoaded = False
        self.filter = None
        self.dutImagePath = None
        self.refImagePath = None
        self.rawImage = None
        self.refImage = None
        self.res = None
        self.map = None
        self.filteredTarget = None
        self.filteredRef = None
        self.roi_w = 100
        self.ratio = 0.99
        self.blemishDetectionService = BlemishDetectionService()

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
        self.btnUpdateFilter = QPushButton("Update filter")
        self.btnUpdateFilter.clicked.connect(self._updateFilter)

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
        dualModeParaGridLayout.addWidget(self.labelTreshold, 0, 5, 1, 1)
        dualModeParaGridLayout.addWidget(self.lineEditThreshold, 0, 6, 1, 1)
        # dualModeParaGridLayout.addWidget(QLabel(""), 0, 7, 1, 4)


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
        hboxLayout.addWidget(self.btnUpdateFilter)

        vboxLayout.addLayout(detectionModeHboxLayout)
        vboxLayout.addLayout(loadImageHboxLayout)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(dualModeParaGridLayout)
        figuresLayout = self._createCanvasLayout()
        vboxLayout.addLayout(figuresLayout)
        
        self.btnCalculate = QPushButton("DETECT")
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
        self.btnLoadRefImage.setVisible(True)
        self.labelRefImagePath.setVisible(True)
        
        # canvases
        # self.canvasWidgets[1].setVisible(False)
        # self.canvasWidgets[2].setVisible(False)

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
            # self.labelTreshold.setVisible(True)
            # self.lineEditThreshold.setVisible(True)
            self.btnLoadRefImage.setVisible(False)
            self.labelRefImagePath.setVisible(False)
        # elif self.cboxDetectionMode.currentIndex() == 1:
        #     self.canvasWidgets[1].setVisible(True)
        #     self.canvasWidgets[2].setVisible(True)

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
        self.canvasWidgets = []
        vbox = QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)

        return vbox

    def _updateImagePaths(self):
        if self._isDUTLoaded:
            self.labelDUTImagePath.setText(self.dutImagePath) 
        if self._isRefLoaded:
            self.labelRefImagePath.setText(self.refImagePath)

    def _getBWFromIndex(self, option):
        return self.BWs[option] 
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
            self.refImage = cv2.imread(imagePath)
            if self.refImage is not None:
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
        if not self._isDUTLoaded:
            QMessageBox.warning(self, "warning", "DUT image is not loaded")
            return 

        if not self._isFilterLoaded:
            QMessageBox.warning(self, "warning", "Filter is not loaded")
            return
        
        self.blemishDetectionService.set_image(self.rawImage)
        self.blemishDetectionService.set_filter(self.filter)

        detectionMode = self.cboxDetectionMode.currentIndex()
        try:
            thr = float(self.lineEditThreshold.text())
        except:
            QMessageBox.warning(self, "warning", "Invalid Threshold Value")
            return 
        if detectionMode == 0: # single mode
            self.blemishDetectionService.initBlemishDetectionObject()
            self.res, _ = self.blemishDetectionService.start_calculate(thr)
            self.filteredTarget = self.blemishDetectionService.get_filtered_target_image()

        elif detectionMode == 1:
            if not self._isRefLoaded:
                QMessageBox.warning(self, "warning", "Ref image is not loaded")
                return
            
            try:
                self.roi_w = int(self.lineEditRoiW.text())
                self.ratio = float(self.lineEditRatio.text())
            except:
                QMessageBox.warning(self, "warning", "Invalid ROI width or ratio")
            
            self.blemishDetectionService.set_ref_image(self.refImage)
            self.blemishDetectionService.set_ratio(self.ratio)
            self.blemishDetectionService.set_roi_w(self.roi_w)
            self.blemishDetectionService.initBlemishDetectionObject()
            self.res, self.map = self.blemishDetectionService.start_calculate(thr)
            self.filteredTarget = self.blemishDetectionService.get_filtered_target_image()
            self.filteredRef = self.blemishDetectionService.get_filtered_ref_image()

        self._updateCanvasImage()


    def _updateCanvasImage(self):
        self.figure.clear()
        if self._isRefLoaded: # dual mode
            ax1 = self.figure.add_subplot(141)
            if self.filteredTarget is not None:
                ax1.imshow(self.filteredTarget)
            ax2 = self.figure.add_subplot(142, sharex=ax1, sharey=ax1)
            ax2.axes.xaxis.set_visible(False)
            ax2.axes.yaxis.set_visible(False)
            if self.filteredRef is not None:
                ax2.imshow(self.filteredRef)
            ax3 = self.figure.add_subplot(143, sharex=ax1, sharey=ax1)
            ax3.axes.xaxis.set_visible(False)
            ax3.axes.yaxis.set_visible(False)
            if self.map is not None:
                ax3.imshow(self.map)
            ax4 = self.figure.add_subplot(144, sharex=ax1, sharey=ax1)
            ax4.axes.xaxis.set_visible(False)
            ax4.axes.yaxis.set_visible(False)
            if self.res is not None:
                ax4.imshow(self.res)
        else:
            ax1 = self.figure.add_subplot(121)
            if self.filteredTarget is not None:
                ax1.imshow(self.filteredTarget)
            ax4 = self.figure.add_subplot(122, sharex=ax1, sharey=ax1)
            ax4.axes.xaxis.set_visible(False)
            ax4.axes.yaxis.set_visible(False)
            if self.res is not None:
                ax4.imshow(self.res)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def _updateFilter(self):
        filterType = self.cboxFilterType.currentIndex()
        filterBW = self.cboxFilterBW.currentIndex()

        print(filterType, filterBW)

        filt = None
        cutin = 0
        cutoff = 0
        sigmax = 0
        sigmay = 0
        sigmax2 = 0
        sigmay2 = 0
        shape = None
        if self._isDUTLoaded:
            shape = self.rawImage.shape[:2]
        else:
            QMessageBox.warning(self, "warning", "Load DUT first")
            return 

        if filterType == 0:
            try:
                cutin = float(self.lineEditCutInFrequency.text())
                if filterBW == 2:
                    cutoff = float(self.lineEditCutOffFrequency.text())
            except Exception as e:
                print(e)
            
            filt = FilterService.get_butterworth_filter(shape=shape, 
                                                        cutin=cutin, 
                                                        cutoff=cutoff, 
                                                        type=self._getBWFromIndex(filterBW))

        if filterType == 1: # Gaussian
            try:
                sigmax = float(self.lineEditSigmaX.text())
                sigmay = float(self.lineEditSigmaY.text())
                if filterBW == 2:
                    sigmax2 = float(self.lineEditSigmaX2.text())
                    sigmay2 = float(self.lineEditSigmaY2.text())

                filt = FilterService.get_gaussian_filter(shape=shape, 
                                                        sigma_x=sigmax, 
                                                        sigma_y=sigmay, 
                                                        type=self._getBWFromIndex(filterBW),
                                                        sigma_x2=sigmax2,
                                                        sigma_y2=sigmay2)
            except Exception as e:
                print(e.__traceback__())

        if filt is not None:
            self.filter = filt
            self._isFilterLoaded = True


def run():
    app = QApplication(sys.argv)
    window = BlemishDetectionWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()