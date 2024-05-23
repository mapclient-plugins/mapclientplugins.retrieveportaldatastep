
"""
MAP Client Plugin Step
"""
import json
import os

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
            'identifier': '', 'output-directories': [], 'output-directory-index': 0
        }

    def _setup_configure_dialog(self, parent=None):
        d = ConfigureDialog(parent)
        d.setWorkflowLocation(self._location)
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        return d

    def _determine_ouptut_dir(self):
        d = self._setup_configure_dialog()
        return d.get_output_directory()

    def execute(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        try:
            output_dir = self._determine_ouptut_dir()
            self._view = RetrievePortalDataWidget(output_dir)
            self._view.register_done_execution(self._doneExecution)
            self._setCurrentWidget(self._view)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def getPortData(self, index):
        return self._view.get_output_files()

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


