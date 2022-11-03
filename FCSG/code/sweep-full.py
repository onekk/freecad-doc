#
"""sweep-full.py

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


DOC_NAME = "sweep_ex"

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

ROT0 = Rotation(0, 0, 0)

### CODE START HERE ###

VZOR = Vector(0, 0, 0)
EPS = 0.001
EPS_C = EPS * -0.5

c1rad = 120
spess = 20

c2rad = c1rad - spess

c3rad = 150

circ1 = Part.makeCircle(c1rad, Vector(0, 0, 0))

# Part.show(circ1, "circ1")

circ2 = Part.makeCircle(c2rad, Vector(0, 0, 0))

# Part.show(circ2, "circ2")

circ3 = Part.makeCircle(c3rad, Vector(0, 0, 0), Vector(0, 1, 0))

# Part.show(circ3, "circ3")

sweep_crv_e = circ3.Curve.toShape(pi, pi / 4.0)

sweep_crv_i = circ3.Curve.toShape(pi - EPS, (pi / 4.0) + EPS)

sec_e = DOC.addObject("Part::Feature", "ext_section")
sec_e.Shape = Part.Face(Part.Wire(circ1))

spine = DOC.addObject("Part::Feature", "spine")
spine.Shape = sweep_crv_e
spine.Placement = Placement(Vector(c3rad, 0, 0), ROT0)

DOC.recompute()

sweep_e = DOC.addObject("Part::Sweep", "sweep_ext")
sweep_e.Sections = sec_e
sweep_e.Spine = spine
sweep_e.Solid = True

sec_i = DOC.addObject("Part::Feature", "int_section")
sec_i.Shape = Part.Face(Part.Wire(circ2))

spine_i = DOC.addObject("Part::Feature", "spine")
spine_i.Shape = sweep_crv_i
spine_i.Placement = Placement(Vector(c3rad, 0, 0), ROT0)

DOC.recompute()

sweep_i = DOC.addObject("Part::Sweep", "sweep_int")
sweep_i.Sections = sec_i
sweep_i.Spine = spine_i
sweep_i.Solid = True

DOC.recompute()

tube_shape = sweep_e.Shape.cut(sweep_i.Shape)

tube = DOC.addObject("Part::Feature", "tube")
tube.Shape = tube_shape.copy()
tube.Placement = Placement(Vector(0, c1rad * 2.5, 0), ROT0)

sec_y_disp = c1rad * 5.0

sec_tube = tube_shape.copy()
sec_tube.Placement = Placement(Vector(0, sec_y_disp, 0), ROT0)

sec_dim = c3rad * 2.1 + c1rad * 2.1

cut_pos = sec_y_disp + (0.00 * c1rad)

section = Part.makeBox(sec_dim, c1rad * 2.1, sec_dim)
section.Placement = Placement(Vector(c1rad * -1.05, cut_pos, sec_dim * -0.5), ROT0)

# Part.show(section, "cutting shape")

sect_tube = DOC.addObject("Part::Feature", "tube_section")
sect_tube.Shape = sec_tube.cut(section).removeSplitter()

DOC.recompute()

setview()

