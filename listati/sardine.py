#
"""sardine.py

   This code was written as an sample code 
   for "FreeCAD Scripting Guide" 
     
   Author: Carlo Dormeletti
   Copyright: 2020
   Licence: CC BY-NC-ND 4.0 IT 
"""

import os
import sys
import importlib

import FreeCAD
from FreeCAD import Base, Vector
import Part
from math import pi, sin, cos

scripts_path = os.path.join(os.path.dirname(__file__),)
sys.path.append(scripts_path)

import GfcMod as GFC
importlib.reload(GFC)

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

    FreeCAD.Gui.activeDocument().activeView().viewAxometric()
    FreeCAD.Gui.activeDocument().activeView().setAxisCross(True)
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")


if DOC is None:
    FreeCAD.newDocument(DOC_NAME)
    FreeCAD.setActiveDocument(DOC_NAME)
    DOC = FreeCAD.activeDocument()

else:

    clear_doc()


# EPS= tolerance to uset to cut the parts
EPS = 0.10
EPS_C = EPS * -0.5


def sardine(nome, lung, prof, alt, raggio, spess):
    """sardine
        crea una geometria a forma di scatola di sardine

        Keywords Arguments:
        nome   = nome della geometria finale
        lung   = lunghezza della scatola, lungo l'asse X
        larg   = larghezza della scatole, lungo l'asse Y
        alt    = altezza della scatola, lungo l'asse Z
        raggio = raggio dello "stondamendo" della scatola
        spess  = spessore della scatola 
    """
    
    obj = GFC.cubo_stondato(
        DOC, nome + "_est", lung, prof, alt, raggio, 0.0)

    lung_int = lung - (spess * 2)
    prof_int = prof - (spess * 2)
    alt_int = alt + EPS - spess
    raggio_int = raggio - spess

    obj_int = GFC.cubo_stondato(
        DOC, nome + "_int",
        lung_int, prof_int, alt_int, raggio_int, spess)

    obj_f = DOC.addObject("Part::Cut", nome)
    obj_f.Base = obj
    obj_f.Tool = obj_int
    obj_f.Refine = True
    DOC.recompute()

    return obj_f

sardine("scatola", 30, 20, 10, 5, 1)

setview()
