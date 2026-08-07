import base64
import hashlib
import json
import os
import pathlib

import requests
import threading

from urllib.parse import urlparse

from PySide6 import QtCore, QtGui, QtWidgets

from mapclientplugins.retrieveportaldatastep.ui_retrieveportaldatawidget import Ui_RetrievePortalDataWidget
from mapclientplugins.retrieveportaldatastep.definitions import DEFAULT_VALUE, DEFAULT_HEADERS
from mapclientplugins.retrieveportaldatastep.scicrunch_requests import create_filter_request, \
    form_scicrunch_match_request
from mapclientplugins.retrieveportaldatastep.downloadprogressdialog import DownloadProgressDialog

from mapclient.settings.general import get_data_directory

POSSIBLE_DOI_SUFFIXES = ["DOI:", "https://doi.org/", "http://dx.doi.org/"]

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
    for suffix in POSSIBLE_DOI_SUFFIXES:
        if text.startswith(suffix):
            text = text.replace(suffix, "")
            text = text.strip()

    return text


def _create_search_result(obj, result):
    return {
        "name": obj["name"],
        "datasetId": result["_source"]["object_id"],
        "datasetVersion": result["_source"]["pennsieve"]["version"]["identifier"],
        "mimetype": obj["additional_mimetype"]["name"] if obj["additional_mimetype"]["name"] else obj["mimetype"][
            "name"],
        "datasetPath": obj["dataset"]["path"],
        "uri": "",
    }


def _return_scicrunch_search_result(search_text, search_type, facets):
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
        req = form_scicrunch_match_request("item.curie", search_text, source_fields, size=result_size, start=0)
    else:
        print("Something has gone wrong!", search_type, "is not a handled search type.")

    response = _do_scicrunch_request(req)
    return response.json(), result_size, target_field_parts


def _scicrunch_search(search_text, search_type, facets=None):
    post_result, result_size, target_field_parts = _return_scicrunch_search_result(search_text, search_type, facets)
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
    if uri:
        parsed_object = urlparse(uri)
        return parsed_object.path.split("files/")[1]

    return ''


def get_sha256(file_path):
    if not os.path.isfile(file_path):
        return '---'

    with open(file_path, 'rb') as f:
        buf = f.read()
        sha256_hash = hashlib.sha256(buf).digest()

    return base64.b64encode(sha256_hash).decode()


def _form_pennsieve_download_file_endpoint(item):
    return f'https://api.pennsieve.io/discover/datasets/{item["datasetId"]}/versions/{item["datasetVersion"]}/files'


def safe_makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except FileExistsError:
        # Another thread might have created it between the check and the call
        pass


class DownloadSignals(QtCore.QObject):
    progress = QtCore.Signal(str, float)
    finished = QtCore.Signal(str, str)


class FileDownloadTask(QtCore.QRunnable):

    def __init__(self, item, output_dir, cancel_event: threading.Event):
        super().__init__()
        self._item = item
        self._output_dir = output_dir
        self._cancel_event = cancel_event
        self.signals = DownloadSignals()

    def run(self):
        # If cancellation was already requested before this task started, exit early
        if self._cancel_event.is_set():
            return

        local_destination = "error"
        was_cancelled = False

        try:
            local_destination = _form_local_destination(self._output_dir, self._item)
            local_dir = os.path.dirname(local_destination)
            safe_makedirs(local_dir)

            uri = _form_pennsieve_download_file_endpoint(self._item)
            params = (
                {'path': self._item['datasetPath']}
                if self._item['datasetPath'].startswith('files/')
                else {'path': f'files/{self._item["datasetPath"]}'}
            )

            response = requests.get(uri, params=params, stream=True)

            json_data = response.json()
            if json_data.get('sha256', '') != get_sha256(local_destination):
                req = {
                    "data": {
                        "paths": [params['path']],
                        "datasetId": self._item['datasetId'],
                        "version": self._item['datasetVersion'],
                    }
                }
                discover_zipit_url = "https://api.pennsieve.io/zipit/discover"
                headers = {"content-type": "application/json"}
                last_emitted_progress = -1

                # Use requests with a timeout so threads don't hang indefinitely on bad connections.
                with requests.post(
                    discover_zipit_url, json=req, headers=headers, stream=True, timeout=10
                ) as response:
                    response.raise_for_status()

                    file_size = json_data.get('size', 0)
                    bytes_downloaded = 0
                    # Write chunks to disk and check cancellation flag periodically.
                    with open(local_destination, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=64 * 1024):  # 64 KB chunks
                            if self._cancel_event.is_set():
                                was_cancelled = True
                                break
                            if chunk:
                                bytes_downloaded += len(chunk)
                                f.write(chunk)
                                current_progress = bytes_downloaded / file_size
                                if current_progress > 1.1 * last_emitted_progress:
                                    self.signals.progress.emit(local_destination, current_progress)
                                    last_emitted_progress = current_progress

        except Exception as e:
            print("Handling unknown exception in FileDownloadTask:")
            print(e)

        finally:
            if was_cancelled:
                # Cleanup partially downloaded file on cancellation.
                if os.path.exists(local_destination) and local_destination != "error":
                    try:
                        os.remove(local_destination)
                    except OSError:
                        pass
            else:
                # Only emit finished signal if the download wasn't cancelled.
                self.signals.finished.emit(local_destination, json.dumps(self._item))


class SearchResultFilterProxy(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._row = -1
        self._filter = ""

    def set_filter_on_row(self, row, filter_text):
        self._row = row
        self._filter = filter_text
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):

        if self._filter == "":
            return True

        model = self.sourceModel()

        if self._row == -1:
            all_text = [model.index(source_row, column).data() or "" for column in range(model.columnCount())]
            text = ' '.join(all_text)
        else:
            text = model.index(source_row, self._row).data() or ""

        reg_exp = QtCore.QRegularExpression.fromWildcard(
            self._filter,
            options=QtCore.QRegularExpression.WildcardConversionOption.UnanchoredWildcardConversion
        )

        return reg_exp.match(text).hasMatch()


class RetrievePortalDataWidget(QtWidgets.QWidget):

    def __init__(self, output_dir, output_files, settings_filename, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._model = None
        self._proxy_model = None
        self._selection_model = None
        self._list_files = None
        self._callback = None
        self._cancel_event = None
        self._completing = False
        self._dataset_id_completing = False
        self._output_dir = output_dir
        self._settings_filename = settings_filename

        self._ui = Ui_RetrievePortalDataWidget()
        self._ui.setupUi(self)
        self._ui.toolButtonFilterSpecies.setMenu(_create_filter_menu(self._ui.toolButtonFilterSpecies, SPECIES))
        self._ui.toolButtonFilterOrgan.setMenu(_create_filter_menu(self._ui.toolButtonFilterOrgan, ORGANS))

        _initialise_search_bank()

        self._completer = QtWidgets.QCompleter()
        self._completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self._completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self._completer.setWidget(self._ui.lineEditSearch)
        self._search_completer_model = None
        self._update_completer_model(self._ui.comboBoxSearchBy.currentText())

        self._dataset_id_completer = QtWidgets.QCompleter(_word_bank('dataset-id'))
        self._dataset_id_completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self._dataset_id_completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)

        file_browser_model = QtWidgets.QFileSystemModel()
        file_browser_model.setRootPath(QtCore.QDir.rootPath())
        self._ui.treeViewFileBrowser.setModel(file_browser_model)
        self._ui.treeViewFileBrowser.setRootIndex(file_browser_model.index(self._output_dir))

        list_model = QtCore.QStringListModel(output_files)
        self._ui.listViewProvidedFiles.setModel(list_model)

        self._make_connections()
        self._update_ui()

        # Check for missing cached files on startup.
        QtCore.QTimer.singleShot(100, self._check_and_restore_cache)

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
        self._ui.comboBoxSearchResultFilter.currentIndexChanged.connect(self._search_result_filter_changed)

    def _update_ui(self):
        results_available = self._proxy_model.rowCount() > 0 if self._proxy_model else False
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
        self._ui.pushButtonClearSelection.setEnabled(ready)
        self._ui.pushButtonSelectAll.setEnabled(results_available)
        self._ui.lineEditSearchResultFilter.setEnabled(results_available)
        self._ui.comboBoxSearchResultFilter.setEnabled(results_available)

    def _file_browser_expanded(self, index):
        if index.isValid() and index.column() == 0:
            self._ui.treeViewFileBrowser.resizeColumnToContents(0)

    def _set_table(self, file_list):
        self._model = QtGui.QStandardItemModel(0, 4)
        self._model.setHorizontalHeaderLabels(['Filename', 'Dataset ID', 'Dataset Version', 'Mimetype', 'Dataset Path'])
        for row, file_info in enumerate(file_list):
            item = QtGui.QStandardItem(f"{file_info['name']}")
            item.setData(file_info, QtCore.Qt.ItemDataRole.UserRole)
            self._model.setItem(row, 0, item)
            item = QtGui.QStandardItem(f"{file_info['datasetId']}")
            self._model.setItem(row, 1, item)
            item = QtGui.QStandardItem(f"{file_info['datasetVersion']}")
            self._model.setItem(row, 2, item)
            mimetype_approx = file_info.get('mimetype', file_info.get('fileType', ''))
            item = QtGui.QStandardItem(f"{mimetype_approx}")
            self._model.setItem(row, 3, item)
            dataset_path = file_info.get('datasetPath', _determine_dataset_path(file_info['uri']))
            item = QtGui.QStandardItem(f"{dataset_path}")
            self._model.setItem(row, 4, item)

        self._proxy_model = SearchResultFilterProxy(self)
        self._proxy_model.setSourceModel(self._model)
        self._ui.tableViewSearchResult.setModel(self._proxy_model)
        self._ui.tableViewSearchResult.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._ui.tableViewSearchResult.horizontalHeader().setStretchLastSection(True)
        self._selection_model = self._ui.tableViewSearchResult.selectionModel()
        self._selection_model.selectionChanged.connect(self._update_ui)
        self._ui.pushButtonClearSelection.clicked.connect(self._selection_model.clearSelection)
        self._ui.pushButtonSelectAll.clicked.connect(self._select_all_search_results)
        self._ui.lineEditSearchResultFilter.textEdited.connect(self._filter_search_results)

    def _filter_search_results(self):
        self._search_result_filter_changed()

    def _search_result_filter_changed(self):
        filter_type_map = {
            "Dataset Path": 4,
            "Filename": 0,
            "Mimetype": 3,
        }
        current_filter = self._ui.comboBoxSearchResultFilter.currentText()
        current_text = self._ui.lineEditSearchResultFilter.text()
        self._proxy_model.set_filter_on_row(filter_type_map.get(current_filter, -1), current_text)

    def _select_all_search_results(self):
        top_left = self._proxy_model.index(0, 0)
        bottom_right = self._proxy_model.index(self._proxy_model.rowCount() - 1, self._proxy_model.columnCount() - 1)
        selection = QtCore.QItemSelection(top_left, bottom_right)
        self._selection_model.select(selection, QtCore.QItemSelectionModel.SelectionFlag.Select)

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

        # Retrieve files
        if search_by == "filename":
            discover_search_files_url = "https://api.pennsieve.io/discover/search/files"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json; charset=utf-8",
            }
            params = {
                "limit": 100,
                "offset": 0,
                "query": search_text,
                "datasetId": dataset_id,
            }
            response = requests.get(discover_search_files_url, headers=headers, params=params)
            if response.status_code == 200:
                json_data = response.json()
                self._list_files = json_data['files']
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
        self._update_ui()

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

    def _check_and_restore_cache(self):
        """Scans manifest and provided files list to restore missing items."""
        manifest = _load_manifest(self._settings_filename)
        if not manifest:
            return

        missing_items = []
        provided_files = self.get_output_files()

        for rel_path, item_data in manifest.items():
            full_path = os.path.join(self._output_dir, rel_path)

            # If file is missing or explicitly needed by the provided files list
            if not os.path.exists(full_path) or (
                    rel_path in provided_files and not os.path.exists(full_path)
            ):
                missing_items.append(item_data)

        if missing_items:
            missing_count = len(missing_items)
            singular = missing_count == 1
            reply = QtWidgets.QMessageBox.question(
                self,
                "Restore Missing Cache",
                f"Could not find {missing_count} provided file{'' if singular else 's'} cached locally."
                f" Would you like to restore {'it' if singular else 'them'} now?",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self._start_download_batch(missing_items)

    def _start_download_batch(self, items_data):
        if not items_data:
            return

        thread_pool = QtCore.QThreadPool.globalInstance()
        self._cancel_event = threading.Event()

        download_dialog = DownloadProgressDialog(len(items_data), self)
        download_dialog.show()
        download_dialog.rejected.connect(self._cancelled_download)

        for item_data in items_data:
            task = FileDownloadTask(item_data, self._output_dir, self._cancel_event)

            task.signals.finished.connect(self._on_download_finished)
            task.signals.finished.connect(download_dialog.on_file_downloaded)
            task.signals.progress.connect(download_dialog.on_file_progress)

            thread_pool.start(task)

    def _on_download_finished(self, local_destination, item_data_str):
        if local_destination != "error" and os.path.exists(local_destination):
            # Update cache manifest.
            item_data = json.loads(item_data_str)
            _save_manifest_entry(self._output_dir, item_data, self._settings_filename)

            # Automatically populate output files list if not present.
            self._populate_output_list(local_destination)

    def _populate_output_list(self, local_destination):
        rel_path = os.path.relpath(local_destination, self._output_dir)
        list_model = self._ui.listViewProvidedFiles.model()
        current_strings = list_model.stringList()
        if rel_path not in current_strings:
            current_strings.append(rel_path)
            list_model.setStringList(current_strings)
            self._update_ui()

    def _download_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()
        items_to_download = []

        for index in indexes:
            model_index = index.siblingAtColumn(0)
            item_data = model_index.data(QtCore.Qt.ItemDataRole.UserRole)
            if item_data.get('datasetPath') is None:
                item_data['datasetPath'] = _determine_dataset_path(item_data['uri'])
            items_to_download.append(item_data)

        self._start_download_batch(items_to_download)

    def _cancelled_download(self):
        # 1. Signal all currently executing threads to stop streaming.
        if self._cancel_event is not None:
            self._cancel_event.set()

        # 2. Clear any tasks waiting in the QThreadPool queue that haven't started yet.
        QtCore.QThreadPool.globalInstance().clear()

    def _export_vtk_button_clicked(self):
        indexes = self._ui.tableViewSearchResult.selectionModel().selectedRows()
        for index in indexes:
            output_name = os.path.join(self._output_dir, self._list_files[index.row()]['name'])
            print('DISABLED: Exporting ' + output_name)

    def get_output_files(self):
        list_model = self._ui.listViewProvidedFiles.model()
        return list_model.stringList()

    def _done_button_clicked(self):
        # Validate all provided files exist before completing step
        manifest = _load_manifest(self._settings_filename)
        provided_files = self.get_output_files()
        missing_required = []

        for rel_path in provided_files:
            full_path = os.path.join(self._output_dir, rel_path)
            if not os.path.exists(full_path):
                if rel_path in manifest:
                    missing_required.append(manifest[rel_path])

        if missing_required:
            reply = QtWidgets.QMessageBox.warning(
                self,
                "Missing Files",
                f"{len(missing_required)} required file(s) are missing from disk. Download them before proceeding?",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self._start_download_batch(missing_required)
                return

        self._callback()

    def register_done_execution(self, callback):
        self._callback = callback

    def set_identifier(self, identifier):
        self._ui.manifestGroupBox.setTitle(f"Identifier: {identifier}")


def _form_local_destination(base_dir, info):
    near_relative_local_path = info['datasetPath'].replace('files/', '')
    return os.path.join(base_dir, str(info['datasetId']), str(info['datasetVersion']), near_relative_local_path)


def _load_manifest(manifest_path):
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f).get('manifest', {})
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_manifest_entry(output_dir, item_data, manifest_path):
    manifest = _load_manifest(manifest_path)
    local_dest = _form_local_destination(output_dir, item_data)
    rel_path = os.path.relpath(local_dest, output_dir)
    path_key = pathlib.PureWindowsPath(rel_path).as_posix()
    # Save metadata indexed by relative file path.
    manifest[path_key] = item_data

    safe_makedirs(output_dir)
    try:
        with open(manifest_path) as f:
            all_content = json.load(f)
        all_content.update({'manifest': manifest})
        with open(manifest_path, 'w') as f:
            json.dump(all_content, f, indent=2)
    except OSError as e:
        print(f"Error updating download manifest: {e}")

