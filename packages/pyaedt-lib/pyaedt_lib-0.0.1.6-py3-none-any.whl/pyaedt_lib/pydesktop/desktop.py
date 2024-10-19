import pyaedt

from ansys.aedt.core import Desktop

import os
import shutil
import psutil

class LibDesktop(Desktop):

    def __init__(self, version=None, non_graphical=False, student_version=False, *args, **kwargs):

        if 'version' in kwargs:
            version = kwargs.pop('version')

        if 'non_graphical' in kwargs:
            non_graphical = kwargs.pop('non_graphical')

        if 'student_version' in kwargs:
            student_version = kwargs.pop('student_version')


        super().__init__(version=version, non_graphical=non_graphical, student_version=student_version)


        self.disable_autosave()

        self.pid = self.aedt_process_id



    def close_desktop(self) :

        super().close_desktop()


    
    def get_process_info(self) :

        try : 

            process = psutil.Process(self.pid)
            self.cpu_usage = process.cpu_percent(interval=1) # 1 sec CPU usage
            self.memory_usage = process.memory_info().rss / (1024 * 1024 * 1024) # [Unit : GB]
            
            return True
    
        except psutil.NoSuchProcess :

            return False
