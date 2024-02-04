import requests
import sys
import os
import io
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtCore


template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>580</width>
    <height>460</height>
   </rect>
  </property>
  <property name="mouseTracking">
   <bool>true</bool>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="image_label">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>540</width>
      <height>330</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QPushButton" name="find_button">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>350</y>
      <width>121</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Найти</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="enter_edit">
    <property name="geometry">
     <rect>
      <x>150</x>
      <y>350</y>
      <width>171</width>
      <height>41</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>580</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>'''


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.initUI()
        self.load_map(self.mp)

    def initUI(self):
        self.mp = {'lt': 59.939820, 'ln': 30.314383, 'z': 17, 'l': 'map'}

        self.enter_edit.setEnabled(False)
        self.find_button.setEnabled(False)

    def load_map(self, mp):
        map_request_params = {
            'll': str(mp['ln']) + ',' + str(mp['lt']),
            'z': str(mp['z']),
            'l': mp['l']
        }
        static_api = 'http://static-maps.yandex.ru/1.x/'
        response = requests.get(static_api, map_request_params)
        if not response:
            print("Ошибка выполнения запроса")
            print("HTTP статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        else:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.image_label.setPixmap(pixmap)


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_PageUp:
            self.mp['z'] += (1 if self.mp['z'] < 19 else 0)
        if event.key() == QtCore.Qt.Key.Key_PageDown:
            self.mp['z'] -= (1 if self.mp['z'] > 1 else 0)
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.mp['lt'] += (0.001 if self.mp['lt'] < 90 else 0)
        if event.key() == QtCore.Qt.Key.Key_Down:
            self.mp['lt'] -= (0.001 if self.mp['lt'] > -90 else 0)
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.mp['ln'] -= (0.001 if self.mp['ln'] > -180 else 0)
        if event.key() == QtCore.Qt.Key.Key_Right:
            self.mp['ln'] += (0.001 if self.mp['ln'] < 180 else 0)
        if event.key() == QtCore.Qt.Key.Key_Space:
            self.mp['l'] = ('skl' if self.mp['l'] == 'map' else 'map')

        self.load_map(self.mp)
        event.accept()

    def mousePressEvent(self, event):
        if self.enter_edit.x() <= event.pos().x() <= self.enter_edit.x() + self.enter_edit.width() and \
                self.enter_edit.y() <= event.pos().y() <= self.enter_edit.y() + self.enter_edit.height():
            self.enter_edit.setEnabled(True)
            self.find_button.setEnabled(True)
        else:
            self.enter_edit.setEnabled(False)
            self.find_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MapWindow()
    ex.show()
    sys.exit(app.exec_())



