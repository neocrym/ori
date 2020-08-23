"""Unit test module for :mod:`ori.subprocess`."""
import os
import tempfile
import unittest
import uuid

import ori.subprocess


class LogToFile:
    """Create a function that continually appends to a file."""

    def __init__(self, filename: str):
        self.filename = filename

    def __call__(self, message: str):
        with open(self.filename, "a") as handle:
            return handle.write(message)


class TestSubprocess(unittest.TestCase):
    """Unit tests for ori.subprocess."""

    def test__run_process_in_background__stdout(self):
        """Test that we can run a command in the background while logging stdout."""
        temp_dir = tempfile.TemporaryDirectory()
        temp_filename = os.path.join(temp_dir.name, str(uuid.uuid4()) + ".txt")
        log_to_file = LogToFile(temp_filename)
        if os.name == "nt":
            command = "dir"
        else:
            command = "ls"
        process = ori.subprocess.run_process_in_background(
            command=[command, __file__], stdout_function=log_to_file,
        )
        process.join()
        with open(temp_filename, "r") as fh:
            output = fh.read()
        temp_dir.cleanup()
        assert "test_subprocess.py" in output
