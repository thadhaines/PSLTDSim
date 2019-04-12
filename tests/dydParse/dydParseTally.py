"""Test script to parse dyd file, and tally models found"""
import psltdsim as ltd
import pprint

# location of cases
dydLoc = '14ls11e_21P1a_dg.dyd' # light summer 2014
#dydLoc = '16HS31_dg.dyd' # heavy summer 2016
#dydLoc = '18HSP2a1.dyd' # heavy spring 2018
#dydLoc = '18HSP2a1_dg.dyd' # heavy spring 2018

""" Start of dictionary tally definitions """
primeMoverDict = {
'ccbt1' : 0,
'ccst3' : 0,
'crcmgv' : 0,
'degov1' : 0,
'g2wscc' : 0,
'gast' : 0,
'gegt1' : 0,
'ggov1' : 0,
'ggov2' : 0,
'ggov3' : 0,
'gpwscc' : 0,
'h6b' : 0,
'h6bd' : 0,
'hyg3' : 0,
'hygov4' : 0,
'hygov8' : 0,
'hygov' : 0,
'hygovr' : 0,
'hypid' : 0,
'hyst1' : 0,
'ieeeg1' : 0,
'ieeeg3' : 0,
'lcfb1' : 0,
'lm2500' : 0,
'lm6000' : 0,
'pidgov' : 0,
'stag1' : 0,
'tgov1' : 0,
'tgov3' : 0,
'w2301' : 0,
'wndtge' : 0,
'wndtrb' : 0,
'TOTAL': 0,
}

machineDict = {
'gencc' : 0,
'gencls' : 0,
'genind' : 0,
'genrou' : 0,
'gensal' : 0,
'gensdo' : 0,
'gentpf' : 0,
'gentpj' : 0,
'genwri' : 0,
'gewtg' : 0,
'motor1' : 0,
'motorc' : 0,
'motorw' : 0,
'motorx' : 0,
'shaft5' : 0,
'TOTAL': 0,
}

windTurbineDict = {
'ewtgfc' : 0,
'ewtgfx' : 0,
'exwtg1' : 0,
'extwge' : 0,
'genwri' : 0,
'gewtg' : 0,
'gewtgx' : 0,
'reec_a' : 0,
'regc_a' : 0,
'repc_a' : 0,
'repc_b' : 0,
'wndtge' : 0,
'wndtrb' : 0,
'wndvar' : 0,
'wt1g' : 0,
'wt1p' : 0,
'wt1p_b' : 0,
'wt1t' : 0,
'wt2e' : 0,
'wt2g' : 0,
'wt2p' : 0,
'wt2t' : 0,
'wt3e' : 0,
'wt3g' : 0,
'wt3p' : 0,
'wt3t' : 0,
'wt4e' : 0,
'wt4g' : 0,
'wt4t' : 0,
'wtga_a' : 0,
'wtgp_a' : 0,
'wtgq_a' : 0,
'wtgt_a' : 0,
'TOTAL': 0,
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
        primeMoverDict[parts[0]]+=1
        primeMoverDict['TOTAL']+=1

    elif parts[0] in machineDict:
        machineDict[parts[0]]+=1
        machineDict['TOTAL']+=1

    elif parts[0] in windTurbineDict:
        windTurbineDict[parts[0]]+=1
        windTurbineDict['TOTAL']+=1

    line = next(file, None)

file.close()
print('Finished Processing %d Lines.' % procLine)

# Output results
print('\ndyd: %s' % dydLoc)
print('\nPrime Movers Found:')
pprint.pprint(primeMoverDict)
print('\nMachines Found:')
pprint.pprint(machineDict)
print('\nWind Turbines Found:')
pprint.pprint(windTurbineDict)