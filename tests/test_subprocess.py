import contextlib
import os
import tempfile
import unittest
import uuid

import ori.subprocess


@contextlib.contextmanager
def get_temporary_filename():
    """Context manager to open a temporary file in the current directory and delete it afterwards.

    This returns the filename as a string. The user has to reopen it to get a
    file handle.

    This is needed because temporary files created with Python's
    `tempfile.NamedTemporaryFile` cannot be reopened under Windows NT or later.
    """
    filename = str(uuid.uuid4()) + ".txt"
    open(filename, "w").close()
    try:
        yield filename
    finally:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass


def create_file_logger(filename):
    def printer(value):
        with open(filename, "a") as fh:
            return fh.write(value)

    return printer


class TestSubprocess(unittest.TestCase):
    def test__run_process_in_background__stdout(self):
        with get_temporary_filename() as log_filename:
            logger = create_file_logger(log_filename)
            if os.name == "nt":
                command = "dir"
            else:
                command = "ls"
            process = ori.subprocess.run_process_in_background(
                command=[command, log_filename], stdout_function=logger,
            )
            process.join()
            with open(log_filename, "r") as fh:
                output = fh.read()
            assert log_filename in output
