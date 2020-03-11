#
"""rev-full.py

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

# EPS= tolerance to use to cut the parts
EPS = 0.10
EPS_C = EPS * -0.5

def reg_poly(center=Vector(0, 0, 0), sides=6, dia=6,
             align=0, outer=1):
    """
    This return a polygonal face

    Keywords Arguments:
        center   - Vector holding the center of the polygon
        sides    - the number of sides
        dia      - the diameter of the base circle 
                     (aphotem or externa diameter)
        align    - 0 or 1 it try to align the base with one axis
        outer    - 0: aphotem 1: outer diameter (default 1)

    """

    ang_dist = pi / sides

    if align == 0:
        theta = 0.0
    else:
        theta = ang_dist

    if outer == 1:
        rad = dia * 0.5
    else:
        # dia is the apothem, so calculate the radius
        # outer radius given the inner diameter
        rad = (dia / cos(ang_dist)) * 0.5 

    vertex = []

    for n_s in range(0, sides+1):
        vpx = rad * cos((2 * ang_dist * n_s) + theta) + center[0]
        vpy = rad * sin((2 * ang_dist * n_s) + theta) + center[1]
        vertex.append(Vector(vpx, vpy, 0))

    obj = Part.makePolygon(vertex)
    wire = Part.Wire(obj)
    poly_f = Part.Face(wire)
 
    return poly_f 


def dado(nome, dia, spess):
    poly_f = reg_poly(Vector(0, 0, 0), 6, dia, 0, 0)

    nut = DOC.addObject("Part::Feature", nome + "_dado")
    nut.Shape = poly_f.extrude(Vector(10, 5, spess))

    return nut


def point(nome, pos, pt_r = 0.25, color = (0.85, 0.0, 0.00),
        tr = 0):  
    """draw a point for reference"""
    rot_p = DOC.addObject("Part::Sphere", nome)
    rot_p.Radius = pt_r
    rot_p.Placement = FreeCAD.Placement(
        pos, FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    rot_p.ViewObject.ShapeColor = color
    rot_p.ViewObject.Transparency = tr

    DOC.recompute()

    return rot_p


def manico(nome):
    """Revolve a face"""
    face = reg_poly(Vector(0, 0, 0), 6, 5.5, 0, 0)
    # base point of the rotation axis
    pos = Vector(0,10,0)
    # direction of the rotation axis
    vec = Vector(1,0,1)
    angle = 360 # Rotation angle

    point("punto_rot", pos)

    obj = DOC.addObject("Part::Feature", nome)
    obj.Shape = face.revolve(pos, vec, angle)

    DOC.recompute()

    return obj

# definizione oggetti

manico("Manico")

setview()

