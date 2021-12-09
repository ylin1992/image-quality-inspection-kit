import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QComboBox, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib

from backend.service import FilterService

QLINEEDIT_GREY_SHEET = """QLineEdit { background-color: green; color: #808080 }"""
QLINEEDIT_WHITE_SHEET = """QLineEdit { background-color: green; color: white }"""

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class State:
    def __init__(self):
        self._image_loaded = False
        self._filter_generated = False
        self._filter_applied = False
        self._threshold_applied = False
    
    def setImageLoaded(self, isLoaded: bool):
        self._image_loaded = isLoaded

    def setFilterGenerated(self, isGenerated: bool):
        self._filter_generated = isGenerated

    def setFilterApplied(self, isApplied: bool):
        self._filter_applied = isApplied
    
    def thresholdApplied(self, isApplied: bool):
        self._threshold_applied = isApplied

    def resetAll(self):
        self._image_loaded = False
        self._filter_generated = False
        self._filter_applied = False
        self._threshold_applied = False
    
    def isImageLoaded(self):
        return self._image_loaded
    
    def isFilterGenerated(self):
        return self._filter_generated
    
    def isFilterApplied(self):
        return self._filter_applied

    def isThresholdApplied(self):
        return self._threshold_applied

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IQI Filter Tuner")
        self._centralWidget = QWidget()
        self.setCentralWidget(self._centralWidget)

        self._initPara()
        self._createWidgets()
        self._createMenu()
        self._updateEditTextVisibility(self.cboxFilterType.currentIndex())
        # self._updateTextViewVisibiltyForBW(self.cboxFilterBW.currentIndex())

    def _initPara(self):
        self.filter = None
        self.rawImage = None
        self.appliedFilter = None
        self.appliedThreshold = None
        self.BWs = ['lp', 'hp', 'bp']
        self.state = State()

    def _createWidgets(self):
        vboxLayout = QVBoxLayout()
        hboxLayout = QHBoxLayout()

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

        self.btnCheckFilter = QPushButton("Check Filter")
        self.btnApplyFilter = QPushButton("Apply Filter")
        self.btnApplyThreshold = QPushButton("Apply Threshold")

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
        hboxLayout.addWidget(QLabel("Threshold"))
        hboxLayout.addWidget(self.lineEditThreshold)
        
        hboxLayoutFigure = self._createCanvasLayout()
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(hboxLayoutFigure)
        # vboxLayout.addWidget(self.toolbar)
        # vboxLayout.addWidget(self.canvas)
        

        self._centralWidget.setLayout(vboxLayout)

    def _createMenu(self):
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        self.menu = bar.addMenu("File")
        openAction = QAction('Open Image', self)  
        openAction.triggered.connect(self._openImage) 
        self.menu.addAction(openAction)


    def _createCanvasLayout(self):
        '''
            self.figures[i]
            i == 0: rawImage
            i == 1: filter
            i == 2: applied filter
            i == 3: threshold
        '''
        font = {'family' : 'normal',
                'size'   : 5}
        matplotlib.rc('font', **font)
        self.figures = []
        self.canvases = []
        self.axs = []
        self.btns = []
        hbox = QHBoxLayout()
        vboxStack = QVBoxLayout()
        for i in range(4):
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
            
            if i == 0:
                self.btns.append(QPushButton("Reset Image"))
                self.btns[i].clicked.connect(self._resetImage)
            elif i == 1:
                self.btns.append(QPushButton("Check filter"))
                self.btns[i].clicked.connect(self._checkFilter)
            elif i == 2:
                self.btns.append(QPushButton("Apply filter"))
                self.btns[i].clicked.connect(self._applyFilter)
            else:
                self.btns.append(QPushButton("Apply Threshold"))
                self.btns[i].clicked.connect(self._applyFilter)


            vbox = QVBoxLayout()
            vbox.addWidget(toolbar)
            vbox.addWidget(canvas)
            vbox.addWidget(self.btns[i])
            hbox.addLayout(vbox)
            if i == 1 or i == 3:
                vboxStack.addLayout(hbox)
                hbox = QHBoxLayout()

        return vboxStack

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

 # --------------------------------------------------------------------------
 #  Signal functions
 # --------------------------------------------------------------------------
    def _resetImage(self):
        self.state.resetAll()
        self.rawImage = None
        self.filter = None
        self.appliedFilter = None
        self.appliedThreshold = None
        for ax in self.axs:
            ax.clear()
        for c in self.canvases:
            c.draw()
    
    def _openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        self.rawImage = cv2.imread(imagePath)
        self.state.setImageLoaded(True)
        print(self.rawImage.shape)
        self.axs[0].imshow(self.rawImage)
        for c in self.canvases:
            c.draw()
        

    def _checkFilter(self):
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
        shape = (100, 100)
        if self.state.isImageLoaded():
            shape = self.rawImage.shape[:2]


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
            except Exception as e:
                print(e)

                filt = FilterService.get_gaussian_filter(shape=shape, 
                                                        sigma_x=sigmax, 
                                                        sigma_y=sigmay, 
                                                        type=self._getBWFromIndex(filterBW),
                                                        sigma_x2=sigmax2,
                                                        sigma_y2=sigmay2)

        self.axs[1].imshow(filt.get_filt())
        self.canvases[1].draw()
        
    def _applyFilter(self):
        print("Apply filter")
    
    def _applyThreshold(self):
        print("Apply Threshold")

    def _getBWFromIndex(self, option):
        return self.BWs[option]

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()