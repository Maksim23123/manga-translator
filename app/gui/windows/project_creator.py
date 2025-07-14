# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_creatorgMXvcu.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)


class ProjectCreator(QDialog):
    def __init__(self, parent=None, flags=Qt.WindowFlags(), *, sizeGripEnabled=False, modal=False, default_directory=""):
        super().__init__(parent, flags)
        self.setSizeGripEnabled(sizeGripEnabled)
        self.setModal(modal)

        self._setup_ui()
        self._apply_settings()

        self.set_directory(default_directory)
    

    @property
    def project_name(self):
        if self.project_name_edit_line:
            return self.project_name_edit_line.text()
        else:
            return None
    

    @property
    def project_path(self):
        if self.choose_location_edit_line:
            return self.choose_location_edit_line.text()
        else:
            return None
    
    
    def _setup_ui(self):
        self._ui = Ui_ProjectCreatorDialog()
        self._ui.setupUi(self)

        self.project_name_edit_line = self._ui.project_name_line_edit
        self.choose_location_edit_line = self._ui.choose_location_edit_line
        self.choose_location_button = self._ui.choose_location_button
        self.dialog_button_box = self._ui.buttonBox 


    def _apply_settings(self):
        self.setFixedSize(366, 162)
        self.setWindowTitle("New project")

    
    def set_directory(self, directory: str):
        self.choose_location_edit_line.setText(directory)
        

# Generated part.
# Don't tuch


class Ui_ProjectCreatorDialog(object):
    def setupUi(self, ProjectCreatorDialog):
        if not ProjectCreatorDialog.objectName():
            ProjectCreatorDialog.setObjectName(u"ProjectCreatorDialog")
        ProjectCreatorDialog.resize(366, 162)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProjectCreatorDialog.sizePolicy().hasHeightForWidth())
        ProjectCreatorDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(ProjectCreatorDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.project_name_label = QLabel(ProjectCreatorDialog)
        self.project_name_label.setObjectName(u"project_name_label")

        self.horizontalLayout.addWidget(self.project_name_label)

        self.project_name_line_edit = QLineEdit(ProjectCreatorDialog)
        self.project_name_line_edit.setObjectName(u"project_name_line_edit")

        self.horizontalLayout.addWidget(self.project_name_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.choose_location_label = QLabel(ProjectCreatorDialog)
        self.choose_location_label.setObjectName(u"choose_location_label")

        self.horizontalLayout_5.addWidget(self.choose_location_label)

        self.choose_location_edit_line = QLineEdit(ProjectCreatorDialog)
        self.choose_location_edit_line.setObjectName(u"choose_location_edit_line")

        self.horizontalLayout_5.addWidget(self.choose_location_edit_line)

        self.choose_location_button = QPushButton(ProjectCreatorDialog)
        self.choose_location_button.setObjectName(u"choose_location_button")

        self.horizontalLayout_5.addWidget(self.choose_location_button)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.buttonBox = QDialogButtonBox(ProjectCreatorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox, 0, Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(ProjectCreatorDialog)

        QMetaObject.connectSlotsByName(ProjectCreatorDialog)
    # setupUi

    def retranslateUi(self, ProjectCreatorDialog):
        ProjectCreatorDialog.setWindowTitle(QCoreApplication.translate("ProjectCreatorDialog", u"Dialog", None))
        self.project_name_label.setText(QCoreApplication.translate("ProjectCreatorDialog", u"Project name", None))
        self.choose_location_label.setText(QCoreApplication.translate("ProjectCreatorDialog", u"Project location", None))
        self.choose_location_button.setText(QCoreApplication.translate("ProjectCreatorDialog", u"choose", None))
    # retranslateUi

