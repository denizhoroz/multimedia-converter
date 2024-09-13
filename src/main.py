import sys
import os
import threading
import time
from PySide6 import QtCore, QtWidgets, QtGui
import converter

def runtime(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            time_took = end_time - start_time
            return time_took, res
        return wrapper

class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.setWindowTitle('Multimedia Converter')
        self.setFixedSize(900, 500)

        # Load stylesheet
        self.load_stylesheet()

        # Initialize widgets
        self.initialize_ui()

        # Variables
        self.convertion_queue = []
        self.filetype = None
        self.dst_path = None
        self.filetypes = {
            'photos': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.raw', '.heif', '.heic', '.psd', '.svg', '.ico', '.ai', '.eps'],
            'audios': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff', '.alac'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp'],
        }

    def load_stylesheet(self):
        with open('./src/style.qss', 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def initialize_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        group_layout = QtWidgets.QHBoxLayout()

        plain_spacer1 = QtWidgets.QSpacerItem(1, 50, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        plain_spacer2 = QtWidgets.QSpacerItem(1, 150, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        plain_spacer3 = QtWidgets.QSpacerItem(1, 250, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # Top Header
        header = QtWidgets.QLabel('Multimedia Converter', self)
        header.setObjectName('header')
        header.setFixedHeight(60)

        # Create Groups frame
        frame_groups = QtWidgets.QFrame()
        frame_groups.setFrameShape(QtWidgets.QFrame.Box)

        ## === Groupbox Select files Area === ##
        group_select = QtWidgets.QGroupBox("Select Files")
        group_select_layout = QtWidgets.QGridLayout()

        self.list_convert_queue = QtWidgets.QListWidget()

        button_select_files = QtWidgets.QPushButton("Select files")
        button_select_files.setFixedWidth(180)
        button_select_files.clicked.connect(self.load_file)

        button_clear = QtWidgets.QPushButton("Clear")
        button_clear.setFixedWidth(50)
        button_clear.clicked.connect(self.clear_queue)

        # Destination folder frame
        frame_dst = QtWidgets.QFrame()
        frame_dst.setFrameShape(QtWidgets.QFrame.Box)
        frame_dst_layout = QtWidgets.QGridLayout()
        
        label_dst = QtWidgets.QLabel('Destination folder')

        button_change_dst = QtWidgets.QPushButton("📁")
        button_change_dst.setFixedWidth(25)
        button_change_dst.clicked.connect(self.select_dest)

        self.label_dst_path = QtWidgets.QLabel('destination/folder')
        self.label_dst_path.setObjectName('destination-folder')

        frame_dst_layout.addWidget(label_dst,                    0, 0, 1, 2)
        frame_dst_layout.addWidget(button_change_dst,            1, 0)
        frame_dst_layout.addWidget(self.label_dst_path,          1, 1)
        frame_dst.setLayout(frame_dst_layout)
        ###

        group_select_layout.addWidget(self.list_convert_queue,   0, 0, 1, 2)
        group_select_layout.addWidget(button_select_files,       1, 0,)
        group_select_layout.addWidget(button_clear,              1, 1,)
        group_select_layout.addItem(plain_spacer1,               2, 0, 1, 2)
        group_select_layout.addWidget(frame_dst,                 3, 0, 1, 2)
        group_select.setLayout(group_select_layout)

        ## === Groupbox Conversion options Area === ##
        group_options = QtWidgets.QGroupBox("Conversion Options")
        group_options_layout = QtWidgets.QGridLayout()

        label_type = QtWidgets.QLabel("Select media type")

        self.option_photos = QtWidgets.QRadioButton("Photos")
        self.option_audios = QtWidgets.QRadioButton("Audios")
        self.option_videos = QtWidgets.QRadioButton("Videos")
        self.option_photos.toggled.connect(self.set_filetype)
        self.option_audios.toggled.connect(self.set_filetype)
        self.option_videos.toggled.connect(self.set_filetype)

        label_file = QtWidgets.QLabel("Select file type to convert")

        self.dst_type = QtWidgets.QComboBox()
        
        group_options_layout.addWidget(label_type,               0, 0, 1, 3)
        group_options_layout.addWidget(self.option_photos,       1, 0,)
        group_options_layout.addWidget(self.option_audios,       1, 1,)
        group_options_layout.addWidget(self.option_videos,       1, 2,)
        group_options_layout.addItem(plain_spacer1,              2, 0, 1, 3)
        group_options_layout.addWidget(label_file,               3, 0, 1, 3)
        group_options_layout.addWidget(self.dst_type,            4, 0,)
        group_options_layout.addItem(plain_spacer2,              5, 0, 1, 3)
        group_options.setLayout(group_options_layout)

        ## === Groupbox Convert Area === ##
        group_convert = QtWidgets.QGroupBox("Convert")
        group_convert_layout = QtWidgets.QGridLayout()
        
        button_convert = QtWidgets.QPushButton("Convert")
        button_convert.clicked.connect(self.convert_button_clicked)

        self.enable_threading = QtWidgets.QCheckBox("Enable Multithreading")

        self.time_feed = QtWidgets.QLabel("")

        group_convert_layout.addWidget(button_convert,          0, 0,)
        group_convert_layout.addWidget(self.enable_threading,   1, 0,)
        group_convert_layout.addWidget(self.time_feed,          2, 0,)
        group_convert_layout.addItem(plain_spacer3,             3, 0,)
        group_convert.setLayout(group_convert_layout)

        # Apply group layout
        group_layout.addWidget(group_select)
        group_layout.addWidget(group_options)
        group_layout.addWidget(group_convert)

        frame_groups.setLayout(group_layout)

        # Apply main layout
        main_layout.addWidget(header)
        main_layout.addWidget(frame_groups)
        self.setLayout(main_layout)
    
    def load_file(self):
        # Select files
        file_path, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 
                                                              "Select File", 
                                                              "", 
                                                              "All Files (*)",)

        # Filter and load files
        for file in file_path:
            if file not in self.convertion_queue:
                self.convertion_queue.append(file)
        
        # Display files on the list
        self.list_convert_queue.clear()
        for file in self.convertion_queue:
            item = os.path.basename(file)
            self.list_convert_queue.addItem(item)

        # Update default dst
        if len(self.convertion_queue) > 0:
            self.dst_path = os.path.dirname(self.convertion_queue[0])
            self.label_dst_path.setText(self.dst_path)

            # Update initial filetype selection
            filetype_bias = os.path.splitext(self.convertion_queue[0])[1]
            if filetype_bias in self.filetypes['photos']:
                self.filetype = 'photos'
                self.update_filetypes()
                self.option_photos.setChecked(True)
            elif filetype_bias in self.filetypes['audios']:
                self.filetype = 'audios'
                self.update_filetypes()
                self.option_audios.setChecked(True)
            elif filetype_bias in self.filetypes['videos']:
                self.filetype = 'videos'
                self.update_filetypes()
                self.option_videos.setChecked(True)
            else:
                self.raise_warning(error='typeNotFound')

    def select_dest(self):
        # Set default dst
        if len(self.convertion_queue) > 0:
            self.dst_path = os.path.dirname(self.convertion_queue[0])

        # Select folder
        self.dst_path = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                                 "Select Destination Folder", 
                                                                 "", 
                                                                 QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.DontUseNativeDialog,)
        
        # Display folder on label
        self.label_dst_path.setText(self.dst_path)
  
    def set_filetype(self):
        if self.option_photos.isChecked():
            self.filetype = 'photos'
        elif self.option_audios.isChecked():
            self.filetype = 'audios'
        elif self.option_videos.isChecked():
            self.filetype = 'videos'
        else:
            self.filetype = None

        # Update comboboxes
        self.update_filetypes()

    def update_filetypes(self):
        filetype_options = []

        self.dst_type.clear()
        filetype_options = self.filetypes[self.filetype]
        
        for option in filetype_options:
            self.dst_type.addItem(option)
    
    def convert_button_clicked(self):
        execution_time, res = self.convert_files()
        
        if res == 'complete':
            self.time_feed.setText("Took {:.2f} seconds".format(execution_time))
        elif res == 'error':
            self.time_feed.setText("")


    @runtime
    def convert_files(self):
        if len(self.convertion_queue) > 0: 
            if self.dst_path != '':
                if self.filetype in ['photos', 'audios', 'videos']:
                    if self.enable_threading.isChecked():
                        self.process_threading()
                    else:
                        for file in self.convertion_queue:
                            self.process(file=file)
                    return 'complete'
                else:
                    self.raise_warning(error='noFileType')
                    return 'error'
            else:
                self.raise_warning(error='noDstPath')
                return 'error'
        else:
            self.raise_warning(error='emptyQueue')
            return 'error'
            
    def process_threading(self):
        threads = []
        
        # Create and start threads for every processing task
        for file in self.convertion_queue:
            print(type(file))
            thread = threading.Thread(target=self.process, args=(file,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def process(self, file):
        converter.convert(file, self.dst_path, self.dst_type.currentText())

    def clear_queue(self):
        self.convertion_queue.clear()
        self.list_convert_queue.clear()
        self.dst_path = None
        self.label_dst_path.setText('destination/folder')

    def raise_warning(self, error):
        warningbox = QtWidgets.QMessageBox()
        warningbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        warningbox.setWindowTitle('Warning')
        
        if error == 'emptyQueue':
            warningbox.setText('No files in the queue')
        elif error == 'noDstPath':
            warningbox.setText('No destination folder found')
        elif error == 'noFileType':
            warningbox.setText('No file type is selected')
        elif error == 'typeNotFound':
            warningbox.setText('Incorrect file type')
            self.clear_queue()
        else:
            pass

        warningbox.exec()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    interface = Interface()
    interface.show()

    sys.exit(app.exec())