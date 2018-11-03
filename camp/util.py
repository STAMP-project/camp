#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from inspect import isgeneratorfunction

from os import devnull, dup, dup2

from sys import stderr



def redirect_stderr_to(destination):

    def decorate(function):

        def wrapped_generator(*args, **kwargs):
            with StderrRedirect(destination):
                 for each in function(*args, **kwargs):
                     yield each

        def wrapped(*args, **kwargs):
            with StderrRedirect(destination):
                return function(*args, **kwargs)
                     
        if isgeneratorfunction(function):
            return wrapped_generator
        return wrapped
        
    return decorate

    


class StderrRedirect(object):

    
    def __init__(self, destination=devnull):
        self._destination = destination


    def __enter__(self):
        self._stderr_fd = stderr.fileno()
        self._destination_file = open(self._destination, "w")
        self._destination_fd = self._destination_file.fileno()

        # Create a second file descriptor that also points to stderr
        self._memento_fd = dup(self._stderr_fd)

        # Redirect stderr so it points towards the given destination
        dup2(self._destination_fd, self._stderr_fd)

        return self


    def __exit__(self, ex_type, ex_value, ex_traceback):
        self._destination_file.close()

        # Redirect stderr so it points back towards its original file
        dup2(self._memento_fd, self._stderr_fd)

        
