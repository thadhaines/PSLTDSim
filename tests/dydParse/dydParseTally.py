"""Test script to parse dyd file, and tally models found"""
# 11/15/19    Addition of MW capacity and %s of models and capacity
# 11/17/19    Addition of LaTex style sorted table output

import pprint
import os

print(os.getcwd())
# workaround for interactive mode runs (Use as required)
#os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
print(os.getcwd())

import psltdsim as ltd

# location of cases
#dydLoc = '14ls11e_21P1a_dg.dyd' # light summer 2014
#dydLoc = '16HS31_dg.dyd' # heavy summer 2016
dydLoc = r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1.dyd"

#dydLoc = r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim\tests\dydParse\sixMachineGENERICmodels.dyd"
#dydLoc = '18HSP2a1_dg.dyd' # heavy spring 2018
#dydLoc = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_V9_RJ_govsfixed_fadded.dyd"
#dydLoc = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"

""" Start of dictionary tally definitions """
# each entry has a model count, MW capacity, % of total models, % of total Capacity list field
primeMoverDict = {
'ccbt1' :[ 0, 0, 0, 0],
'ccst3' :[ 0, 0, 0, 0],
'crcmgv' :[ 0, 0, 0, 0],
'degov1' :[ 0, 0, 0, 0],
'g2wscc' :[ 0, 0, 0, 0],
'gast' :[ 0, 0, 0, 0],
'gegt1' :[ 0, 0, 0, 0],
'ggov1' :[ 0, 0, 0, 0],
'ggov2' :[ 0, 0, 0, 0],
'ggov3' :[ 0, 0, 0, 0],
'gpwscc' :[ 0, 0, 0, 0],
'h6b' :[ 0, 0, 0, 0],
'h6bd' :[ 0, 0, 0, 0],
'hyg3' :[ 0, 0, 0, 0],
'hygov4' :[ 0, 0, 0, 0],
'hygov8' :[ 0, 0, 0, 0],
'hygov' :[ 0, 0, 0, 0],
'hygovr' :[ 0, 0, 0, 0],
'hypid' :[ 0, 0, 0, 0],
'hyst1' :[ 0, 0, 0, 0],
'ieeeg1' :[ 0, 0, 0, 0],
'ieeeg3' :[ 0, 0, 0, 0],
'lcfb1' :[ 0, 0, 0, 0],
'lm2500' :[ 0, 0, 0, 0],
'lm6000' :[ 0, 0, 0, 0],
'pidgov' :[ 0, 0, 0, 0],
'stag1' :[ 0, 0, 0, 0],
'tgov1' :[ 0, 0, 0, 0],
'tgov3' :[ 0, 0, 0, 0],
'w2301' :[ 0, 0, 0, 0],
'wndtge' :[ 0, 0, 0, 0],
'wndtrb' :[ 0, 0, 0, 0],
'TOTAL':[ 0, 0, 0, 0],
}

machineDict = {
'gencc' :[ 0, 0, 0, 0],
'gencls' :[ 0, 0, 0, 0],
'genind' :[ 0, 0, 0, 0],
'genrou' :[ 0, 0, 0, 0],
'gensal' :[ 0, 0, 0, 0],
'gensdo' :[ 0, 0, 0, 0],
'gentpf' :[ 0, 0, 0, 0],
'gentpj' :[ 0, 0, 0, 0],
'genwri' :[ 0, 0, 0, 0],
'gewtg' :[ 0, 0, 0, 0],
'motor1' :[ 0, 0, 0, 0],
'motorc' :[ 0, 0, 0, 0],
'motorw' :[ 0, 0, 0, 0],
'motorx' :[ 0, 0, 0, 0],
'shaft5' :[ 0, 0, 0, 0],
'TOTAL':[ 0, 0, 0, 0],
}

windTurbineDict = {
'ewtgfc' :[ 0, 0, 0, 0],
'ewtgfx' :[ 0, 0, 0, 0],
'exwtg1' :[ 0, 0, 0, 0],
'extwge' :[ 0, 0, 0, 0],
'genwri' :[ 0, 0, 0, 0],
'gewtg' :[ 0, 0, 0, 0],
'gewtgx' :[ 0, 0, 0, 0],
'reec_a' :[ 0, 0, 0, 0],
'regc_a' :[ 0, 0, 0, 0],
'repc_a' :[ 0, 0, 0, 0],
'repc_b' :[ 0, 0, 0, 0],
'wndtge' :[ 0, 0, 0, 0],
'wndtrb' :[ 0, 0, 0, 0],
'wndvar' :[ 0, 0, 0, 0],
'wt1g' :[ 0, 0, 0, 0],
'wt1p' :[ 0, 0, 0, 0],
'wt1p_b' :[ 0, 0, 0, 0],
'wt1t' :[ 0, 0, 0, 0],
'wt2e' :[ 0, 0, 0, 0],
'wt2g' :[ 0, 0, 0, 0],
'wt2p' :[ 0, 0, 0, 0],
'wt2t' :[ 0, 0, 0, 0],
'wt3e' :[ 0, 0, 0, 0],
'wt3g' :[ 0, 0, 0, 0],
'wt3p' :[ 0, 0, 0, 0],
'wt3t' :[ 0, 0, 0, 0],
'wt4e' :[ 0, 0, 0, 0],
'wt4g' :[ 0, 0, 0, 0],
'wt4t' :[ 0, 0, 0, 0],
'wtga_a' :[ 0, 0, 0, 0],
'wtgp_a' :[ 0, 0, 0, 0],
'wtgq_a' :[ 0, 0, 0, 0],
'wtgt_a' :[ 0, 0, 0, 0],
'TOTAL':[ 0, 0, 0, 0],
}
""" End Of dictionary tally Definitions"""
file = open(dydLoc, 'r')

cline = None # used in continued line operation
line = next(file)
procLine= 1

while line:
    procLine+=1
    if procLine %5000 == 0:
        print('Processed %d Lines...' % procLine)

    if line[0] == '#' or line[0] =='\n':
        # ignore comments and blanks
        line = next(file, None)
        continue

    if cline:
        # handle slash removal and string concatonation
        line = cline[:-1]+line
        cline = None

    parts = line.split()

    if parts[-1] == '/':
        # save continued line, get next line
        cline = line
        line = next(file, None)
        continue

    cline = None # line complete

    # check if model should be tallied, and tally if so
    if parts[0] in primeMoverDict:
        primeMoverDict[parts[0]][0]+=1
        primeMoverDict['TOTAL'][0]+=1
        for x in parts:
            if '=' in x:
                # strip value from mw=XX, and remove comma if required
                mwSplit = float(x.split('=')[1].replace(',', ''))
                primeMoverDict[parts[0]][1]+= mwSplit
                primeMoverDict['TOTAL'][1]+= mwSplit
                continue
        #break

    elif parts[0] in machineDict:
        machineDict[parts[0]][0]+=1
        machineDict['TOTAL'][0]+=1
        for x in parts:
            if '=' in x:
                # strip value from mw=XX, and remove comma if required
                mwSplit = float(x.split('=')[1].replace(',', ''))
                machineDict[parts[0]][1]+= mwSplit
                machineDict['TOTAL'][1]+= mwSplit
                continue


    elif parts[0] in windTurbineDict:
        windTurbineDict[parts[0]][0]+=1
        windTurbineDict['TOTAL'][0]+=1
        for x in parts:
            if '=' in x:
                # strip value from mw=XX, and remove comma if required
                mwSplit = float(x.split('=')[1].replace(',', ''))
                windTurbineDict[parts[0]][1]+= mwSplit
                windTurbineDict['TOTAL'][1]+= mwSplit
                continue

    # debug of agent creation
    #if parts[0] == "genrou":
    #    cleanLine = ltd.parse.cleanDydStr(line)
    #    print('cleaned: %s' % cleanLine)
    #           #newPmod = ltd.pslfModels.genrou(mirror, cleanLine)

    line = next(file, None)

file.close()
print('Finished Processing %d Lines.' % procLine)

# calculate percentages
listDicts = [primeMoverDict, machineDict, windTurbineDict]
for y in listDicts:
    for x in y:
        if x == 'TOTAL':
            continue
        # model count percent
        y[x][2] = y[x][0]/y['TOTAL'][0]*100
        y['TOTAL'][2] += y[x][2]
        # capacity percent
        y[x][3] = y[x][1]/y['TOTAL'][1]*100
        y['TOTAL'][3] += y[x][3]

# Output results
print('\ndyd: %s' % dydLoc)
print('\nPrime Movers Found:')
pprint.pprint(primeMoverDict)
print('\nMachines Found:')
pprint.pprint(machineDict)
print('\nWind Turbines Found:')
pprint.pprint(windTurbineDict)

print("")
for y in listDicts:

    # sort results by capacity percent
    sorted_x = sorted(y.items(), key=lambda x: x[1][3]) # sorts dictionary by capacity
    sorted_x.reverse()
    # sorted_x is a lis of tuples that contain the dictionary key, and dictionary list values
    # Print dictionary as a LaTeX table
    print("Model Name & \t Occurrences & \t MW MV Cap & \t \% of Models & \t \% of Capcacity \\\\")
    for x in sorted_x:

        # skip totally blank entires
        if (x[1][3] == 0) and (x[1][2] == 0):
            continue

        print("%s & \t%2.3f & \t%2.3f & \t%2.3f & \t%2.3f \\\\" % (x[0],x[1][0],x[1][1],x[1][2],x[1][3]))

    print("")