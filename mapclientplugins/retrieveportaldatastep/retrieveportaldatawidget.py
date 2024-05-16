import json
import os

from PySide6 import QtCore, QtGui, QtWidgets

from mapclientplugins.retrieveportaldatastep.ui_retrieveportaldatawidget import Ui_RetrievePortalDataWidget

from sparc.client.services.pennsieve import PennsieveService
from sparc.client.services.metadata import MetadataService
from sparc.client.zinchelper import ZincHelper


class RetrievePortalDataWidget(QtWidgets.QWidget):

    def __init__(self, output_dir, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._model = None
        self._selection_model = None
        self._list_files = None
        self._callback = None
        self._output_dir = output_dir
        self._ui = Ui_RetrievePortalDataWidget()
        self._ui.setupUi(self)

        self._pennsieve_service = PennsieveService(connect=False)
        self._scicrunch_service = MetadataService(connect=False)
        self._zinc = ZincHelper()

        self._make_connections()
        self._update_ui()

    def _make_connections(self):
        self._ui.pushButtonSearch.clicked.connect(self._search_button_clicked)
        self._ui.pushButtonDownload.clicked.connect(self._download_button_clicked)
        self._ui.pushButtonExportVTK.clicked.connect(self._export_vtk_button_clicked)
        self._ui.pushButtonAnalyse.clicked.connect(self._analyse_button_clicked)
        self._ui.pushButtonDone.clicked.connect(self._done_button_clicked)

        fileBrowserModel = QtWidgets.QFileSystemModel()
        fileBrowserModel.setRootPath(QtCore.QDir.rootPath())
        self._ui.treeViewFileBrowser.setModel(fileBrowserModel)
        self._ui.treeViewFileBrowser.setRootIndex(fileBrowserModel.index(self._output_dir))

    def _update_ui(self):
        ready = len(self._selection_model.selectedRows()) > 0 if self._selection_model else False
        self._ui.pushButtonAnalyse.setEnabled(ready)
        self._ui.pushButtonDownload.setEnabled(ready)
        self._ui.pushButtonExportVTK.setEnabled(ready)
        self._ui.comboBoxAnalyse.setEnabled(ready)

    def _set_table(self, file_list):
        self._model = QtGui.QStandardItemModel(0, 3)
        self._model.setHorizontalHeaderLabels(['Filename', 'Dataset ID', 'Dataset Version'])
        for row in range(len(file_list)):
            item = QtGui.QStandardItem("%s" % (file_list[row]["name"]))
            self._model.setItem(row, 0, item)
            item = QtGui.QStandardItem("%s" % (file_list[row]["datasetId"]))
            self._model.setItem(row, 1, item)
            item = QtGui.QStandardItem("%s" % (file_list[row]["datasetVersion"]))
            self._model.setItem(row, 2, item)

        self._ui.tableViewSearchResult.setModel(self._model)
        self._ui.tableViewSearchResult.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._ui.tableViewSearchResult.horizontalHeader().setStretchLastSection(True)
        self._selection_model = self._ui.tableViewSearchResult.selectionModel()
        self._selection_model.selectionChanged.connect(self._update_ui)

    def _retrieve_data(self):
        # Get user’s input
        filename = self._ui.lineEditSearch.text()
        dataset_id = self._ui.lineEditDatasetID.text()
        # Use sparc.client to retrieve files
        self._list_files = self._pennsieve_service.list_files(
            limit=100,
            query=filename,
            dataset_id=dataset_id,
        )
        # Display the search result in a table view.
        self._set_table(self._list_files)

    def _search_button_clicked(self):
        self._retrieve_data()

    def _download_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()
        for index in indexes:
            output_name = os.path.join(self._output_dir, self._list_files[index.row()]['name'])
            self._pennsieve_service.download_file(self._list_files[index.row()], output_name)

    def _export_vtk_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()
        for index in indexes:
            output_name = os.path.join(self._output_dir, self._list_files[index.row()]['name'])
            self._zinc.get_mbf_vtk(self._list_files[index.row()]['datasetId'], output_name)

    def _analyse_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()
        for index in indexes:
            self._pennsieve_service.download_file(self._list_files[index.row()])
            try:
                organ = self._ui.comboBoxAnalyse.currentText()
                result = self._zinc.analyse(self._list_files[index.row()]['name'], organ)
            except ValueError:
                result = "Input file must be an MBF XML file"
                
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Analyse result")
            dlg.setText(result)
            dlg.exec_()

    def search_scaffolds(self):
        query = '''
        {
            "size": 20,
            "from": 0,
            "query": {
                "query_string": {
                    "fields": [
                        "objects.additional_mimetype.name"
                    ],
                    "query": "(*x.vnd.abi.scaffold*) AND (*meta)"
                }
            }
        }
        '''
        result = self._scicrunch_service.search_portal_data(json.loads(query))

    def _get_output_files(self):
        return [os.path.join(self._output_dir, f) for f in os.listdir(self._output_dir) if os.path.isfile(os.path.join(self._output_dir, f))]

    def _done_button_clicked(self):
        self._callback()

    def registerDoneExecution(self, callback):
        self._callback = callback
