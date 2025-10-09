from multiprocessing import shared_memory
from enum import Enum
import win32gui, win32con, win32api
import time

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
            self.sleeping = shared_memory.SharedMemory(create=False, size=1, name='sleeping')
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
    
    def _broadcast(self, input):
        self.sleeping.buf[0] = input