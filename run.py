from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
class RunSignals(QObject):
    '''
    Defines the signals available from a running thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
class CarRunning(QRunnable):
    """
    work thread
    """
    def __init__(self, *args, **kwargs):
        super(CarRunning, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = RunSignals()
    @pyqtSlot()
    def run(self):
        """
        run this function
        """
        tlist=[]
        tlist.append(5)
        print("thread", self.args, self.kwargs)
        self.signals.result.emit(tlist)