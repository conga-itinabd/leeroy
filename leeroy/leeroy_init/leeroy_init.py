import os
import shutil


def leeroy_init(main_arg):

    def cp_file(file):
        file_directory = os.path.dirname(__file__)
        current_directory = os.getcwd()

        file_path = os.path.join(file_directory, file)
        current_directory_file = os.path.join(current_directory, file)

        shutil.copyfile(file_path, current_directory_file)

    if main_arg == 'init':
        stepsbook = 'stepsbook.yaml'
        values = 'values.yaml'
    elif main_arg == 'init-doc':
        stepsbook = 'doc_stepsbook.yaml'
        values = 'doc_values.yaml'
    elif main_arg == 'init-future':
        stepsbook = 'future_stepsbook.yaml'
        values = 'future_values.yaml'

    cp_file(stepsbook)
    cp_file(values)
