'''Module places molecules in a box'''

import random
import numpy as np
from .isOverlap import isOverlapAtomKDTree, isOverlapMoleculeKDTree, buildKDTreeMapping
from .makeStruc import makeBase, reCenter, Reorient

def atomsFillBox(x, y, z, tol, og, box, radii, numMol):
    '''Fills box with single atoms'''
    if str(numMol).lower() == 'fill':
        numMol = 10000000000000

    filledAtom = []

    # Create KD-tree for filledAtoms
    kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

    for zShift in range(z):
        for yShift in range(y):
            for xShift in range(x):
                for atom in og:
                    # Calculate the shift for each tile and new point
                    newX = box.xCoord + atom[1] + xShift
                    newY = box.yCoord + atom[2] + yShift
                    newZ = box.zCoord + atom[3] + zShift

                    # Adjust for atomic radiss
                    newXMin = newX - radii[atom[0]]
                    newYMin = newY - radii[atom[0]]
                    newZMin = newZ - radii[atom[0]]
                    newXMax = newX + radii[atom[0]]
                    newYMax = newY + radii[atom[0]]
                    newZMax = newZ + radii[atom[0]]

                    # Check if the new atom fits within the box
                    if inBox(newXMin, newXMax, newYMin, newYMax, newZMin, newZMax, box):
                        if len(atom) == 5:
                            newAtom = (atom[0], newX, newY, newZ, atom[4])
                        else:
                            newAtom = (atom[0], newX, newY, newZ)

                        if (kdTree is None or not isOverlapAtomKDTree(newAtom, kdTree, indexToAtom, radii, tol)) and \
                            numMol > len(filledAtom):
                            filledAtom.append(newAtom)

                            # Rebuild KDTree with newly added atoms
                            kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

    return filledAtom

def atomsRandBox(numMol, maxAttempts, og, box,
                     radii, tol):
    '''Places a defined number of single atoms in box'''
    filledAtom = []

    # Create KD-tree for filledAtoms
    kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

    attempts = 0

    while len(filledAtom) < numMol and attempts < maxAttempts:
        for atom in og:
            # Calculate the shift for each tile and new point
            newX = atom[1] + random.uniform(0, box.length)
            newY = atom[2] + random.uniform(0, box.width)
            newZ = atom[3] + random.uniform(0, box.height)
            # Adjust for atomic radiss
            newXMin = newX - radii[atom[0]]
            newYMin = newY - radii[atom[0]]
            newZMin = newZ - radii[atom[0]]
            newXMax = newX + radii[atom[0]]
            newYMax = newY + radii[atom[0]]
            newZMax = newZ + radii[atom[0]]
            # Check if the new atom fits within the box
            if  inBox(newXMin, newXMax, newYMin, newYMax, newZMin, newZMax, box):
                if len(atom) == 5:
                    newAtom = (atom[0], newX, newY, newZ, atom[4])
                else:
                    newAtom = (atom[0], newX, newY, newZ)

                if (kdTree is None or not isOverlapAtomKDTree(newAtom, kdTree, indexToAtom, radii, tol)):
                    filledAtom.append(newAtom)

                    # Rebuild KDTree with newly added atoms
                    kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

        attempts += 1

    return list(filledAtom)

def moleculesFillBox(x, y, z, tol, og, box, radii,
                     baseStruc, randOrient, numMol, rotAngles):
    '''Fills box with molecules'''
    filledAtom = []

    if str(numMol).lower() == 'fill':
        numMol = 10000000000000

    if baseStruc is not None:
        base = makeBase(baseStruc)
        filledAtom.append(reCenter(base, box))

    kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

    for zShift in range(z):
        for yShift in range(y):
            for xShift in range(x):
                newMol = []
                anyAtomOutside = False

                for atom in og:
                    # Calculate the shift for each tile and new point
                    newX = box.xCoord + atom[1] + xShift
                    newY = box.yCoord + atom[2] + yShift
                    newZ = box.zCoord + atom[3] + zShift

                    # Adjust for atomic radiss
                    newXMin = newX - radii[atom[0]]
                    newYMin = newY - radii[atom[0]]
                    newZMin = newZ - radii[atom[0]]
                    newXMax = newX + radii[atom[0]]
                    newYMax = newY + radii[atom[0]]
                    newZMax = newZ + radii[atom[0]]

                    # Check if the new atom fits within the box
                    if  inBox(newXMin, newXMax, newYMin, newYMax, newZMin,
                              newZMax, box):
                        if len(atom) == 5:
                            newAtom = (atom[0], newX, newY, newZ, atom[4])
                        else:
                            newAtom = (atom[0], newX, newY, newZ)
                        newMol.append(newAtom)

                    else:
                        anyAtomOutside = True

                if randOrient and len(newMol) == len(og):
                    newMol = Reorient(newMol, randRotate=True)

                if not np.allclose(np.array(rotAngles), np.array([0, 0, 0])) and len(newMol) == len(og):
                    newMol = Reorient(newMol, angles=rotAngles)

                if ((kdTree is None or not isOverlapMoleculeKDTree(newMol, kdTree, indexToAtom, radii, tol)) and
                    not anyAtomOutside and numMol > len(filledAtom)):

                    filledAtom.append(newMol)

                    # Rebuild KDTree with newly added atoms
                    kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

    return filledAtom

def moleculesRandBox(numMol, maxAttempts, og, box, radii, tol,
                         baseStruc, randOrient, rotAngles):
    '''Places a defined number of molecules in box'''
    filledAtom = []

    attempts = 0

    if baseStruc is not None:
        base = makeBase(baseStruc)
        filledAtom.append(reCenter(base, box))

    # Create KD-tree for filledAtoms
    kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)

    while len(filledAtom) < numMol and attempts < maxAttempts:
        newMol = []
        anyAtomOutside = False
        xShift = random.uniform(0, box.length)
        yShift = random.uniform(0, box.width)
        zShift = random.uniform(0, box.height)
        for atom in og:
            # Calculate the shift for each tile and new point
            newX = atom[1] + xShift
            newY = atom[2] + yShift
            newZ = atom[3] + zShift
            # Adjust for atomic radiss
            newXMin = newX - radii[atom[0]]
            newYMin = newY - radii[atom[0]]
            newZMin = newZ - radii[atom[0]]
            newXMax = newX + radii[atom[0]]
            newYMax = newY + radii[atom[0]]
            newZMax = newZ + radii[atom[0]]
            # Check if the new atom fits within the box
            if  inBox(newXMin, newXMax, newYMin, newYMax, newZMin, newZMax, box):
                if len(atom) == 5:
                    newAtom = (atom[0], newX, newY, newZ, atom[4])
                else:
                    newAtom = (atom[0], newX, newY, newZ)
                newMol.append(newAtom)
            else:
                anyAtomOutside = True

        if randOrient and len(newMol) == len(og):
                    newMol = Reorient(newMol, randRotate=True)

        if not np.allclose(np.array(rotAngles), np.array([0, 0, 0])) and len(newMol) == len(og):
            newMol = Reorient(newMol, angles=rotAngles)

        if (kdTree is None or not isOverlapMoleculeKDTree(newMol, kdTree, indexToAtom, radii, tol)) and not anyAtomOutside:
            filledAtom.append(newMol)

            # Rebuild KDTree with newly added atoms
            kdTree, indexToAtom = buildKDTreeMapping(filledAtom, radii)
        attempts += 1

    return list(filledAtom)

def inBox(xMin, xMax, yMin, yMax, zMin, zMax, box):
    '''Checks if atoms are fully in the box'''
    if (
        xMin >= box.xCoord and xMax <= box.xCoord + box.length and
        yMin >= box.yCoord and yMax <= box.yCoord + box.width and
        zMin >= box.zCoord and zMax <= box.zCoord + box.height
    ):
        return True
    return False
