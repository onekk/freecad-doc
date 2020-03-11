#
"""ob-ex-full.py

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

DOC = FreeCAD.activeDocument()
DOC_NAME = "Pippo"

def clear_doc():
    """
    Clear the active document deleting all the objects
    """
    for obj in DOC.Objects:
        DOC.removeObject(obj.Name)

def setview():
    """Rearrange View"""
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewAxometric()
    FreeCAD.Gui.activeDocument().activeView().setAxisCross(True)


if DOC is None:
    FreeCAD.newDocument(DOC_NAME)
    FreeCAD.setActiveDocument(DOC_NAME)
    DOC = FreeCAD.activeDocument()

else:

    clear_doc()


# EPS= tolerance to uset to cut the parts
EPS = 0.10
EPS_C = EPS * -0.5


def cubo(nome, lung, larg, alt):
    obj_b = DOC.addObject("Part::Box", nome)
    obj_b.Length = lung
    obj_b.Width = larg
    obj_b.Height = alt

    DOC.recompute()
    
    return obj_b

def base_cyl(nome, ang, rad, alt ):
    obj = DOC.addObject("Part::Cylinder", nome)
    obj.Angle = ang
    obj.Radius = rad
    obj.Height = alt
    
    DOC.recompute()

    return obj   

def fuse_obj(nome, obj_0, obj_1):
    obj = DOC.addObject("Part::Fuse", nome)
    obj.Base = obj_0
    obj.Tool = obj_1
    obj.Refine = True
    DOC.recompute()

    return obj

def mfuse_obj(nome, obj_0, obj_1):
    obj = DOC.addObject("Part::MultiFuse", nome)
    obj.Shapes = (obj_0, obj_1)
    obj.Refine = True
    DOC.recompute()

    return obj

def cut_obj(nome, obj_0, obj_1):
    obj = DOC.addObject("Part::Cut", nome)
    obj.Base = obj_0
    obj.Tool = obj_1
    obj.Refine = True
    DOC.recompute()

    return obj

def int_obj(nome, obj_0, obj_1):
    obj = DOC.addObject("Part::MultiCommon", nome)
    obj.Shapes = (obj_0, obj_1)
    obj.Refine = True
    DOC.recompute()

    return obj

# definizione oggetti

obj = cubo("cubo_di_prova", 5, 5, 5)

obj1 = base_cyl('primo cilindro', 360,2,10)

# mfuse_obj("cubo-cyl-fu", obj, obj1)

#cut_obj("cubo-cyl-cu", obj, obj1)

int_obj("cubo-cyl-is", obj, obj1)

setview()

