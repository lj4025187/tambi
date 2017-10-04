
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtCore import QRectF

import urllib.request
import queue

from QCustomizedWidgets.QCustomizedGraphicsView import QCustomizedGraphicsView

from modules.gps.convert_coordinates import ConvertCoordinates

from configs.configFiles import ConfigFile

# to make program closeable with ctr-c in terminal
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class QMapWidget(QCustomizedGraphicsView):
    
    TILE_SIZE = 256
    
    zoom = 10
    
    convert = ConvertCoordinates()
    
    tiles_matrix = {'x_min': None, 'x_max': None, 'y_min': None, 'y_max': None}
    
    def __init__(self):
        super().__init__()
        
        self.setRenderHint(QPainter.Antialiasing)
        
        self.addControlElements()
        self.startDownloadThread()
    
    def addControlElements(self):
        grid = QGridLayout()
        grid.setRowStretch(0, 10000)
        grid.setColumnStretch(0, 10000)
        self.setLayout(grid)
        
        zoom_in_button = QPushButton()
        zoom_in_button.setIcon(QIcon.fromTheme('zoom-in'))
        zoom_in_button.setMaximumSize(25, 25)
        grid.addWidget(zoom_in_button, 1, 1)
        zoom_in_button.clicked.connect(self.zoomInClicked)
        
        zoom_out_button = QPushButton()
        zoom_out_button.setIcon(QIcon.fromTheme('zoom-out'))
        zoom_out_button.setMaximumSize(25, 25)
        grid.addWidget(zoom_out_button, 2, 1)
        zoom_out_button.clicked.connect(self.zoomOutClicked)
    
    def startDownloadThread(self):
        self.download_queue = queue.Queue()
        
        self.download_thread = QDownloadMapTilesThread(self.download_queue, self.scene())#self.scene(), self.zoom, tile_min_x, tile_max_x, tile_min_y, tile_max_y, 'init')
        self.download_thread.drawMapTile.connect(self.__drawMapTile)
        self.download_thread.start()
    
    def zoomInClicked(self):
        if self.download_thread:
            self.download_thread.stop()
        
        if self.zoom < 19:
            self.zoom += 1
        self.scene().clear()
        """ because this seems to be the best way to shrink the scene again: """
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        
        self.calculateNeededTiles(self.boundings_path)
        self.drawPointList()
    
    def zoomOutClicked(self):
        if self.download_thread:
            self.download_thread.stop()
        
        if self.zoom > 0:
            self.zoom -= 1
        self.scene().clear()
        self.items().clear()
        
        """ because this seems to be the best way to shrink the scene again: """
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        
        self.calculateNeededTiles(self.boundings_path)
        self.drawPointList()
    
    def calculateNeededTiles(self, lat_min, lat_max, lon_min, lon_max):
        tile_min_x, tile_max_y = self.convert.degToTileNumber(self.zoom, lat_min, lon_min)
        
        tile_max_x, tile_min_y = self.convert.degToTileNumber(self.zoom, lat_max, lon_max)
        
        tile_max_x += 1
        tile_max_y += 1
        
        self.tiles_matrix['x_min'] = tile_min_x
        self.tiles_matrix['x_max'] = tile_max_x
        self.tiles_matrix['y_min'] = tile_min_y
        self.tiles_matrix['y_max'] = tile_max_y
        
        self.scene_rect = QRectF(0, 0, (tile_max_x - tile_min_x)*self.TILE_SIZE, (tile_max_y - tile_min_y)*self.TILE_SIZE)
        
        """
        self.download_thread = QDownloadMapTilesThread(self.scene(), self.zoom, tile_min_x, tile_max_x, tile_min_y, tile_max_y, 'init')
        self.download_thread.drawMapTile.connect(self.__drawMapTile)
        self.download_thread.start()
        """
        
        self.download_queue.put({
            'zoom': self.zoom,
            'x_min': tile_min_x,
            'x_max': tile_max_x,
            'y_min': tile_min_y,
            'y_max': tile_max_y,
            'mode': 'init',
            })
        
        #self.corners_mercator = self.convert.calculateCorners(self.zoom, tile_min_x, tile_max_x, tile_min_y, tile_max_y)
    
    def fetchMoreTiles(self, mode):
        if mode == 'left':
            x_min = self.tiles_matrix['x_min']
            y_min = self.tiles_matrix['y_min']
            y_max = self.tiles_matrix['y_max']
            
            #self.download_thread_left = QDownloadMapTilesThread(self.scene(), self.zoom, x_min-2, x_min, y_min, y_max, 'left')
            #self.download_thread_left.drawMapTile.connect(self.__drawMapTile)
            #self.download_thread_left.start()
        
        elif mode == 'right':
            pass
        
        elif mode == 'top':
            pass
        
        elif mode == 'bottom':
            pass
        
    
    def showPosition(self):
        #self.calculateNeededTiles(51.476852, 51.476852, 0, 0})
        self.calculateNeededTiles(51, 52, -1, 1)
    
    def __drawMapTile(self, pixmap, pos_x, pos_y):
        item = self.scene().addPixmap(pixmap)
        item.setPos(pos_y*self.TILE_SIZE, pos_x*self.TILE_SIZE)
        item.setZValue(-10)
    
    def scrollContentsBy(self, dx, dy):
        
        hor_cur = self.horizontalScrollBar().value()
        vert_cur = self.verticalScrollBar().value()
        
        hor_min = self.horizontalScrollBar().minimum()
        vert_min = self.verticalScrollBar().minimum()
        
        hor_max = self.horizontalScrollBar().maximum()
        vert_max = self.verticalScrollBar().maximum()
        
        if hor_cur <= hor_min + self.TILE_SIZE:
            self.fetchMoreTiles('left')
        
        elif hor_cur >= hor_max - self.TILE_SIZE:
            self.fetchMoreTiles('right')
        
        if vert_cur <= vert_min + self.TILE_SIZE:
            self.fetchMoreTiles('top')
        
        elif vert_cur >= vert_max - self.TILE_SIZE:
            self.fetchMoreTiles('bottom')
        
        super().scrollContentsBy(dx, dy)

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import os, time
class QDownloadMapTilesThread(QThread):
    
    __stop = False
    drawMapTile = pyqtSignal(object, float, float)
    
    """
    def __init__(self, scene, zoom, x_min, x_max, y_min, y_max, mode):
        super().__init__()
        
        #self.scene = scene
        self.scene_rect = scene.itemsBoundingRect()
        
        self.zoom = zoom
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.mode = mode
        
        config = ConfigFile()
        self.cache_path = config.readPath('cache', 'cachepath')
        self.cache_path = os.path.join(self.cache_path, 'maps')
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
    """
    
    def __init__(self, queue, scene):
        super().__init__()
        
        self.queue = queue
        self.scene = scene
        
        config = ConfigFile()
        self.cache_path = config.readPath('cache', 'cachepath')
        self.cache_path = os.path.join(self.cache_path, 'maps')
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
    
    def run(self):
        while not self.__stop:
            if not self.queue.empty():
                item = self.queue.get()
                if item['mode'] == 'init':
                    self.initialRun(item)
                
                elif item['mode'] == 'left':
                    pass
                
                elif item['mode'] == 'right':
                    pass
                
                elif item['mode'] == 'top':
                    pass
                
                elif item['mode'] == 'bottom':
                    pass
            
            time.sleep(0.0001)
    
    def initialRun(self, item):
        for i, x in enumerate(range(item['x_min'], item['x_max'])):
            if self.__stop:
                break
            QApplication.processEvents()
            for j, y in enumerate(range(item['y_min'], item['y_max'])):
                if self.__stop:
                    break
                QApplication.processEvents()
                self.fetchTile(item['zoom'], x, y, j, i)
    
    def fetchTile(self, zoom, x, y, pos_x, pos_y):
        pixmap = QPixmap()
        
        image_filename = os.path.join(self.cache_path, str(zoom)+'_'+str(x)+'_'+str(y)+'.png')
        
        if not os.path.exists(image_filename):
            tile = urllib.request.urlopen("http://a.tile.openstreetmap.org/{0}/{1}/{2}.png".format(self.zoom, x, y))
            
            image = tile.read()
            pixmap.loadFromData(image)
            
            with open(image_filename, 'bw') as binary:
                binary.write(image)
        
        else:
            pixmap.load(image_filename)
        
        self.drawMapTile.emit(pixmap, pos_x, pos_y)
    
    def stop(self):
        self.__stop = True

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    c = QMapWidget()
    win.setCentralWidget(c)
    win.resize(500, 500)
    win.show()
    sys.exit(app.exec_())
