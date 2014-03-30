# the command to sun setup: python setup.py py2exe
from distutils.core import setup  
import py2exe  
#includes = ["encodings", "encodings.*"]  
# package _strptime fixed run error in exe: "ImportError: No module named _strptime" 
options = {"py2exe":  
            {   "compressed": 1,  
                "optimize": 2, 
                "packages": ["_strptime"],
#                "includes": includes,  
                "bundle_files": 1  # generate only .exe file containing all things.
            }  
          }  
setup(     
    version = "0.1.0",  
    description = "atom xml to bookmark html file for delicious.",  
    name = "atom2bm",  
    options = options,  
    zipfile=None,  
    #windows=[{"script": "atom2bm.py", "icon_resources": [(1, "atom2bm.ico")] }],    
    console=[{"script": "atom2bm.py", "icon_resources": [(1, "atom2bm.ico")] }],   
    )  