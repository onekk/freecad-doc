"""base-objects-full.py

   This code was written as an sample code
   for "FreeCAD Scripting Guide"

   Author: Carlo Dormeletti
   Copyright: 2022
   Licence: CC BY-NC-ND 4.0 IT
"""

import os
from math import pi, sin, cos

import FreeCAD
from FreeCAD import Placement, Rotation, Vector
import Part


DOC_NAME = "base_objects"

def activate_doc():
    """activate document"""
    FreeCAD.setActiveDocument(DOC_NAME)
    FreeCAD.ActiveDocument = FreeCAD.getDocument(DOC_NAME)
    FreeCADGui.ActiveDocument = FreeCADGui.getDocument(DOC_NAME)
    print("{0} activated".format(DOC_NAME))


def setview():
    """Rearrange View"""
    DOC.recompute()
    VIEW.viewAxometric()
    VIEW.setAxisCross(True)
    VIEW.fitAll()


def deleteObject(obj):
    if hasattr(obj, "InList") and len(obj.InList) > 0:
        for o in obj.InList:
            deleteObject(o)
            try:
                DOC.removeObject(o.Name)
            except RuntimeError as rte:
                errorMsg = str(rte)
                if errorMsg != "This object is currently not part of a document":
                    FreeCAD.Console.PrintError(errorMsg)
                    return False
    return True


def clear_DOC():
    """
    Clear the active DOCument deleting all the objects
    """
    while DOC.Objects:
        obj = DOC.Objects[0]
        name = obj.Name

        if not hasattr(DOC, name):
            continue

        if not deleteObject(obj):
            FreeCAD.Console.PrintError("Exiting on error")
            os.sys.exit()

        DOC.removeObject(obj.Name)

        DOC.recompute()


if FreeCAD.ActiveDocument is None:
    FreeCAD.newDocument(DOC_NAME)
    print("Document: {0} Created".format(DOC_NAME))

# test if there is an active document with a "proper" name
if FreeCAD.ActiveDocument.Name == DOC_NAME:
    print("DOC_NAME exist")
else:
    print("DOC_NAME is not active")
    # test if there is a document with a "proper" name
    try:
        FreeCAD.getDocument(DOC_NAME)
    except NameError:
        print("No Document: {0}".format(DOC_NAME))
        FreeCAD.newDocument(DOC_NAME)
        print("Document Created".format(DOC_NAME))

DOC = FreeCAD.getDocument(DOC_NAME)
GUI = FreeCADGui.getDocument(DOC_NAME)
VIEW = GUI.ActiveView

activate_doc()

clear_DOC()

ROT0 = Rotation(0,0,0)

### CODE START HERE ###


def base_cube(name, lng, wid, hei):
    obj_b = DOC.addObject("Part::Box", name)
    obj_b.Length = lng
    obj_b.Width = wid
    obj_b.Height = hei

    DOC.recompute()

    return obj_b

def base_cyl(name, ang, rad, hei):
    obj = DOC.addObject("Part::Cylinder", name)
    obj.Angle = ang
    obj.Radius = rad
    obj.Height = hei

    DOC.recompute()

    return obj


def fuse_obj(name, obj_0, obj_1):
    obj = DOC.addObject("Part::Fuse", name)
    obj.Base = obj_0
    obj.Tool = obj_1
    obj.Refine = True
    DOC.recompute()

    return obj


def mfuse_obj(name, obj_0, obj_1):
    obj = DOC.addObject("Part::MultiFuse", name)
    obj.Shapes = (obj_0, obj_1)
    obj.Refine = True
    DOC.recompute()

    return obj


def cut_obj(name, obj_0, obj_1):
    obj = DOC.addObject("Part::Cut", name)
    obj.Base = obj_0
    obj.Tool = obj_1
    obj.Refine = True
    DOC.recompute()

    return obj


def int_obj(name, obj_0, obj_1):
    obj = DOC.addObject("Part::MultiCommon", name)
    obj.Shapes = (obj_0, obj_1)
    obj.Refine = True
    DOC.recompute()

    return obj


obj = base_cube("test_cube", 5, 5, 5)

obj_1 = base_cyl('test_cylinder', 360, 2, 10)

f_obj = fuse_obj("fusion-cube-cyl", obj, obj_1)
f_obj.Placement = Placement(Vector(20, 0, 0), ROT0)

mf_obj = mfuse_obj("multifusion-cube-cyl", obj, obj_1)
mf_obj.Placement = Placement(Vector(20, 20, 0), ROT0)

c_obj = cut_obj("cut-cube-cyl", obj, obj_1)
c_obj.Placement = Placement(Vector(40, 0, 0), ROT0)

i_obj = int_obj("is-cube-cyl", obj, obj_1)
i_obj.Placement = Placement(Vector(40, 20, 0), ROT0)

setview()
