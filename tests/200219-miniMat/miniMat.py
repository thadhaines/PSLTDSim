"""
Exporting data from full WECC case produces a .mat file that MATLAB
doesn't seem to like opening.
This file is intended to produce a .mat that will work with previously
made matlab frequency validation plots

i.e. only system meta data and system frequency is in .mat

Debug from interactive runs

"""
import psltdsim as ltd

# handle file directory paths
import os
dirname = os.path.dirname(__file__)
print(dirname)
tempFolder = os.path.split(dirname)[0]
rootDir = os.path.split(tempFolder)[0] # root git folder

mirLoc = os.path.join(rootDir, 'delme','thesisV','18HSPweccStepF.mir')
#mirLoc = os.path.join(rootDir, 'delme','thesisV','SixMachineStep1F.mir')

mir = ltd.data.readMirror(mirLoc)

printFigs = False
ltd.plot.sysF(mir, True, printFigs)


rootD = mir.getDataDict()
"""
# busnumber:busName
# uses mbase and H to calcualte weighted freq using psds data
tempGenD = {}
gNdx = 0
for gen in mir.Machines:
    if all(gen.r_St): # for always on gens
        gNdx+=1
        genMATndx = 'G'+str(gNdx)
        genID = str(gen.Busnum) +':'+gen.Busnam
        tempGenD[genMATndx] = {
            'psdsID' : genID,
            'id' : gen.Id,
            'mBase' : gen.Mbase,
            'Hpu' : gen.Hpu,
            'H' : gen.Mbase*gen.Hpu,
            }

# combine gen dict into rootD
genD = {'gens': tempGenD, 'nGens' : gNdx}
rootD = ltd.data.mergeDicts(rootD, genD)
"""
varName = mir.simParams['fileName']
mirD ={varName:rootD}
import scipy.io as sio

mirD = {
    'mir' : {
        'f' : mir.r_f,
        't' : mir.r_t,
            }
        }
os.chdir(dirname)
sio.savemat(varName, mirD)

#ltd.data.exportMat(mirror, mirror.simParams)

# counting of total governors and how many are actually a tgov1
govCount = 0
tgovCount =0
for gov in mir.Dynamics:
    govCount +=1
    if 'tgov1Agent' in str(type(gov)):
        tgovCount +=1

print(tgovCount)
print(govCount)
print("%.2f" % (tgovCount/govCount))
"""
Weighted frequency calcualtion requires generator data from mirror...

WECC data still doesn't export to mat correctly.

"""