import pyaedt

import os
import shutil

import numpy as np
import pandas as pd

class Variable:

    def __init__(self, design) :
        self.vars_range = []
        self.vars = {}
        self.design = design

    
    # variable setting in design
    def set_variable(self) :
        for name, value_unit in self.vars.items() :
            value, unit = value_unit
            self.design[name] = str(value) + str(unit)

        return self.vars
    

    # get random variable by predetermined setting
    def random_variable(self, set=True) :

        for name, min, max, res, unit in self.vars_range :
            value = np.random.choice(np.arange(min, max+res, res))
            self.vars[name] = [value, unit]

        if set == True :
            self.set_variable()

        return self.vars
    

    # return input variable as numpy data form
    def get_numpy(self, unit=True) :
       
        if unit == True :
            return np.array([[name, f"{value}{unit}"] for name, (value, unit) in self.vars.items()])
        else:
            return np.array([value for value, unit in self.vars.values()])


    # return input variables as pandas dataframe
    def get_pandas(self, unit=True) :

        if unit == True :
            data = {name: [f"{value}{unit}"] for name, (value, unit) in self.vars.items()}
        else:
            data = {name: [value] for name, (value, unit) in self.vars.items()}

        df = pd.DataFrame(data)
        return df
