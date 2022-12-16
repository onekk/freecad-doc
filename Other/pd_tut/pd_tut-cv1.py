"""Script to replicate Part Design Tutorial Example.

https://wiki.freecadweb.org/Basic_Part_Design_Tutorial

This code was written as an sample code

Name: 20221013-pdtut-cv1.py

Author: Carlo Dormeletti
Copyright: 2022
Licence: CC BY-NC-ND 4.0

"""
import os  #noqa

import FreeCAD  # noqa
import FreeCADGui  # noqa
import Sketcher
import Part

from FreeCAD import Placement, Rotation, Vector  # noqa


def activate_doc(doc_name):
    """Activate a specific document."""
    FreeCAD.setActiveDocument(doc_name)
    FreeCAD.ActiveDocument = FreeCAD.getDocument(doc_name)
    FreeCADGui.ActiveDocument = FreeCADGui.getDocument(doc_name)
    print(f"Document: {doc_name} activated")


def clear_doc(doc_name):
    """Clear the document deleting all the objects."""
    doc = FreeCAD.getDocument(doc_name)
    for obj in doc.Objects:

        try:
            doc.removeObject(obj.Name)
        except Exception:
            pass


def setview(doc):
    """Rearrange View."""
    try:
        doc_v = FreeCAD.Gui.activeView()
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        doc_v.viewAxometric()
    except Exception:
        pass


def check_exist(doc_name):
    """Check the existence of a FC document named doc_name.

    If it not exist create one.
    """
    try:
        doc = FreeCAD.getDocument(doc_name)
    except NameError:
        doc = FreeCAD.newDocument(doc_name)

    return doc


# CODE start here

# Some methods to ease the work


def createPDBody(doc, bodyname, lcs=False):
    """Create new Part Design Body."""
    newBody = doc.addObject("PartDesign::Body", bodyname)

    if lcs is True:
        # add an LCS at the root of the Part, and attach it to the 'Origin'
        lcs0 = newBody.newObject('PartDesign::CoordinateSystem', 'LCS_0')
        lcs0.Support = [(newBody.Origin.OriginFeatures[0], '')]
        lcs0.MapMode = 'ObjectXY'
        lcs0.MapReversed = False

    newBody.recompute()
    doc.recompute()
    return newBody


def sketchPolyLine(vertexList, closed=True, addHVConstraints=True):
    """Create a polylin."""
    geoList = []
    conList = []
    npts = len(vertexList)
    for i in range(npts - 1):
        geoList.append(Part.LineSegment(vertexList[i], vertexList[i + 1]))

    if closed:
        geoList.append(Part.LineSegment(vertexList[-1], vertexList[0]))

    for i in range(npts - 1):
        conList.append(Sketcher.Constraint('Coincident', i, 2, i + 1, 1))

    if closed:
        conList.append(Sketcher.Constraint('Coincident', npts - 1, 2, 0, 1))

    if addHVConstraints:
        for i, ls in enumerate(geoList):
            if abs(ls.tangent(0)[0].y) < 1e-14:
                conList.append(Sketcher.Constraint('Horizontal', i))
            elif abs(ls.tangent(0)[0].x) < 1e-14:
                conList.append(Sketcher.Constraint('Vertical', i))

    return (geoList, conList)


def make_master_sketch(doc, bd_name, sk_name, l1, h1, dim_const=True):
    """Make rectangular sketch."""
    sk = doc.getObject(bd_name).newObject('Sketcher::SketchObject', sk_name)

    p1 = Vector(0, 0, 0)
    p2 = Vector(l1, 0, 0)
    p3 = Vector(l1, h1, 0)
    p4 = Vector(0, h1, 0)
    geoList, conList = sketchPolyLine([p1, p2, p3, p4])
    (line0, line1, line2, line3) = sk.addGeometry(geoList, False)
    sk.addConstraint(conList)
    sk.addConstraint(Sketcher.Constraint('Symmetric', 0, 1, 0, 2, -1, 1))

    if dim_const is True:
        con_num = sk.ConstraintCount

        sk.addConstraint(
            Sketcher.Constraint('DistanceX', line2, 1, line2, 2, l1))
        sk.addConstraint(
            Sketcher.Constraint('DistanceY', line1, 2, line1, 1, h1))
        sk.renameConstraint(con_num, u'length')
        sk.renameConstraint(con_num + 1, u'width')

    sk.recompute()

    return sk


def make_sk1(doc, bd_name, sk_name):
    """Make sketch 1."""
    sk = doc.getObject(bd_name).newObject('Sketcher::SketchObject', sk_name)
    sk.MapMode = 'FlatFace'
    sk.Support = (doc1.getObject('YZ_Plane'), [''])

    # Lengths
    h1 = 26.00
    l1 = 10.00  # fake value we assign it later
    l2 = 5.00

    # we draw it using counterclockwise order

    p1 = Vector(0, 0, 0)
    p2 = Vector(0, h1, 0)
    p3 = Vector(-l2, h1, 0)
    p4 = Vector(-l1, 0, 0)
    geoList, conList = sketchPolyLine([p1, p2, p3, p4])
    (line0, line1, line2, line3) = sk.addGeometry(geoList, False)

    # line2 end point on X axis
    conList.append(Sketcher.Constraint('PointOnObject', line2, 2, -1))
    # line0 end point on Y axis
    conList.append(Sketcher.Constraint('PointOnObject', line0, 2, -2))

    sk.addConstraint(conList)

    # dimensional constraints (putting in conList fails!?)
    sk.addConstraint(Sketcher.Constraint('DistanceY', line0, 1, line0, 2, h1))
    sk.addConstraint(Sketcher.Constraint('DistanceX', line1, 1, line1, 2, -l2))

    # fake value as expression in working as is
    cont_n = sk.addConstraint(Sketcher.Constraint('DistanceX', line2, 2, line0, 1, 20.836079)) 
    sk.setExpression(f'Constraints[{cont_n}]', u'<<master_sketch>>.Constraints.width')

    sk.recompute()
    return sk


def make_sk2(doc, bd_name, sk_name):
    """Make sketch 2."""
    sk = doc.getObject(bd_name).newObject('Sketcher::SketchObject', sk_name)
    sk.MapMode = 'FlatFace'
    sk.Support = (doc1.getObject('XZ_Plane'), [''])

    l1 = 5.00
    l2 = 11.00
    h1 = 26  # fake
    w1 = 26.5  # fake


    p1 = Vector(-w1, h1, 0)
    p2 = Vector(-w1 + l2, h1, 0)
    p3 = Vector(-w1 + l2, h1 - l1, 0)
    p4 = Vector(-w1, h1 - l1, 0)
    geoList, conList = sketchPolyLine([p1, p2, p3, p4])
    (line0, line1, line2, line3) = sk.addGeometry(geoList, False)
    sk.addExternal("master_sketch", "Edge3")  # id -3
    sk.addExternal("sketch_1", "Edge3")  # id  -4

    # ext references
    conList.append(Sketcher.Constraint('PointOnObject', -3, 1, line3))
    conList.append(Sketcher.Constraint('PointOnObject', -4, 1, line0))
    sk.addConstraint(conList)
    # dimensional constraints (putting in conList fails!?)
    sk.addConstraint(Sketcher.Constraint('DistanceY', line3, 1, line3, 2, l1))
    sk.addConstraint(Sketcher.Constraint('DistanceX', line0, 1, line0, 2, l2))

    sk.recompute()
    return sk


def make_sk3(doc, bd_name, sk_name):
    """Make sketch 3."""
    sk = doc.getObject(bd_name).newObject('Sketcher::SketchObject', sk_name)
    sk.MapMode = 'FlatFace'
    sk.Support = (doc1.getObject('XZ_Plane'), [''])

    l1 = 16.7
    l2 = 7
    w1 = 26.5  # fake

    p1 = Vector(-w1, l1, 0)
    p2 = Vector(-w1 + l2, l1, 0)
    p3 = Vector(-w1 + l2, 0, 0)
    p4 = Vector(-w1, 0, 0)

    geoList, conList = sketchPolyLine([p1, p2, p3, p4])
    (line0, line1, line2, line3) = sk.addGeometry(geoList, False)
    sk.addExternal("master_sketch", "Edge2")  # id -3

    # ext reference
    conList.append(Sketcher.Constraint('Coincident', -3, 1, line3, 1))
    sk.addConstraint(conList)
    sk.addConstraint(Sketcher.Constraint('DistanceY', line1, 2, line1, 1, l1))
    sk.addConstraint(Sketcher.Constraint('DistanceX', line0, 1, line0, 2, l2))
    sk.recompute()

    return sk


def make_sk4(doc, bd_name, sk_name):
    """Make sketch 4."""
    sk = doc.getObject(bd_name).newObject('Sketcher::SketchObject', sk_name)
    sk.MapMode = 'FlatFace'
    sk.Support = (doc1.getObject('YZ_Plane'), [''])

    d1 = 7
    d2 = 17
    p1 = Vector(-11, 19, 0)  # fake approx
    p2 = Vector(-22, 5, 0)  # fake approx
    p3 = Vector(0, 5, 0)  # fake approx
    p4 = Vector(0, 19, 0)  # fake approx

    geoList, conList = sketchPolyLine([p1, p2, p3, p4], closed=True)
    (line0, line1, line2, line3) = sk.addGeometry(geoList, False)
    sk.addExternal('sketch_1', 'Edge3')

    # ext references
    conList.append(Sketcher.Constraint('PointOnObject', 0, 1, -3))
    conList.append(Sketcher.Constraint('PointOnObject', 1, 1, -3))
    # yaxis
    conList.append(Sketcher.Constraint('PointOnObject', -1, 1, 2))
    sk.addConstraint(conList)
    sk.addConstraint(Sketcher.Constraint('Distance', -3, 2, line0, 2, d1))
    sk.addConstraint(Sketcher.Constraint('Distance', line0, 2, line0, 1, d2))
    sk.recompute()

    return sk


# Create the document
DOC1_NAME = 'pd_tut_cv1'

doc1 = check_exist(DOC1_NAME)
clear_doc(DOC1_NAME)
activate_doc(DOC1_NAME)


bd1_name = 'body1'
# We need a body where to place the Features
pd1 = createPDBody(doc1, bd1_name)


# Build sketches
master_sk_name = "master_sketch"
master_sketch = make_master_sketch(doc1, bd1_name, master_sk_name, 55.00, 26.00)
master_sketch.Visibility = False


sk1_name = 'sketch_1'

sk1 = make_sk1(doc1, bd1_name, sk1_name)
sk1.Visibility = False
sk1.recompute()


# First pad
pa1 = pd1.newObject('PartDesign::Pad', 'pad1')
pa1.Type = u"Length"
# pa1.AlongSketchNormal = True
pa1.Midplane = True
pa1.Profile = sk1
pa1.setExpression('Length', u'master_sketch.Constraints.length')

pa1.recompute()

sk2_name = 'sketch_2'
sk2 = make_sk2(doc1, bd1_name, sk2_name)
sk2.Visibility = False

"""
# First pocket
pk1 = pd1.newObject('PartDesign::Pocket', 'pocket1')
pk1.Type = u'ThroughAll'
pk1.Profile = sk2
# pk1.AlongSketchNormal = True
pk1.Reversed = True
pd1.recompute()


sk3_name = 'sketch_3'
sk3 = make_sk3(doc1, bd1_name, sk3_name)
sk3.Visibility = False


# Second pad
pa2 = pd1.newObject('PartDesign::Pad', 'pad2')
pa2.Type = u"Length"
# pa2.AlongSketchNormal = True
pa2.Profile = sk3
pa2.setExpression('Length', u'master_sketch.Constraints.width')

# Mirror fisrt pocket and second pad
pa3 = pd1.newObject('PartDesign::Mirrored', 'Mirrored_Pad')
pa3.Originals = [pk1, pa2]
pa3.MirrorPlane = (doc1.getObject('YZ_Plane'), [''])
pa3.Refine = True
pa3.recompute()

pd1.Tip = pa3
pd1.recompute()


sk4_name = 'sketch_4'
sk4 = make_sk4(doc1, bd1_name, sk4_name)
sk4.Visibility = False


# Final pocket
pk2 = pd1.newObject('PartDesign::Pocket', 'pocket1')
pk2.Type = u'Length'
pk2.Profile = sk4
pk2.Midplane = True
# pk2.AlongSketchNormal = True
pk2.Length = 17
pk2.Refine = True
"""

doc1.recompute()

setview(doc1)
