#
"""rif-cost.py

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

    rot_c = VZOR # Rotation center
    rot = ROT0 # Rotation angles
    obj_b.Placement = FreeCAD.Placement( posiz, rot, rot_c)

    DOC.recompute()

    return obj_b


def base_cyl(nome, ang, rad, alt ):
    obj = DOC.addObject("Part::Cylinder", nome)
    obj.Angle = ang
    obj.Radius = rad
    obj.Height = alt
    
    DOC.recompute()

    return obj   

# definizione oggetti

obj1 = cubo("cubo_cyl", 10, 20, 10, True, 10)
obj2 = base_cyl("cilindro", 360, 2.5, 15 )

print("Cubo Base = ", obj1.Placement) 
print("Cilindro = ", obj2.Placement) 

setview()
