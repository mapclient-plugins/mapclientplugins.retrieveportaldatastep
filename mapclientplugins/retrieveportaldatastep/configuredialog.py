import os
import pathlib

from PySide6 import QtWidgets
from mapclientplugins.retrieveportaldatastep.ui_configuredialog import Ui_ConfigureDialog

from mapclient.settings.general import get_data_directory

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


def _global_output_directory():
    return os.path.join(get_data_directory(), 'retrieveportaldata-downloads')


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a placeholder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._workflow_location = None
        self._previous_location = ''

        self._make_connections()

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def _make_connections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
        self._ui.pushButtonOutputDirectory.clicked.connect(self._directory_chooser_clicked)

    def _directory_chooser_clicked(self):
        # Second parameter returned is the filter chosen
        if not self._previous_location:
            self._previous_location = self._workflow_location

        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination for export', self._previous_location)

        if location:
            self._previous_location = location
            display_location = self._output_location(location)
            self._ui.comboBoxOutputDirectory.addItem(display_location)
            self._ui.comboBoxOutputDirectory.setCurrentIndex(self._ui.comboBoxOutputDirectory.count() - 1)
            self._directory_valid()

    def _output_location(self, location=None):
        if location is None:
            display_path = self._ui.comboBoxOutputDirectory.currentText()
        else:
            display_path = location

        if self._workflow_location and os.path.isabs(display_path):
            display_path = os.path.relpath(display_path, self._workflow_location)

        return display_path

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.StandardButton.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(
                self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QDialog.accept(self)

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEdit0.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEdit0.text())
        if valid:
            self._ui.lineEdit0.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit0.setStyleSheet(INVALID_STYLE_SHEET)

        return valid and self._directory_valid()

    def _output_location_abspath(self):
        dir_path = self._output_location()

        if self._workflow_location:
            dir_path = os.path.realpath(os.path.join(self._workflow_location, dir_path))

        return dir_path

    def _directory_valid(self):
        self._ui.comboBoxOutputDirectory.setItemText(0, self._local_output_directory())
        dir_path = self._output_location_abspath()

        output_directory_exists = os.path.isdir(dir_path)
        if (self._ui.comboBoxOutputDirectory.currentIndex() == 0 or self._ui.comboBoxOutputDirectory.currentIndex() == 1) and not output_directory_exists:
            os.mkdir(dir_path)

        directory_valid = os.path.isdir(dir_path) and len(self._ui.comboBoxOutputDirectory.currentText())
        self._ui.comboBoxOutputDirectory.setStyleSheet(DEFAULT_STYLE_SHEET if directory_valid else INVALID_STYLE_SHEET)

        return directory_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = self._ui.lineEdit0.text()
        output_directories = []
        for i in range(2, self._ui.comboBoxOutputDirectory.count()):
            output_directories.append(self._ui.comboBoxOutputDirectory.itemText(i))
        config = {
            'identifier': self._ui.lineEdit0.text(),
            'output-directory-index': self._ui.comboBoxOutputDirectory.currentIndex(),
            'output-directories': output_directories,
        }
        if self._previous_location:
            config['previous-location'] = os.path.relpath(self._previous_location, self._workflow_location)
        else:
            config['previous-location'] = ''

        return config

    def _local_output_directory(self):
        return f'{self._ui.lineEdit0.text()}-downloads'

    def get_output_directory(self):
        return self._output_location_abspath()

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._ui.lineEdit0.setText(config['identifier'])
        self._ui.comboBoxOutputDirectory.addItem(self._local_output_directory())
        self._ui.comboBoxOutputDirectory.addItem(_global_output_directory())
        for output_directory in config.get('output-directories', []):
            self._ui.comboBoxOutputDirectory.addItem(output_directory)

        self._ui.comboBoxOutputDirectory.setCurrentIndex(config.get('output-directory-index', 0))

        if 'previous-location' in config:
            self._previous_location = os.path.join(self._workflow_location, config['previous-location'])

