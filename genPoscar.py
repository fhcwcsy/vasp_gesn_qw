# generate POSCAR for GeSn QW
import random

qwThickness = 40 # angstrom
bufferThickness = 100 # angstrom
snFraction = 0.11
filename = './POSCAR'
latticeConst = 5.657 # angstrom, conventional cell
superCellWidth = 2 # cells


with open(filename, 'w') as f:

    system = (str(qwThickness/10) + 'nm ' + str(snFraction*100) + '% GeSn quantum well + ' 
            + str(bufferThickness/10) + 'nm buffer')

    qwLayer = round(qwThickness / latticeConst)
    bufferLayer = round(bufferThickness / latticeConst)
    nAtom = 8*superCellWidth*superCellWidth*(qwLayer+bufferLayer)
    nSn = round(8*superCellWidth*superCellWidth*qwLayer*snFraction)
    nGeBuffer = 8*superCellWidth*superCellWidth*bufferLayer
    nGeQW = 8*superCellWidth*superCellWidth*qwLayer - nSn
    print('Number of Sn atoms in the QW:', nSn)
    print('Number of Ge atoms in the QW:', nGeQW)
    print('Actual percentage:', nSn/(nSn+nGeQW))

    latticeX = superCellWidth
    latticeZ = qwLayer+bufferLayer

    ionPositions = list()
    # generate ion coordinates
    for z in range(qwLayer+bufferLayer):
        # the lower qwLayer layers are the QW, and the top bufferLayer layers are the buffer
        for x in range(superCellWidth):
            for y in range(superCellWidth):
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x, y, z))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x+0.5, y+0.5, z))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x, y+0.5, z+0.5))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x+0.5, y, z+0.5))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x+0.25, y+0.25, z+0.25))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x+0.75, y+0.75, z+0.25))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x+0.25, y+0.75, z+0.75))
                ionPositions.append('{:.2f}\t{:.2f}\t{:.2f}\t'.format(x+0.75, y+0.25, z+0.75))

    # generate Sn positions
    qwindex = list(range(nSn+nGeQW))
    random.shuffle(qwindex) # the first nSn ions are Sn, the rest are Ge

    # write output POSCAR
    f.write(system + '\n')
    f.write(str(latticeConst) + '\n')
    
    # lattice vectors
    f.write(str(latticeX) + '\t0\t0\n')
    f.write('0\t'+str(latticeX)+'\t0\n')
    f.write('0\t0\t'+str(latticeZ)+'\n')

    # ion positions
    f.write('Sn\tSin'+str(nSn)+'\t'+str(nGeQW+nGeBuffer)+'\n')
    f.write('Cartesian\n')

    # QW: Sn ions
    for ionIndex in range(nSn):
        f.write(ionPositions[qwindex[ionIndex]]+'Sn\n')

    # QW: Ge ions
    for ionIndex in range(nSn, nSn+nGeQW):
        f.write(ionPositions[qwindex[ionIndex]]+'Ge\n')

    # Buffer layer
    for ionIndex in range(nSn+nGeQW, nAtom):
        f.write(ionPositions[ionIndex]+'Ge\n')

