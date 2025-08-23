# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pageEditorpLvlWb.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QSizePolicy,
    QSpacerItem, QTreeView, QVBoxLayout, QWidget)

class Ui_PageEditor(object):
    def setupUi(self, PageEditor):
        if not PageEditor.objectName():
            PageEditor.setObjectName(u"PageEditor")
        PageEditor.resize(850, 600)
        self.centralwidget = QWidget(PageEditor)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.central_widget_verticalLayout = QVBoxLayout()
        self.central_widget_verticalLayout.setObjectName(u"central_widget_verticalLayout")

        self.verticalLayout_2.addLayout(self.central_widget_verticalLayout)

        PageEditor.setCentralWidget(self.centralwidget)
        self.unit_view_dockWidget = QDockWidget(PageEditor)
        self.unit_view_dockWidget.setObjectName(u"unit_view_dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_5 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.dockWidgetContents)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft)

        self.active_unit_comboBox = QComboBox(self.dockWidgetContents)
        self.active_unit_comboBox.addItem("")
        self.active_unit_comboBox.addItem("")
        self.active_unit_comboBox.setObjectName(u"active_unit_comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.active_unit_comboBox.sizePolicy().hasHeightForWidth())
        self.active_unit_comboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.active_unit_comboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.treeView = QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_3.addWidget(self.treeView)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.unit_view_dockWidget.setWidget(self.dockWidgetContents)
        PageEditor.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.unit_view_dockWidget)
        self.item_settings_dockWidget = QDockWidget(PageEditor)
        self.item_settings_dockWidget.setObjectName(u"item_settings_dockWidget")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout_6 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.dockWidgetContents_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignLeft)

        self.pipeline_comboBox = QComboBox(self.dockWidgetContents_2)
        self.pipeline_comboBox.addItem("")
        self.pipeline_comboBox.addItem("")
        self.pipeline_comboBox.setObjectName(u"pipeline_comboBox")
        sizePolicy.setHeightForWidth(self.pipeline_comboBox.sizePolicy().hasHeightForWidth())
        self.pipeline_comboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.pipeline_comboBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)

        self.item_settings_dockWidget.setWidget(self.dockWidgetContents_2)
        PageEditor.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.item_settings_dockWidget)

        self.retranslateUi(PageEditor)

        QMetaObject.connectSlotsByName(PageEditor)
    # setupUi

    def retranslateUi(self, PageEditor):
        PageEditor.setWindowTitle(QCoreApplication.translate("PageEditor", u"PageEditor", None))
        self.unit_view_dockWidget.setWindowTitle(QCoreApplication.translate("PageEditor", u"Unit view", None))
        self.label.setText(QCoreApplication.translate("PageEditor", u"Active manga:", None))
        self.active_unit_comboBox.setItemText(0, QCoreApplication.translate("PageEditor", u"[Unit 1]", None))
        self.active_unit_comboBox.setItemText(1, QCoreApplication.translate("PageEditor", u"[Unit 2]", None))

        self.item_settings_dockWidget.setWindowTitle(QCoreApplication.translate("PageEditor", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate("PageEditor", u"Pipeline", None))
        self.pipeline_comboBox.setItemText(0, QCoreApplication.translate("PageEditor", u"[Pipeline 1]", None))
        self.pipeline_comboBox.setItemText(1, QCoreApplication.translate("PageEditor", u"[Pipeline 2]", None))

    # retranslateUi

