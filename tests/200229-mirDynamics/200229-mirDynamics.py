"""
Scan mirror for dynamic information
i.e. tally types of govrnors and/or machines active in simulation

Reasoning: The dyd file contains many models that are not used, or linked,
to objects in the main island. 
The resulting output should present a more accurate picture of system models.
"""

import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd
dirname = os.path.dirname(__file__)
tempFolder = os.path.split(dirname)[0]
rootDir = os.path.split(tempFolder)[0] # root git folder

mirLoc = os.path.join(rootDir, 'delme','thesisV','18HSPweccStepF.mir') #wecc step 2018

mir = ltd.data.readMirror(mirLoc)

print(mir)

# governor model count/capacity for ALL models
govDict = {
    # Template for collection dictionary
    'total': {
        'count':0,
        'capacity':0,
        },
    }

for gov in mir.Dynamics:
    try:
        modelName = gov.PSLFgov.Type
    except AttributeError:
        modelName = gov.PSFLgov.Type # typo in tgov 1...

    if modelName in govDict:
        govDict[modelName]['count'] += 1
        govDict[modelName]['capacity'] += gov.mwCap
    else:
        govDict[modelName] ={
           'count': 1,
           'capacity' : gov.mwCap,
           }

    govDict['total']['count'] += 1
    govDict['total']['capacity'] += gov.mwCap

print("Model & \tCount\t & Capacity [MW] \\\\")
for key in sorted(govDict.items(), key=lambda x: x[1]['count'],reverse=True):
    model = key[0]
    count = key[1]['count']
    cap = key[1]['capacity']
    print("%7s & \t%5d\t & %9.2f \\\\" % (model, count, cap))


# model information for SIMULATED models
simGovs = {
    # Template for collection dictionary
    'total': {
        'count':0,
        'capacity':0,
        },
    'gas': {
        'count':0,
        'capacity':0,
        },
    'steam': {
        'count':0,
        'capacity':0,
        },
    'hydro': {
        'count':0,
        'capacity':0,
        },
    'tgov1': {
        'count':0,
        'capacity':0,
        },
    }

for gov in mir.Dynamics:

    if 'Gas' in str(type(gov)):
        simGovs['gas']['count'] += 1
        simGovs['gas']['capacity'] += gov.mwCap
    elif 'Hydro' in str(type(gov)):
        simGovs['hydro']['count'] += 1
        simGovs['hydro']['capacity'] += gov.mwCap
    elif 'Steam' in str(type(gov)):
        simGovs['steam']['count'] += 1
        simGovs['steam']['capacity'] += gov.mwCap
    elif 'tgov1' in str(type(gov)):
        simGovs['tgov1']['count'] += 1
        simGovs['tgov1']['capacity'] += gov.mwCap

    simGovs['total']['count'] += 1
    simGovs['total']['capacity'] += gov.mwCap

print("\nModel & \tCount & \tCapacity [MW] \\\\")
for key in sorted(simGovs.items(), key=lambda x: x[1]['count'],reverse=True):
    model = key[0]
    count = key[1]['count']
    cap = key[1]['capacity']
    print("%7s\t & %5d\t & %9.2f \\\\" % (model, count, cap))

# Machine Info

genDict = {
    'total':{
        'count' : 0,
        'capacity' : 0.0,
        },
    }

for gen in mir.Machines:
    if gen.machine_model != False:
        model = gen.machine_model.Type

        if model in genDict:
            genDict[model]['count']+=1
            genDict[model]['capacity'] += gen.Pmax
        else:
            genDict[model] = {
                'count' : 1,
                'capacity' : gen.Pmax,
                }

        genDict['total']['count'] +=1
        genDict['total']['capacity'] += gen.Pmax

print("\nModel & \t Count\t & Capacity [MW] \\\\")
for key in sorted(genDict.items(), key=lambda x: x[1]['count'],reverse=True):
    model = key[0]
    count = key[1]['count']
    cap = key[1]['capacity']
    print("%7s\t & %5d\t & %9.2f \\\\" % (model, count, cap))


print("Machines:\t%d" %len(mir.Machines))
print("Loads:\t%d" %len(mir.Load))
print("Bus:\t%d" %len(mir.Bus))
print("DEBUG STOP")

"""
Resultant Output:
*** Mirror read from 18HSPweccStepF.mir
<Mirror object at 0x8688b90>
Created from:  C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav
Created on:    2020-02-12 11:14:17.940000
Model	Count	Capacity [MW]
  total	 2243	204161.59
  ggov1	 1006	 74804.11
   hyg3	  315	 28755.47
  hygov	  196	  8883.36
 ieeeg1	  191	 49022.45
 hygov4	  167	  8044.68
 ieeeg3	  133	  9174.48
 gpwscc	   56	  3028.33
 pidgov	   56	  8034.54
   gast	   29	  1162.56
  ggov3	   28	  5010.32
 hygovr	   25	  6249.37
  tgov1	   20	  1140.45
 g2wscc	   18	   818.95
  ccbt1	    3	    32.53

Model	Count	Capacity [MW]
  total	 2243	204161.59
    gas	 1090	 82842.76
  hydro	  777	 60786.37
  steam	  356	 59392.02
  tgov1	   20	  1140.45

Model	Count	Capacity [MW]
  total	 3330	244166.46
 gentpj	 1541	 96559.72
 genrou	 1277	128990.75
 gentpf	  476	 17707.11
 motor1	   34	   717.89
 genwri	    2	   191.00
DEBUG STOP
"""