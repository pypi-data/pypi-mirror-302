'''Sets up the structure files'''
import random
import numpy as np
from .Box3D import Box3d
from .setAtomProp import setAtomicMass
from scipy.spatial.transform import Rotation as R

def makeBase(baseStruc):
    '''Convert dataframe to list of points'''
    atomBase = baseStruc['Atom'].values.tolist()
    xBase = baseStruc['X'].values.tolist()
    yBase = baseStruc['Y'].values.tolist()
    zBase = baseStruc['Z'].values.tolist()

    if 'Residue' not in baseStruc.columns:
        return [(atomBase[i], xBase[i], yBase[i], zBase[i]) for i in range(len(atomBase))]

    residue = baseStruc['Residue'].values.tolist()
    return [(atomBase[i], xBase[i], yBase[i], zBase[i], residue[i]) for i in range(len(atomBase))]

def calcCenter(coords):
    '''Calculate geometric center'''
    if not coords:
        return None

    numCoords = len(coords)
    centerX = sum(coord[1] for coord in coords) / numCoords
    centerY = sum(coord[2] for coord in coords) / numCoords
    centerZ = sum(coord[3] for coord in coords) / numCoords

    return (centerX, centerY, centerZ)

def reCenter(struc, shape):
    '''Set center structure coordiantes to center of shape'''
    currentCenter = calcCenter(struc)
    shapeCenter = shape.findCenter()
    displacement = (
        shapeCenter[0] - currentCenter[0],
        shapeCenter[1] - currentCenter[1],
        shapeCenter[2] - currentCenter[2]
    )
    newCoords = [(coord[0], coord[1] + displacement[0], coord[2] + displacement[1],
                coord[3] + displacement[2]) for coord in struc]

    return newCoords

def shiftPoints(points, shape):
    '''Sifts points to the bottom-left front corner of a 3D shape'''
    pointNames = [point[0] for point in points]
    coords = np.array([point[1:4] for point in points], dtype=float)

    if len(points[0]) == 5:
        pointRes = [point[4] for point in points]
    else:
        pointRes = None

    # Determine the bounds of the points
    minXPoints = np.min(coords[:, 0])
    minYPoints = np.min(coords[:, 1])
    minZPoints = np.min(coords[:, 2])

    # Calculate the translation required
    translation = np.array([
        shape.origin()[0] - minXPoints,
        shape.origin()[1] - minYPoints,
        shape.origin()[2] - minZPoints,
    ])

    # Shift the points
    shiftedCoords = coords + translation
    if pointRes:
        shiftedPoints = [[name] + coord.tolist() + [residue]
                         for name, coord, residue in
                         zip(pointNames, shiftedCoords, pointRes)]
    else:
        shiftedPoints = [[name] + coord.tolist()
                         for name, coord in zip(pointNames, shiftedCoords)]

    return shiftedPoints

def Reorient(mol, randRotate=False, angles=[0,0,0]):
    '''Reorients a molecule around geometric center'''
    if len(mol) == 0:
        return mol

    atomNames = [atom[0] for atom in mol]
    atomInfo = [atom[4:] if len(atom) > 4 else [] for atom in mol]
    points = np.array([atom[1:4] for atom in mol], dtype=np.float64)
    centroid = points.mean(axis=0) # Calculate center of points
    points -= centroid # Translate the points to origin

    # Perform the rotaton
    # Generate random rotation angles in radians
    if randRotate:
        thetaX = random.uniform(0, 2*np.pi)
        thetaY = random.uniform(0, 2*np.pi)
        thetaZ = random.uniform(0, 2*np.pi)
    else:
        thetaX = angles[0]
        thetaY = angles[1]
        thetaZ = angles[2]

    # Create the rotation matrix for the x-axis
    rx = np.array([[1, 0, 0],
                  [0, np.cos(thetaX), -np.sin(thetaX)],
                  [0, np.sin(thetaX), np.cos(thetaX)]],
                  dtype=np.float64)

    # Create rotation matrix for the y-axis
    ry = np.array([[np.cos(thetaY), 0, np.sin(thetaY)],
                  [0, 1, 0],
                  [-np.sin(thetaY), 0, np.cos(thetaY)]],
                  dtype=np.float64)

    # Create rotation matrix for the z-axis
    rz = np.array([[np.cos(thetaZ), -np.sin(thetaZ), 0],
                  [np.sin(thetaZ), np.cos(thetaZ), 0],
                  [0, 0, 1]],
                  dtype=np.float64)

    # Combined rotation matrix
    R = rz @ ry @ rx

    # Apply the rotation matrix to the points
    rotatedPoints = np.dot(points, R.T)

    # Translate the points back to position
    rotatedPoints += centroid

    rotatedAtoms = [tuple(name) + tuple(coord.tolist()) + tuple(info)
                    for name, coord, info in zip(atomNames, rotatedPoints, atomInfo)]

    rotatedAtoms = [tuple(atom) for atom in rotatedAtoms]

    return rotatedAtoms

def calcDensity(shape, mol):
    '''Calculates the density of a given structure'''
    vol = shape.volume() * 1e-24 # mL
    mass = 0
    atomicMass = setAtomicMass()  # g

    for atom in mol:
        mass += atomicMass[atom[0]]
    
    moles = mass # g

    return mass/vol # g/mL

def calcNumMol(shape, mol, density):
    '''
    Calulates the number of molecules needed in a box to match
    the defined density based off of the defined volume
    '''
    vol = shape.volume() # A^3
    rho = density # g/mL
    rho *= 1e-24 # g/A^3
    atomicMass = setAtomicMass() # g/mol
    molarMass = 0 
    for atom in mol:
        molarMass += atomicMass[atom[0]]
    
    numMol = (rho * 6.022e23 * vol)/molarMass # molecules

    return int(numMol)

def calcDistance(shape, mol, density, shapeType):
    '''
    Calculates the distance between molecules for the correct density
    '''
    if str(shapeType).lower() == "box":
        x, y, z = shape.length, shape.width, shape.height

        numMol = calcNumMol(shape, mol, density)

        # Calculate the molecules to place in each dimension
        pointsPerDimension = round(numMol ** (1/3))

        # Generate grid points
        XCount = np.linspace(0, x, pointsPerDimension, endpoint=False)
        YCount = np.linspace(0, y, pointsPerDimension, endpoint=False)
        ZCount = np.linspace(0, z, pointsPerDimension, endpoint=False)

        # Create a meshgrid and reshape it to get coordiantes
        xx, yy, zz = np.meshgrid(XCount, YCount, ZCount, indexing='ij')
        coords = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T

        return coords[:numMol].tolist()
    
    elif str(shapeType).lower() == "sphere":

        def insideSphere(x, y, z, radius):
            return x**2 + y**2 + z**2 <= radius**2

        r = shape.radius

        # Create cubic geometry to enclose the sphere
        cubeSide = 2*r

        box = Box3d(0, 0, 0, [cubeSide, cubeSide, cubeSide])

        numMol = calcNumMol(box, mol, density)

        # Calculate total points in the cube
        totalPoints = round(numMol ** (1/3))

        # Generate points within cube
        XCount = np.linspace(-r, r, int(totalPoints**(1/3)))
        YCount = np.linspace(-r, r, int(totalPoints**(1/3)))
        ZCount = np.linspace(-r, r, int(totalPoints**(1/3)))

        # Create meshgrid and reshape to get coordinates
        xx, yy, zz = np.meshgrid(XCount, YCount, ZCount, indexing='ij')
        coords = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T

        # Find points inside sphere
        insidePoints = [point for point in coords if insideSphere(*point, r)]
        
        return insidePoints[:numMol]
    
    elif str(shapeType).lower() == 'mesh':
        # Determine bounds of mesh
        bounds = shape.bounds
        minBound, maxBound = bounds[0], bounds[1]

        numMol = calcNumMol(shape, mol, density)

        # Calculate the molecules to place in each dimension
        pointsPerDimension = round(numMol ** (1/3))

        # Generate grid points
        XCount = np.linspace(minBound[0], maxBound[0], pointsPerDimension, endpoint=False)
        YCount = np.linspace(minBound[1], maxBound[1], pointsPerDimension, endpoint=False)
        ZCount = np.linspace(minBound[2], maxBound[2], pointsPerDimension, endpoint=False)

        # Create a meshgrid and reshape it to get coordiantes
        xx, yy, zz = np.meshgrid(XCount, YCount, ZCount, indexing='ij')
        coords = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T

        # Find points inside sphere
        insidePoints = [point for point in coords if shape.isInside(point)]

        return insidePoints[:numMol]
    
def applyGlobalTransform(data, matrix):
    '''Applies the global transformation to atom coordinates'''

    # Compute original centroid
    ogCentroid = computeCentroid(data)

    # Get Transformation Vector from Matrix
    transVector = matrix[:3, 3]

    # Compute Translation Vector
    transVector = transVector - np.array(ogCentroid)

    # Apply the translation to all atoms
    transformed = applyTranslation(data, transVector)
    
    return transformed

def computeCentroid(atoms):
    '''Computes the centroid of a set of atoms'''
    coords = np.array([atom[1:4] for atom in atoms])
    centroid = np.mean(coords, axis = 0)
    return centroid.tolist()

def applyTranslation(atoms, transVector, strucType='atom'):
    '''Applies the translation vector to all atoms'''
    translated = []
    if strucType == 'atom':
        for atom in atoms:
            translatedCoords = (np.array(atom[1:4]) + transVector).tolist()
            if len(atom) == 4:
                translated.append([atom[0]] + translatedCoords)
            elif len(atom) == 5:
                translated.append([atom[0]] + translatedCoords + [atom[4]])
    elif strucType == 'molecule':
        for mol in atoms:
            newMol = []
            for atom in mol:
                translatedCoords = (np.array(atom[1:4]) + transVector).tolist()
                if len(atom) == 4:
                    newMol.append([atom[0]] + translatedCoords)
                elif len(atom) == 5:
                    newMol.append([atom[0]] + translatedCoords + [atom[4]])
            translated.append(newMol)
    return translated

def findMinPoint(mols):
    '''Finds the minimum point of the total structure'''
    coords = np.array([atom[1:4] for mol in mols for atom in mol])
    minPoint = np.min(coords, axis=0)
    return minPoint

def calcLatticeVectors(a, b, c, alpha, beta, gamma):
    '''Calculates the lattice vectors for a unit cell'''
    # Convert angle from degrees to radians
    alphaRad = np.radians(alpha)
    betaRad = np.radians(beta)
    gammaRad = np.radians(gamma)

    # Lattice Vector a (points along x-axis)
    aVec = np.array([a, 0, 0])

    # Lattice Vector b (points along y-axis)
    bVec = np.array([b * np.cos(gammaRad), b * np.sin(gammaRad), 0])

    # Lattice Vector c (points along z-axis)
    cX = c * np.cos(betaRad)
    cY = c * (np.cos(alphaRad) - np.cos(betaRad) * np.cos(gammaRad)) / np.sin(gammaRad)
    cZ = c * np.sqrt(1 - np.cos(betaRad)**2 - (cY/c)**2)
    cVec = np.array([cX, cY, cZ])

    latticeVectors = np.array([aVec, bVec, cVec])

    return latticeVectors

def rotateUnitCell(latticeVec, atoms, rotAngles):
    '''Rotate unit cell lattice vectors and atoms'''
    xAxis = [1, 0, 0]
    yAxis = [0, 1, 0]
    zAxis = [0, 0, 1]

    atomTypes = [atom[0] for atom in atoms]
    atomCoords = [atom[1:4] for atom in atoms]

    if rotAngles[0] != 0:
        rotX = R.from_rotvec(np.radians(rotAngles[0]) * np.array(xAxis))
        latticeVec = rotX.apply(latticeVec)
        atomCoords = rotX.apply(atomCoords @ latticeVec)
    
    if rotAngles[1] != 0:
        rotY = R.from_rotvec(np.radians(rotAngles[1]) * np.array(yAxis))
        latticeVec = rotY.apply(latticeVec)
        atomCoords = rotY.apply(atomCoords @ latticeVec)

    if rotAngles[2] != 0:
        rotZ = R.from_rotvec(np.radians(rotAngles[2]) * np.array(zAxis))
        latticeVec = rotZ.apply(latticeVec)
        atomCoords = rotZ.apply(atomCoords @ latticeVec)

    if len(atoms[0]) == 4:
        rotatedAtoms = [atomTypes[i] + atomCoords[i] for i in range(len(atoms))]
    elif len(atoms[0]) == 5:
        rotatedAtoms = [atomTypes[i] + atomCoords[i] + atoms[i][-1] for i in range(len(atoms))]

    a = np.linalg.norm(latticeVec[0])
    b = np.linalg.norm(latticeVec[1])
    c = np.linalg.norm(latticeVec[2])

    alpha = np.degrees(np.acrcos(np.dot(latticeVec[1], latticeVec[2])/(b*c)))
    beta = np.degrees(np.acrcos(np.dot(latticeVec[0], latticeVec[2])/(a*c)))
    gamma = np.degrees(np.acrcos(np.dot(latticeVec[0], latticeVec[1])/(a*b)))

    cellParams = {'a' : a,
                  'b' : b,
                  'c' : c,
                  'alpha' : alpha,
                  'beta' : beta,
                  'gamma' : gamma}


    return rotatedAtoms, cellParams