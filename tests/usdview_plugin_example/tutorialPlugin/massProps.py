from pxr import UsdPhysics, Gf, UsdGeom
from pxr.Usdviewq.usdviewApi import UsdviewApi
import numpy as np

def MassProps(usdview_api:UsdviewApi):
    for prim in usdview_api.dataModel.selection.getPrims():
        mass, moment = calc_mass_properties(prim, usdview_api.stage)
        print(f"Prim:{prim.GetPath()}, Mass:{mass}, CoG:{moment/mass}")

def calc_mass_properties(current_prim,stage,depth=0):
    """Recursively walks the prim tree and reports mass properties at each level.
    This would change the 'view' of the mass properties rollup.

    """
    
    children_mass = 0
    children_moment = np.zeros([3])

    # iterate over children and recursively call calc_mass_properties on children.
    for child_prim in current_prim.GetChildren():
        mass, moment = calc_mass_properties(child_prim, depth+1)
        children_mass += mass
        children_moment += moment
    
    if len(current_prim.GetChildren()) > 0: 
        cog = children_moment/children_mass
        # report branch properties => update view
        # print(f"{' '*depth*4}{current_prim.GetPath()}\t{children_mass}\t{cog.tolist()}")

        # set mass properties of parent node in the session layer
        if not stage:
            stage.SetEditTarget(stage.GetSessionLayer())
            mass_api = UsdPhysics.MassAPI.Apply(current_prim)
            mass_api.CreateMassAttr(children_mass)
            mass_api.CreateCenterOfMassAttr(Gf.Vec3f(cog.tolist()))
            stage.SetEditTarget(stage.GetRootLayer())
    
    # need to work on a better filter here, but idea is to get any leaf prims with mass property attributes.
    if 'PhysicsMassAPI' in current_prim.GetAppliedSchemas() and current_prim.GetTypeName() != 'Xform' : # leaf
        current_mass = UsdPhysics.MassAPI(current_prim).GetMassAttr().Get()
        prim_world_transform = UsdGeom.Xformable(current_prim).ComputeLocalToWorldTransform(1)
        translation = Gf.Transform(prim_world_transform).GetTranslation()
        center_of_mass = UsdPhysics.MassAPI(current_prim).GetCenterOfMassAttr().Get()
        current_moment = (np.array(center_of_mass) + np.array(translation))*np.array(current_mass)
        mass = current_mass + children_mass
        moment = current_moment+children_moment
        # print(f"{' '*depth*4}{current_prim.GetPath()}\t{mass}\t{moment/mass}")
        return mass, moment
    else: # root
        return children_mass, children_moment