#
"""aereo.py

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

def cubo(nome, lung, larg, alt, cent = False, off_z = 0):
    obj_b = DOC.addObject("Part::Box", nome)
    obj_b.Length = lung
    obj_b.Width = larg
    obj_b.Height = alt
    
    if cent == True:
        posiz = Vector(lung * -0.5, larg * -0.5, off_z)
    else:
        posiz = Vector(0, 0, off_z)

    obj_b.Placement = FreeCAD.Placement(
        posiz, 
        FreeCAD.Rotation(0, 0, 0),
        FreeCAD.Vector(0,0,0)
        )

    DOC.recompute()

    return obj_b


def base_cyl(nome, ang, rad, alt ):
    obj = DOC.addObject("Part::Cylinder", nome)
    obj.Angle = ang
    obj.Radius = rad
    obj.Height = alt
    
    DOC.recompute()

    return obj   

def sfera(nome, rad):
    obj = DOC.addObject("Part::Sphere", nome)
    obj.Radius = rad
    
    DOC.recompute()

    return obj   


def mfuse_obj(nome, objs):
    obj = DOC.addObject("Part::MultiFuse", nome)
    obj.Shapes = objs
    obj.Refine = True
    DOC.recompute()

    return obj


def aeroplano():

    lung_fus = 30
    diam_fus = 5
    ap_alare = lung_fus * 1.75
    larg_ali = 7.5
    spess_ali = 1.5   
    alt_imp = diam_fus * 3.0
    pos_ali = (lung_fus*0.70)
    off_ali = (pos_ali- (larg_ali * 0.5))

    obj1 = base_cyl('primo cilindro', 360, diam_fus, lung_fus)

    obj2 = cubo('ali', ap_alare, spess_ali, larg_ali, True, off_ali)

    obj3 = sfera("naso", diam_fus)
    obj3.Placement = FreeCAD.Placement(Vector(0,0,lung_fus), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

    obj4 = cubo('impennaggio', spess_ali, alt_imp, larg_ali, False, 0)
    obj4.Placement = FreeCAD.Placement(Vector(0,alt_imp * -1,0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

    objs = (obj1, obj2, obj3, obj4)

    obj = mfuse_obj("Forma esempio", objs)
    obj.Placement = FreeCAD.Placement(Vector(0,0,0), FreeCAD.Rotation(0,0,-90), Vector(0,0,pos_ali))

    DOC.recompute()

    return obj


aeroplano()

setview()
