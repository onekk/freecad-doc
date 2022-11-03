"""spline_surface.py

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


DOC_NAME = "spline_surface"

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

# from /Mod/Draft/draftfunctions/scale.py
# implemented by Dion Moult during 0.19 dev cycle

points = [
    Vector(0.0, 0.0, 0.0),
    Vector(100.0, 100.0, 0.0),
    Vector(100.0, 300.0, 0.0),
    Vector(0.0, 400.0, 0.0),
    Vector(0.0, 400.0, 0.0)
    ]

spline = Part.BSplineCurve()
spline.interpolate(points)

DOC.recompute()

sp_curv1 = Part.Wire(spline.toShape())

# Part.show(sp_curv1, "Spline")

scale = Vector(0.5, 0.5, 0.5)
center = Vector(0, 0, 0)

poles = spline.getPoles()

npoles = []

for index, point in enumerate(poles):
    npoint = point.sub(center).scale(scale.x, scale.y, scale.z).add(center)
    npoles.append(npoint)

spline2 = Part.BSplineCurve()
spline2.interpolate(npoles)

sp_curv2 = Part.Wire(spline2.toShape())
sp_curv2.Placement = Placement(Vector(1500, 0, 0), ROT0)

DOC.recompute()

# Part.show(sp_curv2, "Spline2")

surf = Part.makeRuledSurface(sp_curv1, sp_curv2)

#Part.show(surf, "surface")

# create bottom face
