#
"""brep-adv.py

   This code was written as an sample code 
   for "FreeCAD Scripting Guide" 
     
   Author: Carlo Dormeletti
   Copyright: 2020
   Licence: CC BY-NC-ND 4.0 IT 

   Attenzione: Questo listato va usato aggiungeno le linee 
   da 18 in poi al codice presente in sc-base.py

   Warning: This code has to be adding the lines starting
   from 18 to the code in sc-base.py
"""

def cubo_brep(nome, lung, larg, alt):
    h_lung = lung * 0.5
    h_larg = larg * 0.5

    vertex = (
    (h_lung * -1, h_larg * -1, 0),
    (h_lung * 1, h_larg * -1, 0),
    (h_lung * 1, h_larg * 1, 0),
    (h_lung * -1, h_larg * 1, 0),
    (h_lung * -1, h_larg * -1, 0))

    obj = Part.makePolygon(vertex)
    wire = Part.Wire(obj)
    poly_f = Part.Face(wire)

    cexsh = DOC.addObject("Part::Feature", nome)
    cexsh.Shape = poly_f.extrude(Vector(0, 0, alt))
    
    return cexsh


def forma_brep(nome, lung, larg, alt):
    h_lung = lung * 0.5
    h_larg = larg * 0.5
    vertex = (
        (h_lung * -1, h_larg * -1, 0),
        (h_lung * 1, h_larg * -1, 0),
        (h_lung * 1, h_larg * 1, 0),
        (h_lung * -1, h_larg * 1, 0),
        (h_lung * -1, h_larg * -1, 0))

    obj = Part.makePolygon(vertex)
    wire = Part.Wire(obj)
    
    hole = Part.makeCircle(1.5)
    h_wire = Part.Wire(hole)
    h_wire.reverse()

    h_wire1 = h_wire.copy()
    h_wire1.translate(Vector(3.5,0,0))

    h_wire2 = h_wire.copy()
    h_wire2.translate(Vector(-3.5,0,0))

    poly_f = Part.Face([wire,h_wire, h_wire1, h_wire2])

    cexsh = DOC.addObject("Part::Feature", nome)
    cexsh.Shape = poly_f.extrude(Vector(0, 0, alt))
    
    return cexsh

# definizione oggetti

forma_brep("cubo-brep", 20, 10, 15)

setview()

