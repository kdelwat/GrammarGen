import sys
import math
import time

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pypandoc

import generate

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

        # Clear progress bar
        self.clear_progress(stages=4)

        # Connect inputs to handlers
        self.markdown_path_select.clicked.connect(self.select_markdown_file)
        self.output_path_select.clicked.connect(self.select_output_file)
        self.generate_button.clicked.connect(self.generate)

    def clear_progress(self, stages):
        '''Set the progress bar to 0. Calculate the number of intervals needed
        based on the number of generation stages and add the correct increment to
        a variable.
        '''
        self.progress = 0
        self.generate_progress.setValue(self.progress)

        self.increment = math.ceil(100 / stages)

    def update_progress(self, message):
        '''Increment the progress bar one step, displaying the given status
        message.'''
        self.progress += self.increment
        self.generate_progress.setValue(self.progress)
        self.status_bar.showMessage(message)

    def select_markdown_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file')
        self.markdown_path_input.setText(filename[0])

    def select_output_file(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Create file')
        self.output_path_input.setText(filename[0])

    def generate(self):
        '''Generate the HTML file.'''
        self.update_progress('Loading Markdown...')
        time.sleep(1)
        self.update_progress('Generating HTML...')
        time.sleep(1)
        self.update_progress('Styling output...')
        time.sleep(1)
        self.update_progress('Saving HTML...')
        time.sleep(1)
        self.clear_progress(4)

        markdown_filename = self.markdown_path_input.text()
        output_filename = self.output_path_input.text()

        theme = self.theme_choice.currentText()

        try:
            with open(markdown_filename, 'r') as f:
                input_text = f.read()
                print(input_text)
        except FileNotFoundError:
            self.status_bar.showMessage('ERROR: Markdown file not found!')
            return False

        output_text = generate.generate(input_text, theme)

        with open(output_filename, 'w') as f:
            f.write(output_text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GrammarGenApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
