import pyaedt

from .polyline import Polyline


class LibModeler:
    def __init__(self, design):
        self.initialized = False
        self.design = design

        self._polyline = Polyline(self)

    @property
    def polyline(self):
        return self._polyline

    def initialize_modeler(self):
        self.initialized = True


    def test(self) :
        origin = [0, 0, 0]
        dimension = [100, 100 ,100]
        self.design.modeler.create_box(origin=origin, sizes=dimension)


    def create_region(self, x_p=100, x_n=100, y_p=100, y_n=100, z_p=100, z_n=100) :

        region = self.design.modeler.create_air_region(x_pos=x_p, x_neg=x_n, y_pos=y_p, y_neg=y_n, z_pos=z_p, z_neg=z_n)

        region_face = self.design.modeler.get_object_faces("Region")

        self.design.assign_material(assignment = region, material="vacuum")
        self.design.assign_radiation(assignment=region_face, radiation="Radiation")
        
        return region




    def create_line(self, polyline, width_list, thick="1mm") :

        point1 = None
        point2 = None

        return 0