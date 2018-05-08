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
        """ run this function """
        trace6d=[]
        for i in range(6):
            trace6d.append([])
        # test car moving
        trace6d[0].append(0)
        trace6d[0].append(10)
        trace6d[0].append(20)
        trace6d[1].append(0)
        trace6d[1].append(20)
        trace6d[1].append(40)
        trace6d[5].append(2.3702363)
        trace6d[5].append(32.3702363)
        trace6d[5].append(-32.3702363)
        #print("thread", self.args, self.kwargs)
        self.signals.result.emit(trace6d)