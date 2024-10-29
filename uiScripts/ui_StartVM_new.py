# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartVM_newNsTkJh.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 381, 281))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 0, 10, 0)
        self.lbl_tpm = QLabel(self.gridLayoutWidget)
        self.lbl_tpm.setObjectName(u"lbl_tpm")

        self.gridLayout.addWidget(self.lbl_tpm, 0, 0, 1, 1)

        self.le_tpm = QLineEdit(self.gridLayoutWidget)
        self.le_tpm.setObjectName(u"le_tpm")

        self.gridLayout.addWidget(self.le_tpm, 0, 1, 1, 2)

        self.btn_startVM = QPushButton(self.gridLayoutWidget)
        self.btn_startVM.setObjectName(u"btn_startVM")

        self.gridLayout.addWidget(self.btn_startVM, 3, 0, 1, 3)

        self.btn_oneTimeEdit = QPushButton(self.gridLayoutWidget)
        self.btn_oneTimeEdit.setObjectName(u"btn_oneTimeEdit")

        self.gridLayout.addWidget(self.btn_oneTimeEdit, 2, 0, 1, 3)

        self.lbl_vmNotice = QLabel(self.gridLayoutWidget)
        self.lbl_vmNotice.setObjectName(u"lbl_vmNotice")
        self.lbl_vmNotice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_vmNotice.setWordWrap(True)

        self.gridLayout.addWidget(self.lbl_vmNotice, 1, 0, 1, 3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lbl_tpm.setText(QCoreApplication.translate("Dialog", u"TPM (Linux only)", None))
        self.btn_startVM.setText(QCoreApplication.translate("Dialog", u"Start VM", None))
        self.btn_oneTimeEdit.setText(QCoreApplication.translate("Dialog", u"Edit VM for this session", None))
        self.lbl_vmNotice.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>If your VM does not start within five minutes, make sure you can read the stuff on the console.</p></body></html>", None))
    # retranslateUi

