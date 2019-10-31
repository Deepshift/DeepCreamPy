from PySide2 import QtCore

# Signals used for sharing status between threads(gui thread <-> decensoring thread)
class Signals(QtCore.QObject):

    # str : tells status (print in cmd for debug)
    # int : value to change
    # usage example in other class(thread) :
    # → self.signals.total_ProgressBar_update_MAX_VALUE.emit("update value :"+str(max), max)
    total_ProgressBar_update_MAX_VALUE = QtCore.Signal(str, int)
    total_ProgressBar_update_VALUE = QtCore.Signal(str, int)

    signal_ProgressBar_update_MAX_VALUE = QtCore.Signal(str, int)
    signal_ProgressBar_update_VALUE = QtCore.Signal(str, int)

    # str : tells status (print in cmd for debug)
    # str : String to update label
    update_progress_LABEL = QtCore.Signal(str, str)
