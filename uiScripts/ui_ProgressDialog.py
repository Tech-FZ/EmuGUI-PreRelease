# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProgressDialogiWAasF.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QProgressBar,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(385, 300)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 361, 271))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.progressBar = QProgressBar(self.gridLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout_2.addWidget(self.progressBar, 0, 1, 1, 1)

        self.endBtn = QPushButton(self.gridLayoutWidget)
        self.endBtn.setObjectName(u"endBtn")

        self.gridLayout_2.addWidget(self.endBtn, 2, 1, 1, 1)

        self.taskBox = QTextEdit(self.gridLayoutWidget)
        self.taskBox.setObjectName(u"taskBox")
        self.taskBox.setReadOnly(True)

        self.gridLayout_2.addWidget(self.taskBox, 1, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(accessibility)
        self.progressBar.setAccessibleName(QCoreApplication.translate("Dialog", u"Progress", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.endBtn.setAccessibleName(QCoreApplication.translate("Dialog", u"Cancel", None))
#endif // QT_CONFIG(accessibility)
        self.endBtn.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
#if QT_CONFIG(accessibility)
        self.taskBox.setAccessibleName(QCoreApplication.translate("Dialog", u"Task Log", None))
#endif // QT_CONFIG(accessibility)
    # retranslateUi

