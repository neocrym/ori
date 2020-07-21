"""Utility function for running external commands as subprocesses."""
import multiprocessing
import selectors
import signal
import subprocess
import sys
import typing


def _null_function(*args, **kwargs):  # pylint: disable=unused-argument
    """A function that does nothing.

    This function is used to replace printing or logging functions
    when they are not specified.
    """


def run_process_in_background(
    *,
    command: typing.Iterable[str],
    stdout_function: typing.Optional[typing.Callable] = None,
    stderr_function: typing.Optional[typing.Callable] = None,
    exception_function: typing.Optional[typing.Callable] = None,
    exit_code_on_killed: int = 0,
):
    """
    Runs `command`, writing stdout and stderr to the logger in `logger`.

    This function is based on `this answer on StackOverflow <https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order/56918582#56918582>`_.

    Args:
        command: This is an iterable--like a list--of strings. This iterable
            describes a command line program to run. For example, the
            command `ls -l /home` would be broken up into
            `["ls", "-l", "/home"]`. You can use the function
            :func:`shlex.split` to turn any string command into an iterable.
        stdout_function: This is a function that your subprocess will call for
            every line of standard output that your program emits.
            You can choose functions like :func:`print` or, say,
            :func:`logging.debug`.
        stderr_function: This is a function that your subprocess will call
            for every line of standard error that your program emits.
            The same rules apply as for `stdout_function`.
        exception_function: This is a function to call if we catch an exception
            while logging the program.
        exit_code_on_killed: This is the exit code we return for the subprocess
            when we catch an exception while logging the program.

    Returns:
        This returns an already-started :class:`multiprocessing.Process` instance,
        which you can use to monitor or kill the process as time goes on.
    """

    if not stdout_function:
        stdout_function = _null_function
    if not stderr_function:
        stderr_function = _null_function
    if not exception_function:
        exception_function = _null_function

    def target():
        """Manage the actual command we're running."""
        command_process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True,
        )
        try:
            # If the control process receives a signal to stop,
            # then make sure to stop the command process.
            def kill_handler(signum, frame):  # pylint: disable=unused-argument
                command_process.terminate()
                sys.exit(exit_code_on_killed)

            signal.signal(signal.SIGHUP, kill_handler)
            signal.signal(signal.SIGTERM, kill_handler)
            signal.signal(signal.SIGINT, kill_handler)

            # Listen on stdout and stderr in parallel, preserving order,
            # writing stdout to debug logs and stderr to info logs.
            sel = selectors.DefaultSelector()
            sel.register(command_process.stdout, selectors.EVENT_READ)
            sel.register(command_process.stderr, selectors.EVENT_READ)
            while True:
                for key, _ in sel.select():
                    data = key.fileobj.read1().decode()
                    if not data:
                        return
                    if key.fileobj is command_process.stdout:
                        stdout_function(data)
                    else:
                        stderr_function(data)
        except BaseException as exc:
            exception_function(exc)
            command_process.terminate()
            raise

    control_process = multiprocessing.Process(target=target)
    control_process.start()
    return control_process
