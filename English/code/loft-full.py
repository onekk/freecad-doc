#
"""loft-full.py

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


DOC_NAME = "loft_ex"

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

def base_figure(dim_x, dim_y):
    """Create a polygon."""
    points = (
        (0.0, 0.0, 0.0),
        (dim_x, 0.0, 0.0),
        (dim_x, dim_y, 0.0),
        (0.0, dim_y, 0.0),
        (0.0, 0.0, 0.0)
    )

    obj = Part.makePolygon(points)

    return obj

# elements hold created wires
elements = []

# dimensions hold values that are (dim_x, dim_y, z height) of generating figures
dimensions = (
    (5.0, 5.0, 0.0),
    (5.0, 5.0, 5.0),
    (8.0, 8.0, 7.0),
    (10.0, 10.0, 10.0),
    (8.0, 8.0, 13.0),
    (5.0, 5.0, 20.0),
    (5.0, 5.0, 25.0),
    )

for dims in dimensions:
    obj = base_figure(dims[0], dims[1])
    obj.Placement = Placement(Vector(dims[0] * -0.5, dims[1] * -0.5, dims[2]), ROT0)
    elements.append(obj)

# makeLoft(list of wires,[solid=False,ruled=False,closed=False,maxDegree=5])

sol_loft = Part.makeLoft(elements, True, True, False, 5)

Part.show(sol_loft, "Loft_Solid")


elem2 = []

dims2 = (
    (8.0, 5.0),
    (8.0, 7.5),
    (8.0, 10.0),
    (8.0, 7.5),
    (8.0, 5.0),
    )

idx = 0

for dims in dims2:
    obj = base_figure(dims[0], dims[1])
    step = 25
    pl1 = Placement(Vector(20, 0, 0), Rotation(0, 0, 90))
    pl2 = Placement(Vector(0, 0, 0), Rotation(step * idx, 0, 0), Vector(0, 0, 0))
    obj.Placement = pl2.multiply(pl1)
    # Part.show(obj)
    elem2.append(obj)
    idx += 1

# makeLoft(list of wires,[solid=False,ruled=False,closed=False,maxDegree=5])

sol_loft2 = Part.makeLoft(elem2, True, False, False, 3)

Part.show(sol_loft2, "Loft_Solid_2")

setview()
