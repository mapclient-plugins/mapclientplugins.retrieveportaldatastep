import os

from PySide6 import QtWidgets
from mapclientplugins.retrieveportaldatastep.ui_configuredialog import Ui_ConfigureDialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


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
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._workflow_location = None
        self._previousLocation = ''

        self._makeConnections()

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def _makeConnections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
        self._ui.pushButtonOutputDirectory.clicked.connect(self._directory_chooser_clicked)

    def _directory_chooser_clicked(self):
        # Second parameter returned is the filter chosen
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination for export', self._previousLocation)

        if location:
            self._previousLocation = location
            display_location = self._output_location(location)
            self._ui.lineEditOutputDirectory.setText(display_location)
            self._directory_valid()

    def _output_location(self, location=None):
        if location is None:
            display_path = self._ui.lineEditOutputDirectory.text()
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

        return valid

    def _directory_valid(self):
        dir_path = self._output_location()

        if self._workflow_location:
            dir_path = os.path.realpath(os.path.join(self._workflow_location, dir_path))

        directory_valid = os.path.isdir(dir_path) and len(self._ui.lineEditOutputDirectory.text())
        self._ui.lineEditOutputDirectory.setStyleSheet(DEFAULT_STYLE_SHEET if directory_valid else INVALID_STYLE_SHEET)

        return directory_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = self._ui.lineEdit0.text()
        config = {}
        config['identifier'] = self._ui.lineEdit0.text()
        config['outputDir'] = self._output_location()
        if self._previousLocation:
            config['previous_location'] = os.path.relpath(self._previousLocation, self._workflow_location)
        else:
            config['previous_location'] = ''

        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._ui.lineEdit0.setText(config['identifier'])
        if 'outputDir' in config:
            self._ui.lineEditOutputDirectory.setText(config['outputDir'])
        if 'previous_location' in config:
            self._previousLocation = os.path.join(self._workflow_location, config['previous_location'])

