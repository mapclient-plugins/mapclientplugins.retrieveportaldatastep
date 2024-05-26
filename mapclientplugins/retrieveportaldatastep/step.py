
"""
MAP Client Plugin Step
"""
import json
import os
import pathlib

from PySide6 import QtGui, QtWidgets, QtCore

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.retrieveportaldatastep.configuredialog import ConfigureDialog
from mapclientplugins.retrieveportaldatastep.retrieveportaldatawidget import RetrievePortalDataWidget


class RetrievePortalDataStep(WorkflowStepMountPoint):

    def __init__(self, location):
        super(RetrievePortalDataStep, self).__init__('Retrieve Portal Data', location)
        self._view = None
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Source'
        self._location = location
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/retrieveportaldatastep/images/data-source.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides-list-of',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        # Port data:
        self._portData0 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location
        # Config:
        self._config = {
            'identifier': '', 'output-directories': [], 'output-directory-index': 0,
        }

    def _setup_configure_dialog(self, parent=None):
        d = ConfigureDialog(parent)
        d.setWorkflowLocation(self._location)
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        return d

    def _determine_output_dir(self):
        d = self._setup_configure_dialog()
        return d.get_output_directory()

    def _settings_filename(self):
        return os.path.join(self._location, f"{self._config['identifier']}-settings.json")

    def _get_output_files(self):
        if not os.path.isfile(self._settings_filename()):
            with open(self._settings_filename(), "w") as fh:
                json.dump({}, fh)

        with open(self._settings_filename()) as fh:
            settings = json.load(fh)

        return [f for f in settings.get("output-files", []) if os.path.isfile(os.path.join(self._determine_output_dir(), f))]

    def _set_output_files(self, output_files):
        with open(self._settings_filename()) as fh:
            settings = json.load(fh)

        settings['output-files'] = [pathlib.PureWindowsPath(f).as_posix() for f in output_files]

        with open(self._settings_filename(), "w") as fh:
            json.dump(settings, fh)

    def execute(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        try:
            output_dir = self._determine_output_dir()
            output_files = self._get_output_files()
            self._view = RetrievePortalDataWidget(output_dir, output_files)
            self._view.register_done_execution(self._done_execution)
            self._setCurrentWidget(self._view)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def _done_execution(self):
        output_files = self._view.get_output_files()
        self._set_output_files(output_files)
        self._doneExecution()

    def getPortData(self, index):
        output_files = self._view.get_output_files()
        output_dir = self._determine_output_dir()
        return [os.path.join(output_dir, f) for f in output_files]

    def configure(self):
        dlg = self._setup_configure_dialog(self._main_window)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.

        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = self._setup_configure_dialog()
        self._configured = d.validate()

    def getAdditionalConfigFiles(self):
        return [self._settings_filename()]
