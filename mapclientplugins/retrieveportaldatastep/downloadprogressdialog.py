import os.path

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Signal, Slot, Qt, QTimer


class DownloadProgressDialog(QDialog):
    update_progress = Signal(str)

    def __init__(self, total_files, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Downloading Files")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(400, 100)

        self.total_files = total_files
        self.completed = 0

        layout = QVBoxLayout(self)
        self.label = QLabel("Starting downloads...", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

        self.update_progress.connect(self.on_file_downloaded)

    @Slot(str)
    def on_file_downloaded(self, file_path):
        self.completed += 1
        self.progress_bar.setValue(self.completed)
        self.label.setText(f"Downloaded: {os.path.basename(file_path)}")

        if self.completed >= self.total_files:
            self.label.setText("All downloads complete.")
            QTimer.singleShot(500, self.accept)
