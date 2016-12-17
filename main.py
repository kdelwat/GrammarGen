import sys
import math
import time
import csv

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pypandoc

import generate

# Initialise GUI layout from Qt Designer file
main_window, qt_base_class = uic.loadUiType('app.ui')


class GrammarGenApp(QtWidgets.QMainWindow, main_window):
    '''The main application class.'''
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        main_window.__init__(self)
        self.setupUi(self)

        self.check_pandoc_on_startup()

        self.clear_progress(stages=4)

        # Connect inputs to handlers
        self.markdown_path_select.clicked.connect(self.select_markdown_file)
        self.lexicon_path_select.clicked.connect(self.select_lexicon_file)
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

    def select_lexicon_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file')
        self.lexicon_path_input.setText(filename[0])

    def select_output_file(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Create file')
        self.output_path_input.setText(filename[0])

    def generate(self):
        '''Generate the HTML file.'''
        self.update_progress('Loading Markdown...')

        markdown_filename = self.markdown_path_input.text()
        try:
            with open(markdown_filename, 'r') as f:
                input_text = f.read()
                print(input_text)
        except FileNotFoundError:
            self.status_bar.showMessage('ERROR: Markdown file not found!')
            return False

        self.update_progress('Generating HTML...')

        theme = self.theme_choice.currentText()
        output_text = generate.generate(input_text, theme)

        self.update_progress('Loading definitions...')
        lexicon_filename = self.lexicon_path_input.text()
        with open(lexicon_filename, 'r') as f:
            csv_reader = csv.reader(f)
            lexicon = [line for line in csv_reader]

        output_text = generate.load_words_from_lexicon(output_text, lexicon)

        self.update_progress('Saving HTML...')

        output_filename = self.output_path_input.text()
        with open(output_filename, 'w') as f:
            f.write(output_text)

        self.clear_progress(4)
        self.status_bar.showMessage('Successfully generated HTML')

    def check_pandoc_on_startup(self):
        '''On startup, checks if pandoc is installed. If it is, continues to main
        application. Otherwise, prompts the user to install.'''
        try:
            version = pypandoc.get_pandoc_version()
            self.status_bar.showMessage('Found pandoc version {0}'.format(version))

        except OSError:
            error_string = '''GrammarGen could not find a local installation of Pandoc.
If you have already installed it, check that it is in your PATH.
Otherwise, GrammarGen can install it automatically. Proceed with installation?'''

            download_prompt = QtWidgets.QMessageBox.question(self,
                                                             'Pandoc not found',
                                                             error_string,
                                                             QtWidgets.QMessageBox.Yes |
                                                             QtWidgets.QMessageBox.No,
                                                             QtWidgets.QMessageBox.No)

            if download_prompt == QtWidgets.QMessageBox.Yes:
                pypandoc.pandoc_download.download_pandoc()
            else:
                sys.exit(0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GrammarGenApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
