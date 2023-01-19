
from pxr import Usd, UsdGeom, UsdPhysics,Gf,Tf
import numpy as np

# build geometry
stage = Usd.Stage.CreateNew('MassProps_01.usda')
print(dir(Usd.Stage))