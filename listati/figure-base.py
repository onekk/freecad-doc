#
"""cubo-prova.py

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

def cubo(nome, lung, larg, alt):
    obj_b = DOC.addObject("Part::Box", nome)
    obj_b.Length = lung
    obj_b.Width = larg
    obj_b.Height = alt

    DOC.recompute()

    return obj_b

def base_cyl(nome, ang, rad, alt ):
    obj = DOC.addObject("Part::Cylinder", nome)
    obj.Angle = ang
    obj.Radius = rad
    obj.Height = alt
    
    DOC.recompute()

    return obj   


obj = cubo("cubo_di_prova", 5, 5, 5)
obj_1 = base_cyl("primo cilindro", 360, 2, 25)

setview()

