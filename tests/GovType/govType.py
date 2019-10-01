"""
Script to investigate quantity of known turbine types assocaited to generators 
in WECC base case (or any case).
Input: location of .sav file
"""
import pprint
import os
import subprocess
import signal
import time
import __builtin__

print(os.getcwd())
# workaround for interactive mode runs (Use as required)
#os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

print(os.getcwd())

# import custom package and make truly global
import psltdsim as ltd
__builtin__.ltd = ltd

# full WECC
savPath = r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav"
dydPath = [r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1.dyd"]
#savPath = r"C:\LTD\pslf_systems\fullWecc\16HS\16HS3a.sav"
#dydPath = [r"C:\LTD\pslf_systems\fullWecc\16HS\16HS31_dg.dyd"]
#savPath = r"C:\LTD\pslf_systems\fullWecc\14LS_DE\14LS_100GW_ALS_SHAWN.sav"
#dydPath = [r"C:\LTD\pslf_systems\fullWecc\14LS_DE\14ls11e_21P1a_dg.dyd"]
ltdPath = None

# Required Paths Dictionary
locations = {
    # path to folder containing middleware dll
    'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'savPath' : savPath,
    'dydPath': dydPath,
    'ltdPath': ltdPath,
    }

ltd.init_PSLF(locations, False)
cPar = col.CaseparDAO.GetCasepar()
nGens = cPar.Ngen
foundGens = 0
curNDX= 0
unkGov = 0

turDict = {
"0" : {'type' : "unknown", 'count' : 0, 'ndxList':[]},
"1" : {'type' : "non-reheat steam", 'count' : 0, 'ndxList':[]},
"2" : {'type' : "reheat steam", 'count' : 0, 'ndxList':[]},
"3" : {'type' : "steam cross compound unit", 'count' : 0, 'ndxList':[]},
"4" : {'type' : "steam in combined cycle (separate shaft)", 'count' : 0, 'ndxList':[]},
"5" : {'type' : "hydro", 'count' : 0, 'ndxList':[]},
"6" : {'type' : "diesel-non turbo charged", 'count' : 0, 'ndxList':[]},
"7" : {'type' : "diesel turbo charged", 'count' : 0, 'ndxList':[]},
"11" : {'type' : "industrial GT (single shaft)", 'count' : 0, 'ndxList':[]},
"12" : {'type' : "aero derivative GT", 'count' : 0, 'ndxList':[]},
"13" : {'type' : "single shaft combined cycle", 'count' : 0, 'ndxList':[]},
"14" : {'type' : "synchronous condenser (no turbine)", 'count' : 0, 'ndxList':[]},
"21" : {'type' : "type 1 wind turbine", 'count' : 0, 'ndxList':[]},
"22" : {'type' : "type 2 wind turbine", 'count' : 0, 'ndxList':[]},
"23" : {'type' : "type 3 wind turbine", 'count' : 0, 'ndxList':[]},
"24" : {'type' : "type 4 wind turbine", 'count' : 0, 'ndxList':[]},
"31" : {'type' : "photovoltaic", 'count' : 0, 'ndxList':[]},
"40" : {'type' : "dc tie (generators representing DC ties)", 'count' : 0, 'ndxList':[]},
"41" : {'type' : "motor/pump", 'count' : 0, 'ndxList':[]},
"99" : {'type' : "other", 'count' : 0, 'ndxList':[]},
}



while foundGens < nGens:
    cGen = col.GeneratorDAO.FindByIndex(curNDX)
    if type(cGen) == type(None):
        # No Generator found at index
        print("no gen at ndx %d" % curNDX)
    else:
        foundGens +=1
        tType = cGen.TurbineType
        if str(tType) in turDict:
            turDict[str(tType)]['count'] +=1
            turDict[str(tType)]['ndxList'].append(curNDX)

    curNDX +=1

print("\nPercent of Known Turbine Types = %.2f%%" %
      ( (1-(turDict['0']['count']+turDict['99']['count'])/float(nGens))*100))
print('Number of unknowns and other: %d' % 
      (turDict['0']['count']+turDict['99']['count']))
#pprint.pprint(turDict)
print("Count \t   Type")
for key in sorted(turDict.keys()):
    dEntry = turDict[key]
    print("%d\t     %s" %( dEntry['count'],dEntry['type'],))


# next step is figuring out which generator ndx entries actually have governors....