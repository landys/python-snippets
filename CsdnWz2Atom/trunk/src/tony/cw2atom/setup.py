# the command to sun setup: python setup.py py2exe
from distutils.core import setup  
import py2exe  
#includes = ["encodings", "encodings.*"]  
options = {"py2exe":  
            {   "compressed": 1,  
                "optimize": 2,  
#                "includes": includes,  
                "bundle_files": 1  # generate only .exe file containing all things.
            }  
          }  
setup(     
    version = "0.1.0",  
    description = "csdn cw to atom xml file.",  
    name = "cw2atom",  
    options = options,  
    zipfile=None,  
    #windows=[{"script": "cw2atom.py", "icon_resources": [(1, "cw2atom.ico")] }],    
    console=[{"script": "cw2atom.py", "icon_resources": [(1, "cw2atom.ico")] }],   
    )  