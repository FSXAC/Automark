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

    def get_submission_info(self):
        """Returns details about the submission"""
        

    def get_submission_note(self):
        """Returns the note / info.txt of the submission"""
        note_filename = self.rootdir + '/' + self.current_id + '.txt'
        info = 'This submission did not have info.txt'
        try:
            note = open(note_filename, 'r')
            info = note.read()
            note.close()
        except Exception as file_io_exception:
            print('[Project]', file_io_exception)

        return info

    def clean_dir(self):
        """Deletes all the binaries in the active directory"""
        try:
            for file in os.listdir(self.rootdir):
                if file.endswith('.exe'):
                    os.remove(os.path.join(self.rootdir, file))
        except Exception as delete_exception:
            print('[Project]', delete_exception)


    def compile_and_run(self):
        """Try to compile the current file"""
        try:
            source = (self.rootdir + '/' + self.current_id + '.c').replace('/', '\\')
            out = (self.rootdir + '/' + self.current_id + '.exe').replace('/', '\\')

            # Call compiler
            process = subprocess.Popen(
                ['gcc', source, '-w', '-o', out],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, err = process.communicate()

            if err == b'':
                subprocess.call('start ' + out, shell=True)
            else:
                # This is when there's a compilation error
                return err.decode("utf-8")

        except Exception as compile_exception:
            print('[Project]', compile_exception)

        return ''

    def compile_all(self):
        """Compiles all the C files in the directory"""
        # Clean the directory first
        self.clean_dir()

        # Compile all
        try:
            for submission in os.listdir(self.rootdir):
                fname, fext = os.path.splitext(submission)
                if fext == '.c':
                    source = (self.rootdir + '/' + fname + '.c').replace('/', '\\')
                    out = source.replace('.c', '.exe')

                    # Call compiler
                    process = subprocess.Popen(['gcc', source, '-w', '-o', out], shell=True)
                    process.communicate()
        except Exception as compile_exception:
            print('[Project]', compile_exception)

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

    def get_current_submission_id(self):
        """Returns CSID"""
        return self.current_id
