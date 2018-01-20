"""
Project wrapper
"""

import os

PROJ_EMPTY_PATH = 'emptypath'
PROJ_EMPTY_DIR = 'emptydir'
PROJ_VALID = 'valid'

class Project():
    """Class that wraps everything todo with each lab"""
    def __init__(self):
        self.rootdir = ''

    def new_project(self, rootdir):
        """Validates the directory"""
        if rootdir == '':
            return 'emptypath'

        self.rootdir = rootdir

        if not os.listdir(self.rootdir):
            return 'emptydir'

        return 'valid'

    def get_submissions(self):
        """Returns a list of file names of submissions"""
        submissions = []
        for submission in os.listdir(self.rootdir):
            fname, fext = os.path.splitext(submission)
            if fname not in submissions:
                submissions.append(fname)

            # Correct the extensions
            if fext == '.cpp':
                new_filename = self.rootdir + '/' + submission
                new_filename = new_filename.replace('/', '\\')
                old_filename = new_filename
                new_filename = new_filename.replace('.cpp', '.c')
                os.rename(old_filename, new_filename)

        return submissions

    def get_submission_code(self, item):
        """Returns the written code of the submission"""
        source_filename = self.rootdir + '/' + item + '.c'
        code = ''
        try:
            source = open(source_filename, 'r')
            code = source.read()
            source.close()
        except Exception as file_io_exception:
            print(file_io_exception)

        return code

