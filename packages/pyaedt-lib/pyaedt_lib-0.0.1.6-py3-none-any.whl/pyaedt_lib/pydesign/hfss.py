import pyaedt

from ansys.aedt.core import Hfss

from ..pymodeler.modeler import LibModeler
from ..variable.variable import Variable


class LibHfss(Hfss):

    def __init__(self, project=None, design_name="design", solver="EddyCurrent"):

        super().__init__(
            project=project.project_file_name, 
            design=design_name, 
            solution_type=solver,
            new_desktop = False
            )
        
        self._lmodeler = LibModeler(self)
        self._variable = Variable(self)

    @property
    def lmodeler(self):
        return self._lmodeler
    
    @property
    def variable(self):
        return self._variable
    



