#
"""sc-base.py

   This code was written as an sample code 
   for "FreeCAD Scripting Guide" 
     
   Author: Carlo Dormeletti
   Copyright: 2020
   Licence: CC BY-NC-ND 4.0 IT 
"""

import FreeCAD
from FreeCAD import Vector, Rotation
import Part
from math import pi, sin, cos

DOC_NAME = "Pippo"
CMPN_NAME = None


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


def clear_doc():
    """Clear the active document deleting all the objects"""
    for obj in DOC.Objects:
        DOC.removeObject(obj.Name)

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
#print("DOC : {0} GUI : {1}".format(DOC, GUI))
activate_doc()
#print(FreeCAD.ActiveDocument.Name)
clear_doc()

if CMPN_NAME is None:
    pass
else:
    DOC.addObject("App::DocumentObjectGroup", CMPN_NAME)

# EPS= tolerance to uset to cut the parts
EPS = 0.10
EPS_C = EPS * -0.5
VZOR = Vector(0, 0, 0)
ROT0 = Rotation(0, 0, 0)

# IL CODICE COMINCIA DA QUI
# MAIN CODE START HERE

