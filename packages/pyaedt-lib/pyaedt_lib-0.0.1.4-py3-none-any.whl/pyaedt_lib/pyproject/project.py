import pyaedt

import os
import shutil

class LibProject:

    def __init__(
            self, 
            desktop = None, # desktop class object
            dir = os.path.expanduser('~/Documents/Ansoft'), 
            project_name = "project",
            itr = True
        ):


        self.dir = dir
        self.project_name = project_name


        self.desktop = desktop # LibDesktop class object


        # create new project in ansys default directory
        self.project = self.desktop.odesktop.NewProject(pyaedt.generate_unique_project_name())
        temp_dir = self.project.GetPath()

        # delete previous simulation folder
        if itr and os.path.exists(dir) == True :
            shutil.rmtree(dir)
        os.mkdir(dir)

        # save project
        self.project_file_name = f"{dir}\\{project_name}.aedt"
        self.project.SaveAs(self.project_file_name, True)

        # delete temp folder
        if os.path.exists(temp_dir) :
            shutil.rmtree(temp_dir)


    def __getattr__(self, name):
        return getattr(self.project, name)
    

    def test(self):

        print("test")
    

    def test2(self) :

        print("test2")


    def test3(self) :

        print("test3")