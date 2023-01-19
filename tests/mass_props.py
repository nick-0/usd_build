from pxr import Usd, UsdGeom, UsdPhysics,Gf,Tf
import numpy as np

# build geometry
print(dir(Usd.Stage))
stage = Usd.Stage.CreateNew('MassProps_01.usda')
UsdGeom.SetStageUpAxis(stage,'Z')
UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdPhysics.SetStageKilogramsPerUnit(stage, 1.0)
base = UsdGeom.Xform.Define(stage,'/physics_scene')
UsdPhysics.Scene(base).Define(stage,'/physics_scene')

# build four sets of spheres with mass attributes.
for i in range(4):
    # container prim
    xformPrim = UsdGeom.Xform.Define(stage, f'/set_00{i}')
    UsdGeom.XformCommonAPI(xformPrim).SetTranslate([i*10,0,0])

    # sphere 1
    spherePrim01 = UsdGeom.Sphere.Define(stage, f'/set_00{i}/sphere_01')
    mass_api = UsdPhysics.MassAPI.Apply(spherePrim01.GetPrim())
    mass_api.CreateMassAttr(10.0)
    center_of_mass = Gf.Vec3f([0,0,0])
    mass_api.CreateCenterOfMassAttr(center_of_mass)

    # sphere 2
    spherePrim02 = UsdGeom.Sphere.Define(stage, f'/set_00{i}/sphere_02')
    spherePrim02.GetRadiusAttr().Set(2.0)
    mass_api = UsdPhysics.MassAPI.Apply(spherePrim02.GetPrim())
    mass_api.CreateMassAttr(20.0)
    mass_api.CreateCenterOfMassAttr(center_of_mass)
    UsdGeom.XformCommonAPI(spherePrim02).SetTranslate([0,10,0])

def calc_mass_properties(current_prim,depth=0):
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
        print(f"{' '*depth*4}{current_prim.GetPath()}\t{children_mass}\t{cog.tolist()}")

        # set mass properties of parent node in the session layer
        if current_prim != stage.GetPseudoRoot():
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
        print(f"{' '*depth*4}{current_prim.GetPath()}\t{mass}\t{moment/mass}")
        return mass, moment
    else: # root
        return children_mass, children_moment

def on_stage_changed(notice, stage):
    """Update mass properties report on changes."""
    # filter for changes outside of session layer to avoid infinite loop.
    for path in notice.GetChangedInfoOnlyPaths():
        if 'physics:mass' in str(path) and '-session.usda' not in stage.GetEditTarget().GetLayer().GetDisplayName() :
            calc_mass_properties( stage.GetPrimAtPath('/'))

# register callback on changes
attribute_changed = Tf.Notice.Register(
    Usd.Notice.ObjectsChanged,
    on_stage_changed,
    stage
)

# initial mass properties report
mass, moment = calc_mass_properties( stage.GetPrimAtPath('/'))

print('='*75)
print('='*75)

# changes should trigger update
spherePrim02 = stage.GetPrimAtPath('/set_001/sphere_02')
spherePrim02.GetAttribute('physics:mass').Set(4.0)

stage.GetRootLayer().Save()