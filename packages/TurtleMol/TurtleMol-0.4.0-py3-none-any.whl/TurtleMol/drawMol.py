'''
These functions are used to repeat a pattern of a given molecule or molecules. 
The goal is to repeat the pattern exactly the specified number of times
within the constraints of a the defined shape. 
A 'Fill' option was also added so that one could just define a space,
and fill said space with provided structure as many times as it can fit.
'''

import math
from .Box3D import Box3d, drawBox
from .Sphere3D import Sphere3d
from .mesh3D import mesh3D
from .shiftBox import atomsFillBox, atomsRandBox, \
                     moleculesFillBox, moleculesRandBox
from .shiftSphere import atomFillSphere, atomRandSphere, \
                        moleculeRandSphere, moleculeFillSphere
from .shiftMesh import atomsFillMesh, moleculesFillMesh, atomsRandMesh, moleculesRandMesh
from .setAtomProp import setAtomicRadius
from .makeStruc import makeBase, shiftPoints
from .shiftDensity import placeMols
from .shiftUnitCell import unitCellBox, unitCellMesh, unitCellSphere
from .shiftHexagon import hexagonUnitCellBox, hexagonUnitCellSphere, hexagonUnitCellMesh

def drawMolBox(struc, baseStruc, iparams):
    '''Utilized to place molecules in a box'''
    dims = drawBox(iparams)
    box = Box3d(0, 0, 0, dims)
    radii = setAtomicRadius(iparams['atomRadius'])
    numMol = iparams['numMolecules']
    tol = float(iparams['tol'])

    originalPoints = makeBase(struc)

    originalPoints = shiftPoints(originalPoints, box)

    if iparams['unitCell']:
        if iparams['hexagonal'] == False:
            filled, strucType, cellParams = unitCellBox(box, dims, iparams['unitCell'], iparams['angle'],
                                            originalPoints, radii, iparams['rotAngles'])
            return filled, strucType, cellParams
        else:
            filled, strucType, cellParams = hexagonUnitCellBox(box, dims, iparams['unitCell'],
                                            originalPoints, radii)
            return filled, strucType, cellParams

    if iparams['density']:
        filled, strucType = placeMols(box, originalPoints, iparams['density'],
                                 tol, "box", radii, iparams['randomizeOrient'], iparams['rotAngles'])
        return filled, strucType

    if not isinstance(numMol, int) and str(numMol).lower() != "fill":
        numMol = int(numMol)

    if iparams['randFill'] == 'False' or iparams['randFill'] is False:
        numXShifts = math.ceil(float(box.length) / float(tol))
        numYShifts = math.ceil(float(box.height) /float( tol))
        numZShifts = math.ceil(float(box.width)/ float(tol))

        # Check if structure is monatomic or molecule
        if len(originalPoints) == 1:
            filledAtom = atomsFillBox(numXShifts, numYShifts, numZShifts,
                                      tol, originalPoints, box, radii, numMol)
            return list(filledAtom), "atom"

        if len(originalPoints) > 1:
            filledAtom = moleculesFillBox(numXShifts, numYShifts, numZShifts,
                                          tol, originalPoints, box, radii, baseStruc,
                                          iparams['randomizeOrient'], numMol, iparams['rotAngles'])
            return list(filledAtom), "molecule"

    elif iparams['randFill'] == 'True' or iparams['randFill'] is True:
        # Check if structure is monatomic or molecule
        if len(originalPoints) == 1:
            filledAtom = atomsRandBox(numMol, iparams['maxAttempts'],
                                          originalPoints, box, radii, tol)
            return list(filledAtom), "atom"

        if len(originalPoints) > 1:
            filledAtom = moleculesRandBox(numMol, iparams['maxAttempts'],
                                              originalPoints, box, radii, tol, baseStruc,
                                              iparams['randomizeOrient'], iparams['rotAngles'])
            return list(filledAtom), "molecule"

    return "ERROR", "No atoms found"

def drawMolSphere(struc, baseStruc, iparams):
    '''Utilized to place molecules in a sphere'''
    sphere = Sphere3d(float(iparams['sphereCenter'][0]), float(iparams['sphereCenter'][1]),
                      float(iparams['sphereCenter'][2]), float(iparams['radius']))
    radii = setAtomicRadius(iparams['atomRadius'])
    numMol = iparams['numMolecules']
    tol = float(iparams['tol'])

    originalPoints = makeBase(struc)
    originalPoints = shiftPoints(originalPoints, sphere)

    if iparams['unitCell']:
        if iparams['hexagonal'] == False:
            filled, strucType, cellParams = unitCellSphere(sphere, iparams['unitCell'], iparams['angle'],
                                            originalPoints, radii, iparams['rotAngles'])
            return filled, strucType, cellParams
        else:
            filled, strucType, cellParams = hexagonUnitCellSphere(sphere, iparams['unitCell'],
                                            originalPoints, radii)
            return filled, strucType, cellParams

    if iparams['density']:
        filled, strucType = placeMols(sphere, originalPoints, iparams['density'],
                                 tol, "sphere", radii, iparams['randomizeOrient'], iparams['rotAngles'])
        return filled, strucType

    if not isinstance(numMol, int) and str(numMol).lower() != "fill":
        numMol = int(numMol)

    if iparams['randFill'] == 'False' or iparams['randFill'] is False:
        numShifts = math.ceil(2*sphere.radius / tol)

        # Check if structure is monatomic or molecule
        if len(originalPoints) == 1:
            filledAtom = atomFillSphere(numShifts, sphere,
                                        originalPoints, radii, tol,
                                        numMol)
            return list(filledAtom), "atom"

        if len(originalPoints) > 1:
            filledAtom = moleculeFillSphere(numShifts, sphere,
                                            originalPoints, radii, tol, baseStruc,
                                            iparams['randomizeOrient'], numMol, iparams['rotAngles'])
            return list(filledAtom), "molecule"

    elif iparams['randFill'] == 'True' or iparams['randFill'] is True:
        # Check if structure is monatomic or molecule
        if len(originalPoints) == 1:
            filledAtom = atomRandSphere(numMol, iparams['maxAttempts'],
                                            originalPoints, sphere, radii, tol)
            return list(filledAtom), "atom"

        if len(originalPoints) > 1:
            filledAtom = moleculeRandSphere(numMol, iparams['maxAttempts'],
                                                originalPoints, sphere, radii, tol, baseStruc,
                                                iparams['randomizeOrient'], iparams['rotAngles'])
            return list(filledAtom), "molecule"

    return "ERROR: No atoms found"

def drawMolMesh(struc, baseStruc, iparams):
    '''Places molecules in a mesh'''
    mesh = mesh3D(iparams['mesh'], iparams['meshScale'], iparams['scaleX'], iparams['scaleY'], iparams['scaleZ'])
    radii = setAtomicRadius(iparams['atomRadius'])
    numMol = iparams['numMolecules']
    tol = float(iparams['tol'])

    originalPoints = makeBase(struc)

    if iparams['unitCell']:
        if iparams['hexagonal'] == False:
            filled, strucType, cellParams = unitCellMesh(mesh, iparams['unitCell'], iparams['angle'],
                                            originalPoints, radii, iparams['rotAngles'])
            return filled, strucType, cellParams
        else:
            filled, strucType, cellParams = hexagonUnitCellMesh(mesh, iparams['unitCell'],
                                            originalPoints, radii)
            return filled, strucType, cellParams

    if iparams['density']:
        filled, strucType = placeMols(mesh, originalPoints, iparams['density'],
                                 tol, "mesh", radii, iparams['randomizeOrient'], iparams['rotAngles'])
        return filled, strucType

    if not isinstance(numMol, int) and str(numMol).lower() != "fill":
        numMol = int(numMol)

    if iparams['randFill'] == 'False' or iparams['randFill'] is False:
        if len(originalPoints) == 1:
            filledAtom = atomsFillMesh(mesh, originalPoints, tol, radii, numMol)

            return list(filledAtom), 'atom'
        else:
            if iparams['onSurface'] == True:
                filledMol = moleculesFillMesh(mesh, originalPoints, tol,
                                          radii, numMol, baseStruc, iparams['randomizeOrient'], iparams['rotAngles'],
                                          onSurface=True)
            elif iparams['alignNormal'] == True:
                filledMol = moleculesFillMesh(mesh, originalPoints, tol,
                                          radii, numMol, baseStruc, iparams['randomizeOrient'], iparams['rotAngles'],
                                          alignNormal=True)
            else:
                filledMol = moleculesFillMesh(mesh, originalPoints, tol,
                                          radii, numMol, baseStruc, iparams['randomizeOrient'], iparams['rotAngles'])
            
            return list(filledMol), 'molecule'

    elif iparams['randFill'] == 'True' or iparams['randFill'] is True:
        if len(originalPoints) == 1:
            filledAtom = atomsRandMesh(mesh, originalPoints, tol, radii, numMol,
                                       iparams['maxAttempts'])
            return list(filledAtom), 'atom'
        else:
            filledMol = moleculesRandMesh(mesh, originalPoints, tol, radii, numMol,
                                          baseStruc, iparams['randomizeOrient'], iparams['rotAngles'],
                                          iparams['maxAttempts'])
            return list(filledMol), 'molecule'
