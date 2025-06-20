import ctypes

class EverythingIPC:
    def __init__(self, dll_path):
        self.dll = ctypes.WinDLL(dll_path)
        self.dll.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
        self.dll.Everything_GetResultFullPathNameW.restype = ctypes.c_uint
        self.dll.Everything_GetResultFullPathNameW.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_uint]
    def query(self, search, results_max):
        self.dll.Everything_SetSearchW(search)
        self.dll.Everything_QueryW(1)
        results = []
        for i in range(min(self.dll.Everything_GetNumResults(), results_max)):
            buf = ctypes.create_unicode_buffer(1024)
            self.dll.Everything_GetResultFullPathNameW(i, buf, 1024)
            results.append(buf.value)
        return results
