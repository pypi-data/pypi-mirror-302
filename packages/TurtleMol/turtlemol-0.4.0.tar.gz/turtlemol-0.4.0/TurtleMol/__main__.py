'''Module contains the main loop'''

import sys
import re
import argparse
from .drawMol import drawMolBox, drawMolSphere, drawMolMesh
from .readWriteFiles import writeOutput, getInput, readStrucFile, loadGlobalMatrix
from .defaultParams import defaultParams
from .multMesh import buildMultiMesh

def parseCommandLine(dparams):
    '''Parses command line for parameters'''
    parser = argparse.ArgumentParser(description='Tile Fill')

    # Command line arguemnnts
    parser.add_argument('-i', '--inputFile', type=str, help="Path to input file")
    parser.add_argument('-struc', '--structureFile', type=str,
                        help='Path to structure file')
    parser.add_argument('-baseStruc', '--baseStrucFile', type=str,
                        help='Path to base structure file', default=dparams['baseStrucFile'])
    parser.add_argument('-s', '--shape', type=str,
                        help="Shape (Box or Cube)", default=dparams['shape'])
    parser.add_argument('-sl', '--sideLength', type=float,
                        help="Dimensions of a cube in Angstroms", default=dparams['sideLength'])
    parser.add_argument('-xl', '--Xlen', type=float,
                        help="X dimension of a box in Angstroms", default=dparams['Xlen'])
    parser.add_argument('-yl', '--Ylen', type=float,
                        help="Y dimension of a box in Angstroms", default=dparams['Ylen'])
    parser.add_argument('-zl', '--Zlen', type=float,
                        help="Z dimension of a box in Angstroms", default=dparams['Zlen'])
    parser.add_argument('-r', '--radius', type=float,
                        help="Radius of a sphere in Angstroms", default=dparams['radius'])
    parser.add_argument('-rand', '--randomizeOrient', type=bool,
                        help="Randomize the orientation or not", default=dparams['randomizeOrient'])
    parser.add_argument('-randFill', '--randFill', type=bool,
                        help="Randomize place molecules when placing a set number",
                        default=dparams['randFill'])
    parser.add_argument('-center', '--center', nargs='+', type=float,
                        help="X, Y, Z coordinates of the center of a sphere",
                        default=dparams['sphereCenter'])
    parser.add_argument('-baseCenter', '--baseStrucCenter', nargs='+', type=float,
                        help="X, Y, Z coordinates of the center of the base structure",
                        default=dparams['baseStrucCenter'])
    parser.add_argument('-n', '--numMolecules', type=int,
                        help="Number of molecules", default=dparams['numMolecules'])
    parser.add_argument('-t', '--tol', type=float,
                        help="Minimum distance between molecules", default=dparams['tol'])
    parser.add_argument('-rho', '--density', type=float,
                        help="Density in g/mL", default=dparams['density'])
    parser.add_argument('-a', '--maxAttempts', type=int,
                        help="Maximum iterations for finite sized systems",
                        default=dparams['maxAttempts'])
    parser.add_argument('-ar', '--atomRadius', type=str,
                        help="What radius type to be used for atoms",
                        default=dparams['atomRadius'])
    parser.add_argument('-out', '--outputFile', type=str,
                        help="Path for output file if desired")
    parser.add_argument('-mesh', '--mesh', type=str,
                        help="Path for mesh file if desired")
    parser.add_argument('-scale', '--meshScale', type=float,
                        help="Uniform scale of mesh", default=dparams['meshScale'])

    return parser.parse_args()

def main():
    '''The main loop'''
    # Init default params
    dparams = defaultParams()

    # Init arguement parser
    args = parseCommandLine(dparams)

    iparams = {}
    if args.inputFile:
        iparams = getInput(args.inputFile)
    else:
        for argName in vars(args):
            iparams[argName] = getattr(args, argName)

    for name in dparams:
        if name not in iparams:
            iparams[name] = dparams[name]

    if not iparams['structureFile']:
        print('Please provide an initial structure')
        sys.exit()

    # Check if structures and meshes are singular or plural
    if ',' in iparams['structureFile']:
        iparams['structureFile'] = [path.strip() for path in iparams['structureFile'].split(',')]

    if iparams['mesh'] is not None and ',' in iparams['mesh']:
        iparams['mesh'] = [path.strip() for path in iparams['mesh'].split(',')]

    if isinstance(iparams['meshScale'], list) and ',' in iparams['meshScale']:
        iparams['meshScale'] = [path.strip() for path in iparams['meshScale'].split(',')]

    if iparams['scaleX'] is not None and ',' in iparams['scaleX']:
        iparams['scaleX'] = [path.strip() for path in iparams['scaleX'].split(',')]

    if iparams['scaleY'] is not None and ',' in iparams['scaleY']:
        iparams['scaleY'] = [path.strip() for path in iparams['scaleY'].split(',')]

    if iparams['scaleZ'] is not None and ',' in iparams['scaleZ']:
        iparams['scaleZ'] = [path.strip() for path in iparams['scaleZ'].split(',')]

    if iparams['globalMatrixPath'] is not None and ',' in iparams['globalMatrixPath']:
        iparams['globalMatrixPath'] = [path.strip() for path in iparams['globalMatrixPath'].split(',')]

    print(iparams)

    # Get structure
    if isinstance(iparams['structureFile'], str):
        struc, unitCell = readStrucFile(iparams['structureFile'])
        unitCells = None
        print(struc)
    elif isinstance(iparams['structureFile'], list):
        struc = []
        unitCells = []
        for i in iparams['structureFile']:
            strucs, unitCellTemp = readStrucFile(i)
            struc.append(strucs)
            unitCells.append(unitCellTemp)

    if unitCell:
        iparams['unitCell'] = [unitCell['a'], unitCell['b'], unitCell['c']]
        iparams['angle'] = [unitCell['alpha'], unitCell['beta'], unitCell['gamma']]

    if unitCells:
        iparams['unitCells'] = [[cell['a'], cell['b'], cell['c']] if cell is not None else None for cell in unitCells]
        iparams['angles'] = [[cell['alpha'], cell['beta'], cell['gamma']] if cell is not None else None for cell in unitCells]

    if iparams['globalMatrixPath'] is not None and isinstance(iparams['globalMatrixPath'], list):
        matrices = []
        for m in iparams['globalMatrixPath']:
            globMat = loadGlobalMatrix(m)
            matrices.append(globMat)

        iparams['globalMatrix'] = matrices

    if iparams['baseStrucFile']:
        baseStruc, baseUnitCell = readStrucFile(iparams['baseStrucFile'])
    else:
        baseStruc = None

    if iparams['shape'].lower() == 'box' or iparams['shape'].lower() == 'cube':
        # Generate the new structure

        if unitCell:
            outStruc, strucType, cellParams = drawMolBox(struc, baseStruc, iparams)
        else:
            outStruc, strucType = drawMolBox(struc, baseStruc, iparams)

    elif iparams['shape'].lower() == 'sphere':
        # Generate the new structure
        if unitCell:
            outStruc, strucType, cellParams = drawMolSphere(struc, baseStruc, iparams)
        else:
            outStruc, strucType = drawMolSphere(struc, baseStruc, iparams)

    elif iparams['shape'].lower() == 'mesh' and iparams['mesh'] is not None:
        # Generate the new structure
        if unitCell:
            outStruc, strucType, cellParams = drawMolMesh(struc, baseStruc, iparams)
        else:
            outStruc, strucType = drawMolMesh(struc, baseStruc, iparams)

    elif iparams['shape'].lower() == 'multimesh' and isinstance(iparams['mesh'], list):
        assert iparams['globalMatrix'] is not None and len(iparams['globalMatrix']) == len(iparams['mesh']), 'Global transformation matrix required for each mesh'
        outStruc, strucType, cellParams = buildMultiMesh(struc, baseStruc, iparams)

    if iparams['outputFile']:
        if unitCell:
            writeOutput(outStruc, iparams['outputFile'], strucType, cellParams, iparams['padding'])
        else:
            writeOutput(outStruc, iparams['outputFile'], strucType)

if __name__ == "__main__":
    main()
