import os.path

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Slot, Qt, QTimer


class DownloadProgressDialog(QDialog):

    def __init__(self, total_files, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Downloading Files")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(400, 100)

        self.total_files = total_files
        self._individual_progress = [0] * self.total_files
        self._seen_file = {}
        self._errors = 0

        layout = QVBoxLayout(self)
        self._label = QLabel("Starting downloads...", self)
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setMaximum(total_files)
        self._progress_bar.setValue(0)

        layout.addWidget(self._label)
        layout.addWidget(self._progress_bar)

    def _update_progress_bar(self):
        self._progress_bar.setValue(sum(self._individual_progress))

    def _register_file_path(self, file_path):
        if file_path not in self._seen_file:
            file_index = len(self._seen_file)
            self._seen_file[file_path] = file_index

    @Slot(str, float)
    def on_file_progress(self, file_path, progress):
        self._register_file_path(file_path)
        self._individual_progress[self._seen_file[file_path]] = progress
        self._update_progress_bar()

    @Slot(str)
    def on_file_downloaded(self, file_path):
        self._register_file_path(file_path)
        self._individual_progress[self._seen_file[file_path]] = 1
        self._update_progress_bar()

        self._label.setText(f"Downloaded: {os.path.basename(file_path)}")
        if file_path == "error":
            self._errors += 1

        if sum(self._individual_progress) >= self.total_files:
            label_text = "All downloads complete."
            dialog_close_delay = 500
            if self._errors > 0:
                label_text = f"({self._errors} file{'s' if self._errors > 1 else ''} failed to download)"
                dialog_close_delay = 1500
            self._label.setText(label_text)
            QTimer.singleShot(dialog_close_delay, self.accept)
