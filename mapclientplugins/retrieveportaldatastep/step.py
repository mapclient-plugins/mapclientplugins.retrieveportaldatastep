
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
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

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
            'identifier': '', 'outputDir': ''
        }

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        try:
            output_dir = self._config['outputDir'] if os.path.isabs(self._config['outputDir']) else os.path.join(
                self._location, self._config['outputDir'])
            output_dir = os.path.realpath(output_dir)
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)

            self._view = RetrievePortalDataWidget(output_dir)
            self._view.registerDoneExecution(self._doneExecution)
            self._setCurrentWidget(self._view)
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.

        :param index: Index of the port to return.
        """
        # http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location
        return self._view.get_output_files()

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.setWorkflowLocation(self._location)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
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

        d = ConfigureDialog()
        d.setWorkflowLocation(self._location)
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


