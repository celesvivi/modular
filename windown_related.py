from multiprocessing import shared_memory
from enum import Enum
import win32gui, win32con, win32api
import time
# VERSION 1.1
class PowerEvent(Enum):
    """Windows power events"""
    SUSPEND = 0x0004            
    RESUME_AUTO = 0x0012        
    RESUME_USER = 0x0007 

class SleepingStateMoniter:
    def __init__(self):
        try:
            self.sleeping = shared_memory.SharedMemory(create=True, size=1, name='sleeping')
        except FileExistsError:
            pass
        self.sleeping.buf[0] = 0
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.lpszClassName = "PyListener"
        wc.hInstance = win32api.GetModuleHandle(None)
        try:
            win32gui.RegisterClass(wc)
        except Exception:
            pass

        self._hwnd = win32gui.CreateWindow(wc.lpszClassName, "", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
        try:
            while True:
                win32gui.PumpWaitingMessages()
                time.sleep(0.01)
        finally:
            win32gui.DestroyWindow(self._hwnd)
            self.sleeping.close()
            self.sleeping.unlink() 
    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if not msg == win32con.WM_POWERBROADCAST:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
        if wparam == PowerEvent.SUSPEND.value:
            self._broadcast(1)
        if wparam == PowerEvent.RESUME_AUTO.value or wparam == PowerEvent.RESUME_USER.value:
            self._broadcast(0)
        
        return 0
    
    def _broadcast(self, input):
        self.sleeping.buf[0] = input
def _start_monitor():
    print('started')
    """Helper method to start monitor in separate process"""
    SleepingStateMoniter()

class output_stuff:
    """ALWAYS USE THIS IN if __name__ == '__main__': IDK WHY"""
    def __init__(self):
        self.monitor_process = None
        #Call shared memory from SleepingStateMoniter, if there isn't share memory, intialize SSM -> now there is shared memory
        try:
            self.sleeping = shared_memory.SharedMemory(create=False, name='sleeping')
            print('good')
        except FileNotFoundError:
            print('no good')
            from multiprocessing import Process
            self.monitor_process = Process(target = _start_monitor, daemon = True)
            self.monitor_process.start()
            time.sleep(0.5)
            self.sleeping = shared_memory.SharedMemory(create=False, name='sleeping')

    def sleeping_or_not(self):
        """True mean sleeping, false mean not sleep"""
        return self.sleeping.buf[0] == 1