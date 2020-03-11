#
"""gfc.py

   This code was written as an sample code 
   for "FreeCAD Scripting Guide" 
     
   Author: Carlo Dormeletti
   Copyright: 2020
   Licence: CC BY-NC-ND 4.0 IT 
"""

import FreeCAD
from FreeCAD import Base, Vector
import Part
from math import pi, sin, cos


# EPS= tolerance to uset to cut the parts
EPS = 0.10
EPS_C = EPS * -0.5

def cubo(nome, lung, larg, alt, cent = True):
    obj_b = doc.addObject("Part::Box", nome)
    obj_b.Length = lung
    obj_b.Width = larg
    obj_b.Height = alt

    doc.recompute()
    
    if cent == True:
        obj_b.Placement = FreeCAD.Placement(
                Vector(lung * -0.5, larg * -0.5, 0), 
                FreeCAD.Rotation(0, 0, 0), FreeCAD.Vector(0,0,0))

    return obj_b

def base_cyl(doc, nome, ang, rad, alt ):
    obj = doc.addObject("Part::Cylinder", nome)
    obj.Angle = ang
    obj.Radius = rad
    obj.Height = alt
    
    doc.recompute()

    return obj   


def cubo_stondato(doc, nome, lung, larg, alt, raggio, off_z):  

    c_c1 = Vector((lung * -0.5) + raggio, (larg * -0.5) + raggio, 0)
    c_c2 = Vector((lung * -0.5) + raggio, (larg * 0.5) - raggio, 0)
    c_c3 = Vector((lung * 0.5) - raggio, (larg * 0.5) - raggio,  0)
    c_c4 = Vector((lung * 0.5) - raggio, (larg * -0.5) + raggio, 0)

    obj_dim = c_c3 - c_c1
    fi_lung = obj_dim[0] + raggio * 2
    fi_larg = obj_dim[1] + raggio * 2

    obj_c1 = base_cyl(nome +'_cil1', 360, raggio, alt)
    obj_c1.Placement = FreeCAD.Placement(
            c_c1, 
            FreeCAD.Rotation(0, 0, 0),
            FreeCAD.Vector(0,0,0)) 

    obj_c2 = base_cyl(nome +'_cil2', 360, raggio, alt)
    obj_c2.Placement = FreeCAD.Placement(
            c_c2, 
            FreeCAD.Rotation(0, 0, 0),
            FreeCAD.Vector(0,0,0)) 

    obj_c3 = base_cyl(nome +'_cil3', 360, raggio, alt)
    obj_c3.Placement = FreeCAD.Placement(
            c_c3,
            FreeCAD.Rotation(0, 0, 0),
            FreeCAD.Vector(0,0,0)) 

    obj_c4 = base_cyl(nome +'_cil4', 360, raggio, alt)
    obj_c4.Placement = FreeCAD.Placement(
            c_c4, 
            FreeCAD.Rotation(0, 0, 0),
            FreeCAD.Vector(0,0,0)) 


    obj1 = cubo(nome + "_int_lu", fi_lung , obj_dim[1], alt, False)
    obj1.Placement = FreeCAD.Placement(Vector(fi_lung * -0.5, obj_dim[1] * -0.5, 0), FreeCAD.Rotation(0, 0, 0), FreeCAD.Vector(0,0,0))    

    obj2 = cubo(nome + "_int_la", obj_dim[0] , fi_larg, alt, False)
    obj2.Placement = FreeCAD.Placement(Vector(obj_dim[0] * -0.5, fi_larg * -0.5, 0), FreeCAD.Rotation(0, 0, 0), FreeCAD.Vector(0,0,0))    


    obj_int = doc.addObject("Part::MultiFuse", nome)
    obj_int.Shapes = [obj1, obj2, obj_c1, obj_c2, obj_c3, obj_c4]
    obj_int.Refine = True
    DOC.recompute()

    obj_int.Placement = FreeCAD.Placement(
        Vector(0, 0, off_z),
        FreeCAD.Rotation(0, 0, 0),
        FreeCAD.Vector(0,0,0)
        )   
    
    return obj_int

