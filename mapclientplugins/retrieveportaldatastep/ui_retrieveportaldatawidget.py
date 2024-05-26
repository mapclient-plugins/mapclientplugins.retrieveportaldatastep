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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

class Ui_RetrievePortalDataWidget(object):
    def setupUi(self, RetrievePortalDataWidget):
        if not RetrievePortalDataWidget.objectName():
            RetrievePortalDataWidget.setObjectName(u"RetrievePortalDataWidget")
        RetrievePortalDataWidget.resize(714, 584)
        self.verticalLayout_9 = QVBoxLayout(RetrievePortalDataWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.manifestGroupBox = QGroupBox(RetrievePortalDataWidget)
        self.manifestGroupBox.setObjectName(u"manifestGroupBox")
        self.gridLayout = QGridLayout(self.manifestGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelSearchTerm = QLabel(self.manifestGroupBox)
        self.labelSearchTerm.setObjectName(u"labelSearchTerm")
        self.labelSearchTerm.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.labelSearchTerm, 0, 0, 1, 1)

        self.lineEditSearch = QLineEdit(self.manifestGroupBox)
        self.lineEditSearch.setObjectName(u"lineEditSearch")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSearch.sizePolicy().hasHeightForWidth())
        self.lineEditSearch.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditSearch, 0, 1, 1, 1)

        self.groupBoxFilter = QGroupBox(self.manifestGroupBox)
        self.groupBoxFilter.setObjectName(u"groupBoxFilter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBoxFilter.sizePolicy().hasHeightForWidth())
        self.groupBoxFilter.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxFilter)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.toolButtonFilterSpecies = QToolButton(self.groupBoxFilter)
        self.toolButtonFilterSpecies.setObjectName(u"toolButtonFilterSpecies")
        self.toolButtonFilterSpecies.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.verticalLayout_3.addWidget(self.toolButtonFilterSpecies)

        self.toolButtonFilterOrgan = QToolButton(self.groupBoxFilter)
        self.toolButtonFilterOrgan.setObjectName(u"toolButtonFilterOrgan")
        self.toolButtonFilterOrgan.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.verticalLayout_3.addWidget(self.toolButtonFilterOrgan)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.groupBoxFilter, 0, 3, 3, 1)

        self.labelSearchBy = QLabel(self.manifestGroupBox)
        self.labelSearchBy.setObjectName(u"labelSearchBy")
        self.labelSearchBy.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.labelSearchBy, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.comboBoxSearchBy = QComboBox(self.manifestGroupBox)
        self.comboBoxSearchBy.addItem("")
        self.comboBoxSearchBy.addItem("")
        self.comboBoxSearchBy.addItem("")
        self.comboBoxSearchBy.setObjectName(u"comboBoxSearchBy")
        self.comboBoxSearchBy.setMinimumSize(QSize(0, 0))
        self.comboBoxSearchBy.setIconSize(QSize(0, 0))
        self.comboBoxSearchBy.setFrame(True)

        self.horizontalLayout_3.addWidget(self.comboBoxSearchBy)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.pushButtonSearch = QPushButton(self.manifestGroupBox)
        self.pushButtonSearch.setObjectName(u"pushButtonSearch")

        self.horizontalLayout_2.addWidget(self.pushButtonSearch)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.groupBoxRestrictTo = QGroupBox(self.manifestGroupBox)
        self.groupBoxRestrictTo.setObjectName(u"groupBoxRestrictTo")
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxRestrictTo)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelDatasetID = QLabel(self.groupBoxRestrictTo)
        self.labelDatasetID.setObjectName(u"labelDatasetID")
        self.labelDatasetID.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.labelDatasetID)

        self.lineEditDatasetID = QLineEdit(self.groupBoxRestrictTo)
        self.lineEditDatasetID.setObjectName(u"lineEditDatasetID")

        self.horizontalLayout_4.addWidget(self.lineEditDatasetID)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.gridLayout.addWidget(self.groupBoxRestrictTo, 0, 2, 3, 1)


        self.verticalLayout_9.addWidget(self.manifestGroupBox)

        self.groupBox = QGroupBox(RetrievePortalDataWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableViewSearchResult = QTableView(self.groupBox)
        self.tableViewSearchResult.setObjectName(u"tableViewSearchResult")
        self.tableViewSearchResult.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableViewSearchResult.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.tableViewSearchResult.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableViewSearchResult.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.tableViewSearchResult)


        self.verticalLayout_9.addWidget(self.groupBox)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frameDownload = QFrame(RetrievePortalDataWidget)
        self.frameDownload.setObjectName(u"frameDownload")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frameDownload.sizePolicy().hasHeightForWidth())
        self.frameDownload.setSizePolicy(sizePolicy2)
        self.frameDownload.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameDownload.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frameDownload)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.pushButtonDownload = QPushButton(self.frameDownload)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout.addWidget(self.pushButtonDownload)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.groupBoxDownloadedFileTree = QGroupBox(self.frameDownload)
        self.groupBoxDownloadedFileTree.setObjectName(u"groupBoxDownloadedFileTree")
        self.verticalLayout = QVBoxLayout(self.groupBoxDownloadedFileTree)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeViewFileBrowser = QTreeView(self.groupBoxDownloadedFileTree)
        self.treeViewFileBrowser.setObjectName(u"treeViewFileBrowser")
        self.treeViewFileBrowser.header().setCascadingSectionResizes(True)

        self.verticalLayout.addWidget(self.treeViewFileBrowser)


        self.verticalLayout_6.addWidget(self.groupBoxDownloadedFileTree)


        self.horizontalLayout_5.addWidget(self.frameDownload)

        self.frameTransfer = QFrame(RetrievePortalDataWidget)
        self.frameTransfer.setObjectName(u"frameTransfer")
        sizePolicy1.setHeightForWidth(self.frameTransfer.sizePolicy().hasHeightForWidth())
        self.frameTransfer.setSizePolicy(sizePolicy1)
        self.frameTransfer.setFrameShape(QFrame.Shape.NoFrame)
        self.frameTransfer.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.frameTransfer)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_5 = QSpacerItem(20, 37, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_8.addItem(self.verticalSpacer_5)

        self.pushButtonTransferIn = QPushButton(self.frameTransfer)
        self.pushButtonTransferIn.setObjectName(u"pushButtonTransferIn")

        self.verticalLayout_8.addWidget(self.pushButtonTransferIn)

        self.verticalSpacer_3 = QSpacerItem(20, 7, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.pushButtonTransferOut = QPushButton(self.frameTransfer)
        self.pushButtonTransferOut.setObjectName(u"pushButtonTransferOut")

        self.verticalLayout_8.addWidget(self.pushButtonTransferOut)

        self.verticalSpacer_4 = QSpacerItem(20, 37, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_8.addItem(self.verticalSpacer_4)


        self.horizontalLayout_5.addWidget(self.frameTransfer)

        self.frameProvide = QFrame(RetrievePortalDataWidget)
        self.frameProvide.setObjectName(u"frameProvide")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(4)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frameProvide.sizePolicy().hasHeightForWidth())
        self.frameProvide.setSizePolicy(sizePolicy3)
        self.frameProvide.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameProvide.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frameProvide)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBoxProvudedFiles = QGroupBox(self.frameProvide)
        self.groupBoxProvudedFiles.setObjectName(u"groupBoxProvudedFiles")
        self.verticalLayout_5 = QVBoxLayout(self.groupBoxProvudedFiles)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listViewProvidedFiles = QListView(self.groupBoxProvudedFiles)
        self.listViewProvidedFiles.setObjectName(u"listViewProvidedFiles")

        self.verticalLayout_5.addWidget(self.listViewProvidedFiles)


        self.verticalLayout_7.addWidget(self.groupBoxProvudedFiles)


        self.horizontalLayout_5.addWidget(self.frameProvide)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setObjectName(u"horizontalLayout1")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout1.addItem(self.horizontalSpacer_8)

        self.pushButtonDone = QPushButton(RetrievePortalDataWidget)
        self.pushButtonDone.setObjectName(u"pushButtonDone")

        self.horizontalLayout1.addWidget(self.pushButtonDone)


        self.verticalLayout_9.addLayout(self.horizontalLayout1)


        self.retranslateUi(RetrievePortalDataWidget)

        QMetaObject.connectSlotsByName(RetrievePortalDataWidget)
    # setupUi

    def retranslateUi(self, RetrievePortalDataWidget):
        RetrievePortalDataWidget.setWindowTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Search tool", None))
        self.labelSearchTerm.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Search term:", None))
        self.groupBoxFilter.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Filter:", None))
        self.toolButtonFilterSpecies.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Species  ", None))
        self.toolButtonFilterOrgan.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Organ  ", None))
        self.labelSearchBy.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Search by:", None))
        self.comboBoxSearchBy.setItemText(0, QCoreApplication.translate("RetrievePortalDataWidget", u"DOI", None))
        self.comboBoxSearchBy.setItemText(1, QCoreApplication.translate("RetrievePortalDataWidget", u"filename", None))
        self.comboBoxSearchBy.setItemText(2, QCoreApplication.translate("RetrievePortalDataWidget", u"mimetype", None))

        self.pushButtonSearch.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Search", None))
        self.groupBoxRestrictTo.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Restrict to:", None))
#if QT_CONFIG(tooltip)
        self.labelDatasetID.setToolTip(QCoreApplication.translate("RetrievePortalDataWidget", u"Restrict the search to the dataset with ID specified here", None))
#endif // QT_CONFIG(tooltip)
        self.labelDatasetID.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Dataset ID:", None))
#if QT_CONFIG(tooltip)
        self.lineEditDatasetID.setToolTip(QCoreApplication.translate("RetrievePortalDataWidget", u"Restrict the search to the dataset with ID specified here", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Search results:", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Download", None))
        self.groupBoxDownloadedFileTree.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Downloaded files:", None))
#if QT_CONFIG(tooltip)
        self.pushButtonTransferIn.setToolTip(QCoreApplication.translate("RetrievePortalDataWidget", u"Add selected file to list of provided files", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonTransferIn.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"-->", None))
#if QT_CONFIG(tooltip)
        self.pushButtonTransferOut.setToolTip(QCoreApplication.translate("RetrievePortalDataWidget", u"Remove selected file to list of provided files", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonTransferOut.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"<--", None))
        self.groupBoxProvudedFiles.setTitle(QCoreApplication.translate("RetrievePortalDataWidget", u"Provided files:", None))
        self.pushButtonDone.setText(QCoreApplication.translate("RetrievePortalDataWidget", u"Done", None))
    # retranslateUi

