# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'retrieveportaldatawidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QToolButton, QTreeView, QVBoxLayout,
    QWidget)

class Ui_RetrievePortalDataWidget(object):
    def setupUi(self, RetrievePortalDataWidget):
        if not RetrievePortalDataWidget.objectName():
            RetrievePortalDataWidget.setObjectName(u"RetrievePortalDataWidget")
        RetrievePortalDataWidget.resize(714, 584)
        self.verticalLayout_3 = QVBoxLayout(RetrievePortalDataWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.manifestGroupBox = QGroupBox(RetrievePortalDataWidget)
        self.manifestGroupBox.setObjectName(u"manifestGroupBox")
        self.gridLayout_2 = QGridLayout(self.manifestGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelSearchTerm = QLabel(self.manifestGroupBox)
        self.labelSearchTerm.setObjectName(u"labelSearchTerm")
        self.labelSearchTerm.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelSearchTerm, 0, 0, 1, 1)

        self.lineEditSearch = QLineEdit(self.manifestGroupBox)
        self.lineEditSearch.setObjectName(u"lineEditSearch")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSearch.sizePolicy().hasHeightForWidth())
        self.lineEditSearch.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lineEditSearch, 0, 1, 1, 1)

        self.labelSearchType = QLabel(self.manifestGroupBox)
        self.labelSearchType.setObjectName(u"labelSearchType")
        self.labelSearchType.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelSearchType, 1, 0, 1, 1)

        self.labelDatasetID = QLabel(self.manifestGroupBox)
        self.labelDatasetID.setObjectName(u"labelDatasetID")
        self.labelDatasetID.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelDatasetID, 2, 0, 1, 1)

        self.lineEditDatasetID = QLineEdit(self.manifestGroupBox)
        self.lineEditDatasetID.setObjectName(u"lineEditDatasetID")

        self.gridLayout_2.addWidget(self.lineEditDatasetID, 2, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonSearch = QPushButton(self.manifestGroupBox)
        self.pushButtonSearch.setObjectName(u"pushButtonSearch")

        self.horizontalLayout_2.addWidget(self.pushButtonSearch)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.comboBoxSearchType = QComboBox(self.manifestGroupBox)
        self.comboBoxSearchType.addItem("")
        self.comboBoxSearchType.addItem("")
        self.comboBoxSearchType.setObjectName(u"comboBoxSearchType")

        self.horizontalLayout_3.addWidget(self.comboBoxSearchType)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.groupBoxFilter = QGroupBox(self.manifestGroupBox)
        self.groupBoxFilter.setObjectName(u"groupBoxFilter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBoxFilter.sizePolicy().hasHeightForWidth())
        self.groupBoxFilter.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.groupBoxFilter)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolButtonFilterSpecies = QToolButton(self.groupBoxFilter)
        self.toolButtonFilterSpecies.setObjectName(u"toolButtonFilterSpecies")
        self.toolButtonFilterSpecies.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.gridLayout.addWidget(self.toolButtonFilterSpecies, 0, 0, 1, 1)

        self.toolButtonFilterOrgan = QToolButton(self.groupBoxFilter)
        self.toolButtonFilterOrgan.setObjectName(u"toolButtonFilterOrgan")
        self.toolButtonFilterOrgan.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.gridLayout.addWidget(self.toolButtonFilterOrgan, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBoxFilter, 0, 2, 4, 1)


        self.verticalLayout_3.addWidget(self.manifestGroupBox)

        self.groupBox = QGroupBox(RetrievePortalDataWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableViewSearchResult = QTableView(self.groupBox)
        self.tableViewSearchResult.setObjectName(u"tableViewSearchResult")
        self.tableViewSearchResult.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableViewSearchResult.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableViewSearchResult.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_2.addWidget(self.tableViewSearchResult)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.pushButtonDownload = QPushButton(RetrievePortalDataWidget)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout.addWidget(self.pushButtonDownload)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.groupBoxDownloadedFileTree = QGroupBox(RetrievePortalDataWidget)
        self.groupBoxDownloadedFileTree.setObjectName(u"groupBoxDownloadedFileTree")
        self.verticalLayout = QVBoxLayout(self.groupBoxDownloadedFileTree)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeViewFileBrowser = QTreeView(self.groupBoxDownloadedFileTree)
        self.treeViewFileBrowser.setObjectName(u"treeViewFileBrowser")

        self.verticalLayout.addWidget(self.treeViewFileBrowser)


        self.verticalLayout_3.addWidget(self.groupBoxDownloadedFileTree)

        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setObjectName(u"horizontalLayout1")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout1.addItem(self.horizontalSpacer_8)

        self.pushButtonDone = QPushButton(RetrievePortalDataWidget)
        self.pushButtonDone.setObjectName(u"pushButtonDone")

        self.horizontalLayout1.addWidget(self.pushButtonDone)


        self.verticalLayout_3.addLayout(self.horizontalLayout1)


        self.retranslateUi(RetrievePortalDataWidget)

        QMetaObject.connectSlotsByName(RetrievePortalDataWidget)
    # setupUi

    def retranslateUi(self, RetrievePortalDataWidget):
        RetrievePortalDataWidget.setWindowTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Search tool", None))
        self.labelSearchTerm.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Search term:", None))
        self.labelSearchType.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Search type:", None))
#if QT_CONFIG(tooltip)
        self.labelDatasetID.setToolTip(QCoreApplication.translate("RetrievePortalDataWidget", u"Restrict the search to the dataset with ID specified here", None))
#endif // QT_CONFIG(tooltip)
        self.labelDatasetID.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Dataset ID:", None))
#if QT_CONFIG(tooltip)
        self.lineEditDatasetID.setToolTip(QCoreApplication.translate("RetrievePortalDataWidget", u"Restrict the search to the dataset with ID specified here", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonSearch.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Search", None))
        self.comboBoxSearchType.setItemText(0, QCoreApplication.translate("RetrievePortalDataWidget", u"by filename", None))
        self.comboBoxSearchType.setItemText(1, QCoreApplication.translate("RetrievePortalDataWidget", u"by mimetype", None))

        self.groupBoxFilter.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Filter:", None))
        self.toolButtonFilterSpecies.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Species  ", None))
        self.toolButtonFilterOrgan.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Organ  ", None))
        self.groupBox.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Search results:", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Download", None))
        self.groupBoxDownloadedFileTree.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Downloaded files:", None))
        self.pushButtonDone.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Done", None))
    # retranslateUi

