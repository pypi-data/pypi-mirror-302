


class Polyline :

    def __init__(self, modeler) :
        self.modeler = modeler


    def rectangluar_coil(self, turns=4, polyline=None, end="top_center", **kwargs) :

        if polyline is None:
            polyline = []

        # variable setting
        outer_x = kwargs.get("outer_x", "150mm")
        outer_y = kwargs.get("outer_y", "90mm")

        width = kwargs.get("width", "3mm")

        space_x = kwargs.get("space_x", "10mm")
        space_y = kwargs.get("space_y", "15mm")

        for itr in range(turns) :

            ox = f"({outer_x}/2)"
            oy = f"({outer_y}/2)"

            sx = f"(({width})+({space_y}))"
            sy = f"(({width})+({space_x}))"

            if itr == 0 :
                polyline.append([f"-{ox} + {itr}*{sx}", f"-{oy} + {itr}*{sy}", f"0"])
            polyline.append([f"-{ox} + {itr}*{sx}", f"{oy} - {itr}*{sy}", f"0"])
            polyline.append([f"{ox} - {itr}*{sx}", f"{oy} - {itr}*{sy}", f"0"])
            polyline.append([f"{ox} - {itr}*{sx}", f"-{oy} + {itr}*{sy}", f"0"])
            polyline.append([f"-{ox} + {itr+1}*{sx}", f"-{oy} + {itr}*{sy}", f"0"])

            if itr == turns-1 and end == "top_center" :
                polyline.append([f"-{ox} + {itr+1}*{sx}", f"{oy} - {itr+1}*{sy}", f"0"])
                polyline.append([f"{width}/2", f"{oy} - {itr+1}*{sy}", f"0"])


        return polyline
    


    def rectangluar_coil2(self, turns=4, polyline=None, end="top_center", **kwargs) :

        if polyline is None:
            polyline = []

        # variable setting
        outer_x = kwargs.get("outer_x", "150mm")
        outer_y = kwargs.get("outer_y", "90mm")

        width = kwargs.get("width", "3mm")

        space_x = kwargs.get("space_x", "10mm")
        space_y = kwargs.get("space_y", "15mm")

        ratio = kwargs.get("ratio", "5mm")



        for itr in range(turns) :

            ox = f"({outer_x}/2)"
            oy = f"({outer_y}/2)"

            sx = f"(({width})+({space_y}))"
            sy = f"(({width})+({space_x}))"

            r = f"({ratio})"

            if itr == 0 :
                polyline.append([f"(-{ox} + {itr}*{sx}) + {r}", f"(-{oy} + {itr}*{sy})", f"0"])

            polyline.append([f"(-{ox} + {itr}*{sx})", f"(-{oy} + {itr}*{sy}) + {r}", f"0"])
            polyline.append([f"(-{ox} + {itr}*{sx})", f"({oy} - {itr}*{sy}) - {r}", f"0"])
            polyline.append([f"(-{ox} + {itr}*{sx}) + {r}", f"({oy} - {itr}*{sy})", f"0"])

            polyline.append([f"({ox} - {itr}*{sx}) - {r}", f"({oy} - {itr}*{sy})", f"0"])
            polyline.append([f"({ox} - {itr}*{sx})", f"({oy} - {itr}*{sy}) - {r}", f"0"])
            polyline.append([f"({ox} - {itr}*{sx})", f"(-{oy} + {itr}*{sy}) + {r}", f"0"])
            polyline.append([f"({ox} - {itr}*{sx}) - {r}", f"(-{oy} + {itr}*{sy})", f"0"])

            polyline.append([f"(-{ox} + {itr+1}*{sx}) + {r}", f"(-{oy} + {itr}*{sy})", f"0"])


            if itr == turns-1 and end == "top_center" :
                polyline.append([f"(-{ox} + {itr+1}*{sx})", f"(-{oy} + {itr+1}*{sy}) + {r}", f"0"])
                polyline.append([f"(-{ox} + {itr+1}*{sx})", f"({oy} - {itr+1}*{sy}) - {r}", f"0"])
                polyline.append([f"(-{ox} + {itr+1}*{sx}) + {r}", f"({oy} - {itr+1}*{sy})", f"0"])
                polyline.append([f"{width}/2", f"{oy} - {itr+1}*{sy}", f"0"])


        return polyline



    def old_rectangluar_coil(self, turns=4, polyline=None, width_list=None, **kwargs) :

        if polyline is None:
            polyline = []
        if width_list is None:
            width_list = []
        
        # variable setting
        outer_x = kwargs.get("outer_x", "150mm")
        outer_y = kwargs.get("outer_y", "90mm")

        width_x = kwargs.get("width_x", "3mm")
        width_y = kwargs.get("width_y", "5mm")

        space_x = kwargs.get("space_x", "10mm")
        space_y = kwargs.get("space_y", "15mm")



        for itr in range(turns) :

            ox = f"({outer_x})"
            oy = f"({outer_y})"

            sx = f"(({width_y})+({space_y}))"
            sy = f"(({width_x})+({space_x}))"

            if itr == 0 :
                polyline.append([f"-{ox} + {itr}*{sx}", f"-{oy} + {itr}*{sy}", f"0"])
            polyline.append([f"-{ox} + {itr}*{sx}", f"{oy} - {itr}*{sy}", f"0"])
            polyline.append([f"{ox} - {itr}*{sx}", f"{oy} - {itr}*{sy}", f"0"])
            polyline.append([f"{ox} - {itr}*{sx}", f"-{oy} + {itr}*{sy}", f"0"])
            polyline.append([f"-{ox} + {itr+1}*{sx}", f"-{oy} + {itr}*{sy}", f"0"])

            width_list.append(width_y)
            width_list.append(width_x)
            width_list.append(width_y)
            width_list.append(width_x)


        return polyline, width_list

