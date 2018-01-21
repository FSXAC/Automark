"""
Project wrapper
"""

import os
import subprocess
import json

PROJ_EMPTY_PATH = 'emptypath'
PROJ_EMPTY_DIR = 'emptydir'
PROJ_VALID = 'valid'

class Project():
    """Class that wraps everything todo with each lab"""
    def __init__(self):
        self.rootdir = ''
        self.current_id = ''
        self.rubric_file = ''
        self.rubric = {}

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

    def set_submission(self, item):
        self.current_id = item

    def get_submission_code(self):
        """Returns the written code of the submission"""
        source_filename = self.rootdir + '/' + self.current_id + '.c'
        code = ''
        try:
            source = open(source_filename, 'r')
            code = source.read()
            source.close()
        except Exception as file_io_exception:
            print(file_io_exception)

        return code

    def get_submission_note(self):
        """Returns the note / info.txt of the submission"""
        note_filename = self.rootdir + '/' + self.current_id + '.txt'
        info = 'This submission did not have info.txt'
        try:
            note = open(note_filename, 'r')
            info = note.read()
            note.close()
        except Exception as file_io_exception:
            print(file_io_exception)

        return info

    def compile_and_run(self):
        """Try to compile the current file"""
        try:
            source = (self.rootdir + '/' + self.current_id + '.c').replace('/', '\\')
            out = (self.rootdir + '/' + self.current_id + '.exe').replace('/', '\\')
            command = 'gcc ' + source + ' -o ' + out
            subprocess.run(command)
            subprocess.call('start ' + out, shell=True)

            # Delete the exe file
            os.remove(out)
        except Exception as compile_exception:
            print(compile_exception)

    def load_rubric(self, fname):
        """Assign the rubric structure"""
        try:
            rubric_file = open(fname, 'r')
            rubric = rubric_file.read()
            rubric_file.close()
        except Exception as file_io_exception:
            print(file_io_exception)

        self.rubric = json.loads(rubric)

    def get_parsed_rubric(self):
        """Returns the JSON parsed rubric"""
        return self.rubric