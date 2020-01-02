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

    ############ new ############

    # str : String to update label
    # direct connect to decensorButton.setText(str)
    update_decensorButton_Text = QtCore.Signal(str)

    # bool : set QPushButton Enabled (True or False)
    # direct connect to decensorButton.setEnabled(bool)
    update_decensorButton_Enabled = QtCore.Signal(bool)

    # direct connect to progressMessage.clear(None)
    clear_progressMessage = QtCore.Signal()

    # str : text to change
    # direct connect to statusLabel.setText
    update_statusLabel_Text = QtCore.Signal(str)

    # int : value to change
    # direct connect to progressBar.setValue(int)
    update_ProgressBar_SET_VALUE = QtCore.Signal(int)

    # int : value to change
    # direct connect to progressBar.setMaximum(int)
    update_ProgressBar_MAX_VALUE = QtCore.Signal(int)

    # int : value to change
    # direct connect to self.progressBar.setMinimum(int)
    update_ProgressBar_MIN_VALUE = QtCore.Signal(int)

    # str : value to change
    # direct connect to self.progressCursor.insertText(str)
    insertText_progressCursor = QtCore.Signal(str)

    # str : value to change
    # direct connect to self.progressMessage.append(str)
    appendText_progressMessage = QtCore.Signal(str)
