#
"""ext-full.py

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

def reg_poly(center=Vector(0, 0, 0), sides=6, dia=6,
             align=0, outer=1):
    """
    This return a polygonal shape

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
    polyg = reg_poly(Vector(0, 0, 0), 6, dia, 0, 0)

    nut = DOC.addObject("Part::Feature", nome + "_dado")
    nut.Shape = polyg.extrude(Vector(0, 0, spess))

    return nut


def estr_comp(nome, spess):
    vertex = ((-2,0,0), (-1, 2, 0), (1, 2, 0), (1, 0, 0),
              (0, -2, 0), (-2,0,0))

    obj = Part.makePolygon(vertex)
    wire = Part.Wire(obj)
    poly_f = Part.Face(wire)

    cexsh = DOC.addObject("Part::Feature", nome)
    cexsh.Shape = poly_f.extrude(Vector(0, 0, spess))
    
    return cexsh


# definizione oggetti

dado("Dado", 5.5, 10)

#estr_comp("complesso", 10)

setview()

