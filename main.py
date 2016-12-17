import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pypandoc

# Initialise GUI layout from Qt Designer file
main_window, qt_base_class = uic.loadUiType('app.ui')


def ensure_pandoc_exists():
    '''Check the current Pandoc version. If it isn't installed, download it using
    pypandoc.
    '''
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.pypandoc.pandoc_download()


class GrammarGenApp(QtWidgets.QMainWindow, main_window):
    '''The main application class.'''
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        main_window.__init__(self)
        self.setupUi(self)

        # Connect inputs to handlers
        self.markdown_path_select.clicked.connect(self.select_markdown_file)
        self.output_path_select.clicked.connect(self.select_output_file)
        self.generate_button.clicked.connect(self.generate)

    def select_markdown_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file')
        self.markdown_path_input.setText(filename[0])

    def select_output_file(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Create file')
        self.output_path_input.setText(filename[0])

    def generate(self):
        '''Generate the HTML file.'''
        markdown_filename = self.markdown_path_input.text()
        output_filename = self.output_path_input.text()

        try:
            with open(markdown_filename, 'r') as f:
                input_text = f.read()
                print(input_text)
        except FileNotFoundError:
            pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GrammarGenApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
