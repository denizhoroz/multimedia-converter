import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui

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
        button_select_files.clicked.connect(self.load_file)

        label_dst = QtWidgets.QLabel('Destination folder')

        button_change_dst = QtWidgets.QPushButton("📁")
        button_change_dst.setFixedWidth(25)
        button_change_dst.clicked.connect(self.select_dest)

        self.label_dst_path = QtWidgets.QLabel('destination/folder')
        self.label_dst_path.setObjectName('destination-folder')

        group_select_layout.addWidget(self.list_convert_queue,   0, 0, 1, 2)
        group_select_layout.addWidget(button_select_files,       1, 0, 1, 2)
        group_select_layout.addItem(plain_spacer1,               2, 0, 1, 2)
        group_select_layout.addWidget(label_dst,                 3, 0, 1, 2)
        group_select_layout.addWidget(button_change_dst,         4, 0,)
        group_select_layout.addWidget(self.label_dst_path,       4, 1,)

        group_select.setLayout(group_select_layout)

        ## === Groupbox Conversion options Area === ##
        group_options = QtWidgets.QGroupBox("Conversion Options")
        group_options_layout = QtWidgets.QGridLayout()

        label_type = QtWidgets.QLabel("Select media type")

        option_photos = QtWidgets.QRadioButton("Photos")
        option_audios = QtWidgets.QRadioButton("Audios")
        option_videos = QtWidgets.QRadioButton("Videos")

        label_file = QtWidgets.QLabel("Select file types")

        src_type = QtWidgets.QComboBox()
        label_between = QtWidgets.QLabel("     to")
        dst_type = QtWidgets.QComboBox()
        
        group_options_layout.addWidget(label_type,          0, 0, 1, 3)
        group_options_layout.addWidget(option_photos,       1, 0,)
        group_options_layout.addWidget(option_audios,       1, 1,)
        group_options_layout.addWidget(option_videos,       1, 2,)
        group_options_layout.addItem(plain_spacer1,         2, 0, 1, 3)
        group_options_layout.addWidget(label_file,          3, 0, 1, 3)
        group_options_layout.addWidget(src_type,            4, 0,)
        group_options_layout.addWidget(label_between,       4, 1,)
        group_options_layout.addWidget(dst_type,            4, 2,)
        group_options_layout.addItem(plain_spacer2,         5, 0, 1, 3)

        group_options.setLayout(group_options_layout)

        ## === Groupbox Convert Area === ##
        group_convert = QtWidgets.QGroupBox("Convert")
        group_convert_layout = QtWidgets.QGridLayout()
        
        button_convert = QtWidgets.QPushButton("Convert")
        progress_convert = QtWidgets.QProgressBar()

        group_convert_layout.addWidget(button_convert,      0, 0,)
        group_convert_layout.addWidget(progress_convert,    1, 0,)
        group_convert_layout.addItem(plain_spacer3,         2, 0,)

        group_convert.setLayout(group_convert_layout)

        # Apply group layout
        group_layout.addWidget(group_select)
        group_layout.addWidget(group_options)
        group_layout.addWidget(group_convert)

        frame_groups.setLayout(group_layout)

        # Apply main layout
        main_layout.addWidget(header)
        main_layout.addWidget(frame_groups)
        #main_layout.addWidget(footer)

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
        for file in self.convertion_queue:
            item = os.path.basename(file)
            self.list_convert_queue.addItem(item)

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

        
    def something(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    interface = Interface()
    interface.show()

    sys.exit(app.exec())