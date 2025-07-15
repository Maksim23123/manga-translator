# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newUnitDialogohoYUo.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_newUnitDialog(object):
    def setupUi(self, newUnitDialog):
        if not newUnitDialog.objectName():
            newUnitDialog.setObjectName(u"newUnitDialog")
        newUnitDialog.resize(242, 73)
        self.verticalLayout_2 = QVBoxLayout(newUnitDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.unitNameLabel = QLabel(newUnitDialog)
        self.unitNameLabel.setObjectName(u"unitNameLabel")

        self.horizontalLayout.addWidget(self.unitNameLabel)

        self.unitNameLineEdit = QLineEdit(newUnitDialog)
        self.unitNameLineEdit.setObjectName(u"unitNameLineEdit")

        self.horizontalLayout.addWidget(self.unitNameLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(newUnitDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(newUnitDialog)
        self.buttonBox.accepted.connect(newUnitDialog.accept)
        self.buttonBox.rejected.connect(newUnitDialog.reject)

        QMetaObject.connectSlotsByName(newUnitDialog)
    # setupUi

    def retranslateUi(self, newUnitDialog):
        newUnitDialog.setWindowTitle(QCoreApplication.translate("newUnitDialog", u"Dialog", None))
        self.unitNameLabel.setText(QCoreApplication.translate("newUnitDialog", u"Manga name", None))
    # retranslateUi

