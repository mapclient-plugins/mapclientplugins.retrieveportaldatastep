import json
import os
import hashlib
from urllib.parse import urlparse

import requests
from PySide6 import QtCore, QtGui, QtWidgets

from mapclientplugins.retrieveportaldatastep.ui_retrieveportaldatawidget import Ui_RetrievePortalDataWidget
from mapclientplugins.retrieveportaldatastep.definitions import DEFAULT_VALUE, DEFAULT_HEADERS
from mapclientplugins.retrieveportaldatastep.scicrunch_requests import create_filter_request, form_scicrunch_match_request

from sparc.client.services.pennsieve import PennsieveService
from sparc.client.services.metadata import MetadataService
from sparc.client.zinchelper import ZincHelper

from mapclient.settings.general import get_data_directory

SPECIES = [
    "Cat",
    "Dog",
    "Ferret",
    "Human",
    "Mouse",
    "Pig",
    "Rabbit",
    "Rat",
    "Sheep",
]
ORGANS = [
    "Stomach",
    "Heart",
    "Lung",
]
SEARCH_BANK_FILENAME = "retrieveportaldata-search-bank.json"
API_KEY_NAME = "SCICRUNCH_API_KEY"


def _create_filter_menu(parent, labels):
    filter_menu = QtWidgets.QMenu(parent)
    for label in labels:
        action = filter_menu.addAction(label)
        action.setCheckable(True)

    return filter_menu


def _initialise_search_bank():
    search_bank_file = os.path.join(get_data_directory(), SEARCH_BANK_FILENAME)
    if not os.path.isfile(search_bank_file):
        with open(search_bank_file, "w") as fh:
            json.dump({}, fh)


def _search_bank():
    with open(os.path.join(get_data_directory(), SEARCH_BANK_FILENAME)) as fh:
        search_bank = json.load(fh)

    return search_bank


def _update_search_bank(search_bank):
    with open(os.path.join(get_data_directory(), SEARCH_BANK_FILENAME), "w") as fh:
        json.dump(search_bank, fh)


def _word_bank(key):
    search_bank = _search_bank()
    return search_bank.get(key, [])


def _save_to_search_bank(key, value):
    search_bank = _search_bank()

    existing = search_bank.get(key, [])
    if not existing:
        search_bank[key] = existing

    if value not in existing:
        existing.append(value)
        _update_search_bank(search_bank)


def _extract_facets(tool_button):
    species_menu = tool_button.menu()
    facets = []
    for action in species_menu.actions():
        if action.isChecked():
            facets.append(action.text())

    return facets


def _do_scicrunch_request(req):
    base_url = "https://scicrunch.org/api/1/elastic/SPARC_PortalDatasets_pr/_search"
    params = {
        "api_key": os.environ.get(API_KEY_NAME, DEFAULT_VALUE),
    }
    headers = DEFAULT_HEADERS
    return requests.post(base_url, json=req, params=params, headers=headers)


def _standardise_doi_form(text):
    POSSIBLE_SUFFIXES = ["DOI:", "https://doi.org/", "http://dx.doi.org/"]
    for suffix in POSSIBLE_SUFFIXES:
        if text.startswith(suffix):
            text = text.replace(suffix)
            text = text.strip()

    return text


def _create_search_result(obj, result):
    return {
        "name": obj["name"],
        "datasetId": result["_source"]["object_id"],
        "datasetVersion": result["_source"]["pennsieve"]["version"]["identifier"],
        "mimetype": obj["additional_mimetype"]["name"] if obj["additional_mimetype"]["name"] else obj["mimetype"]["name"],
        "datasetPath": obj["dataset"]["path"],
        "uri": "",
    }


def _return_scicruncth_search_result(search_text, search_type, facets):
    result_size = 100
    target_field_parts = []
    req = {}
    if search_type == "mimetype":
        target_field_location = "objects.additional_mimetype.name"
        target_field_parts = target_field_location.split(".")[1:]
        req = create_filter_request(search_text, facets, result_size, 0, fields=[target_field_location])
    elif search_type == "DOI":
        source_fields = [
            "object_id",
            "pennsieve.version.identifier",
            "item.curie",
            "item.name",
            "objects.name",
            "objects.mimetype.name",
            "objects.additional_mimetype.name",
            "objects.dataset.path"
        ]
        req = form_scicrunch_match_request("item.curie", search_text, source_fields)
    else:
        print("Something has gone wrong!", search_type, "is not a handled search type.")

    response = _do_scicrunch_request(req)
    return response.json(), result_size, target_field_parts


def _scicrunch_search(search_text, search_type, facets=None):
    post_result, result_size, target_field_parts = _return_scicruncth_search_result(search_text, search_type, facets)
    search_result = []
    if "hits" in post_result and post_result["hits"]["total"] > 0:
        for hit_index in range(min(result_size, post_result["hits"]["total"])):
            result = post_result["hits"]["hits"][hit_index]
            source = result["_source"]

            for obj in source["objects"]:

                if obj["mimetype"]["name"] != "inode/directory":
                    if search_type == "mimetype":
                        target_field_value = obj
                        for field in target_field_parts:
                            target_field_value = target_field_value.get(field, {})
                        if target_field_value == search_text:
                            search_result.append(_create_search_result(obj, result))
                    elif search_type == "DOI":
                        search_result.append(_create_search_result(obj, result))
    else:
        print("Got nothing.")

    return search_result


def _determine_dataset_path(uri):
    parsed_object = urlparse(uri)
    return parsed_object.path.split("files/")[1]


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
        self._ui.toolButtonFilterSpecies.setMenu(_create_filter_menu(self._ui.toolButtonFilterSpecies, SPECIES))
        self._ui.toolButtonFilterOrgan.setMenu(_create_filter_menu(self._ui.toolButtonFilterOrgan, ORGANS))

        _initialise_search_bank()

        self._pennsieve_service = PennsieveService(connect=False)
        self._scicrunch_service = MetadataService()
        self._zinc = ZincHelper()

        self._completer = QtWidgets.QCompleter()
        self._completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self._completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self._completer.setWidget(self._ui.lineEditSearch)
        self._search_completer_model = None
        self._update_completer_model(self._ui.comboBoxSearchBy.currentText())

        self._dataset_id_completer = QtWidgets.QCompleter(_word_bank('dataset-id'))
        self._dataset_id_completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self._dataset_id_completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)

        fileBrowserModel = QtWidgets.QFileSystemModel()
        fileBrowserModel.setRootPath(QtCore.QDir.rootPath())
        self._ui.treeViewFileBrowser.setModel(fileBrowserModel)
        self._ui.treeViewFileBrowser.setRootIndex(fileBrowserModel.index(self._output_dir))

        listModel = QtCore.QStringListModel()
        self._ui.listViewProvidedFiles.setModel(listModel)

        self._make_connections()
        self._update_ui()

        self._completing = False
        self._dataset_id_completing = False

    def _make_connections(self):
        self._ui.pushButtonSearch.clicked.connect(self._search_button_clicked)
        self._ui.pushButtonDownload.clicked.connect(self._download_button_clicked)
        self._ui.pushButtonDone.clicked.connect(self._done_button_clicked)
        self._ui.comboBoxSearchBy.currentTextChanged.connect(self._search_by_changed)
        self._ui.lineEditSearch.textChanged.connect(self._search_text_changed)
        self._ui.treeViewFileBrowser.expanded.connect(self._file_browser_expanded)
        self._completer.activated.connect(self._handle_completion)
        self._dataset_id_completer.activated.connect(self._handle_dataset_id_completion)
        self._ui.pushButtonTransferIn.clicked.connect(self._transfer_in_clicked)
        self._ui.pushButtonTransferOut.clicked.connect(self._transfer_out_clicked)

        self._file_selection_model = self._ui.treeViewFileBrowser.selectionModel()
        self._file_selection_model.selectionChanged.connect(self._update_ui)
        self._provide_selection_model = self._ui.listViewProvidedFiles.selectionModel()
        self._provide_selection_model.selectionChanged.connect(self._update_ui)

    def _update_ui(self):
        ready = len(self._selection_model.selectedRows()) > 0 if self._selection_model else False
        transfer_in = len(self._file_selection_model.selectedRows()) > 0 if self._file_selection_model else False
        transfer_out = len(self._provide_selection_model.selectedRows()) > 0 if self._provide_selection_model else False
        search_text = len(self._ui.lineEditSearch.text()) > 0
        file_search = self._ui.comboBoxSearchBy.currentIndex() == 1
        mimetype_search = self._ui.comboBoxSearchBy.currentIndex() == 2

        self._ui.groupBoxFilter.setEnabled(mimetype_search)
        self._ui.groupBoxRestrictTo.setEnabled(file_search)
        self._ui.pushButtonDownload.setEnabled(ready)
        self._ui.pushButtonTransferIn.setEnabled(transfer_in)
        self._ui.pushButtonTransferOut.setEnabled(transfer_out)
        self._ui.pushButtonSearch.setEnabled(search_text)

    def _file_browser_expanded(self, index):
        if index.isValid() and index.column() == 0:
            self._ui.treeViewFileBrowser.resizeColumnToContents(0)

    def _set_table(self, file_list):
        self._model = QtGui.QStandardItemModel(0, 4)
        self._model.setHorizontalHeaderLabels(['Filename', 'Dataset ID', 'Dataset Version', 'Mimetype', 'Dataset Path'])
        for row in range(len(file_list)):
            item = QtGui.QStandardItem(f"{file_list[row]['name']}")
            self._model.setItem(row, 0, item)
            item = QtGui.QStandardItem(f"{file_list[row]['datasetId']}")
            self._model.setItem(row, 1, item)
            item = QtGui.QStandardItem(f"{file_list[row]['datasetVersion']}")
            self._model.setItem(row, 2, item)
            mimetype_approx = file_list[row]['mimetype'] if file_list[row].get('mimetype', '') else file_list[row]['fileType']
            item = QtGui.QStandardItem(f"{mimetype_approx}")
            self._model.setItem(row, 3, item)
            dataset_path = file_list[row]['datasetPath'] if file_list[row].get('datasetPath', '') else _determine_dataset_path(file_list[row]['uri'])
            item = QtGui.QStandardItem(f"{dataset_path}")
            self._model.setItem(row, 4, item)

        self._ui.tableViewSearchResult.setModel(self._model)
        self._ui.tableViewSearchResult.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._ui.tableViewSearchResult.horizontalHeader().setStretchLastSection(True)
        self._selection_model = self._ui.tableViewSearchResult.selectionModel()
        self._selection_model.selectionChanged.connect(self._update_ui)

    def _transfer_in_clicked(self):
        indexes = self._ui.treeViewFileBrowser.selectionModel().selectedRows()
        model = self._ui.treeViewFileBrowser.model()
        list_model = self._ui.listViewProvidedFiles.model()
        current_strings = list_model.stringList()
        set_of_current_strings = set(current_strings)
        for index in indexes:
            relative_path = os.path.relpath(model.filePath(index), self._output_dir)
            set_of_current_strings.add(relative_path)

        list_model.setStringList(list(set_of_current_strings))

    def _transfer_out_clicked(self):
        indexes = self._ui.listViewProvidedFiles.selectionModel().selectedRows()
        list_model = self._ui.listViewProvidedFiles.model()
        current_strings = list_model.stringList()
        rows_to_delete = []
        for index in indexes:
            rows_to_delete.append(index.row())

        for row in reversed(sorted(rows_to_delete)):
            del current_strings[row]

        list_model.setStringList(current_strings)
        self._update_ui()

    def _retrieve_data(self):
        # Get user’s input
        search_text = self._ui.lineEditSearch.text()
        search_by = self._ui.comboBoxSearchBy.currentText()
        dataset_id = self._ui.lineEditDatasetID.text()

        # Use sparc.client to retrieve files
        if search_by == "filename":
            self._list_files = self._pennsieve_service.list_files(
                limit=100,
                query=search_text,
                dataset_id=dataset_id,
            )
        elif search_by == "mimetype":
            facets = {
                'species': _extract_facets(self._ui.toolButtonFilterSpecies),
                'organ': _extract_facets(self._ui.toolButtonFilterOrgan),
            }

            self._list_files = _scicrunch_search(search_text, search_by, facets)
        elif search_by == "DOI":
            search_text = _standardise_doi_form(search_text)
            self._list_files = _scicrunch_search(search_text, search_by)
        else:
            print("Not handling this type of search yet!")

        # Display the search result in a table view.
        self._set_table(self._list_files)
        self._ui.pushButtonSearch.setText("Search")
        self._ui.pushButtonSearch.setEnabled(True)

    def _update_completer_model(self, text):
        word_bank = _word_bank(text)
        self._search_completer_model = QtCore.QStringListModel(word_bank)
        self._completer.setModel(self._search_completer_model)

    def _search_by_changed(self, text):
        self._update_ui()
        self._update_completer_model(text)

    def _search_text_changed(self, text):
        if not self._completing:
            found = False
            prefix = text.rpartition(',')[-1]
            if len(prefix) > 1:
                self._completer.setCompletionPrefix(prefix)
                if self._completer.currentRow() >= 0:
                    found = True
            if found:
                self._completer.complete()
            else:
                self._completer.popup().hide()
            self._update_ui()

    def _dataset_id_text_changed(self, text):
        if not self._dataset_id_completing:
            found = False
            prefix = text.rpartition(',')[-1]
            if len(prefix) > 1:
                self._dataset_id_completer.setCompletionPrefix(prefix)
                if self._dataset_id_completer.currentRow() >= 0:
                    found = True
            if found:
                self._dataset_id_completer.complete()
            else:
                self._dataset_id_completer.popup().hide()

    def _handle_completion(self, text):
        if not self._completing:
            self._completing = True
            prefix = self._completer.completionPrefix()
            self._ui.lineEditSearch.setText(self._ui.lineEditSearch.text()[:-len(prefix)] + text)
            self._completing = False

    def _handle_dataset_id_completion(self, text):
        if not self._dataset_id_completing:
            self._dataset_id_completing = True
            prefix = self._dataset_id_completer.completionPrefix()
            self._ui.lineEditDatasetID.setText(self._ui.lineEditDatasetID.text()[:-len(prefix)] + text)
            self._dataset_id_completing = False

    def _save_search(self):
        search_by = self._ui.comboBoxSearchBy.currentText()
        search_text = self._ui.lineEditSearch.text()
        _save_to_search_bank(search_by, search_text)
        dataset_id = self._ui.lineEditDatasetID.text()
        if dataset_id:
            _save_to_search_bank("dataset-id", dataset_id)

    def _search_button_clicked(self):
        self._ui.pushButtonSearch.setText("   ...   ")
        self._ui.pushButtonSearch.setEnabled(False)
        self._retrieve_data()
        self._save_search()

    def _file_exists(self, filename):
        return filename in [f for f in os.listdir(self._output_dir) if os.path.isfile(os.path.join(self._output_dir, f))]

    def _file_has_updates(self, filename):
        return filename in [f for f in os.listdir(self._output_dir) if os.path.isfile(os.path.join(self._output_dir, f))]

    def _check_same_file(self, file1, file2):
        digests = []
        hasher = hashlib.md5()
        with open(file1, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            a = hasher.hexdigest()
            digests.append(a)
            print(a)
        with open(file2, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            a = hasher.hexdigest()
            digests.append(a)
            print(a)

        print(digests[0] == digests[1])
        return digests[0] == digests[1]

    def _get_pennsieve_uri_suffix(self, dataset_id):
        result = self._pennsieve_service.list_files(dataset_id=dataset_id, query='manifest', file_type='json')
        return result[0]["uri"].replace("manifest.json", "")

    def _download_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()

        # Pre-search for missing Pennsieve URIs.
        missing_uris = {}
        for index in indexes:
            item = self._list_files[index.row()]
            if not item["uri"] and item["datasetId"] not in missing_uris:
                missing_uris[item["datasetId"]] = self._get_pennsieve_uri_suffix(item["datasetId"])

        # Download files one at a time.
        for index in indexes:
            item = self._list_files[index.row()]
            _fix_missing_uri(item, missing_uris)
            local_destination = _form_local_destination(self._output_dir, item)

            # Prepare missing directory structure for asset.
            local_dir = os.path.dirname(local_destination)
            if not os.path.isdir(local_dir):
                os.makedirs(local_dir)

            do_download = False
            if self._file_exists(local_destination):
                dlg = QtWidgets.QMessageBox(self)
                dlg.setWindowTitle("File already exists!")
                dlg.setText("Do you want to replace the existing file?")
                dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                ret = dlg.exec()
                if ret == QtWidgets.QMessageBox.StandardButton.Yes:
                    do_download = True
            else:
                do_download = True

            if do_download:
                self._pennsieve_service.download_file(item, local_destination)

    def _export_vtk_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()
        for index in indexes:
            output_name = os.path.join(self._output_dir, self._list_files[index.row()]['name'])
            self._zinc.get_mbf_vtk(self._list_files[index.row()]['datasetId'], output_name)

    def get_output_files(self):
        list_model = self._ui.listViewProvidedFiles.model()
        current_strings = list_model.stringList()
        return [os.path.join(self._output_dir, f) for f in current_strings]

    def _done_button_clicked(self):
        self._callback()

    def register_done_execution(self, callback):
        self._callback = callback


def _fix_missing_uri(item, missing_uris):
    if not item["uri"]:
        uri_suffix = missing_uris[item["datasetId"]]
        item["uri"] = f"{uri_suffix}files/{item['datasetPath']}"


def _form_local_destination(base_dir, info):
    parsed_object = urlparse(info["uri"])
    near_relative_local_path = parsed_object.path.replace("files/", "")
    index = near_relative_local_path.find("/")
    relative_local_path = near_relative_local_path[index + 1:]

    return os.path.join(base_dir, relative_local_path)
