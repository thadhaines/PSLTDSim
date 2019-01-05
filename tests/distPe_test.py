"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

# workaround for interactive mode runs (Use only if required)
import os
print(os.getcwd())
os.chdir("C:\\Users\\thad\\Source\\Repos\\thadhaines\\LTD_sim\\")

# Simulation Parameters
timeStep = 1.0
endTime = 10.0
slackTol = 1.0
Hsys = 0.0 # MW*sec of entire system, if !> 0.0, will be calculated in code
Dsys = 0.0 # PU - TODO: Incoroporate into simulation (probably)

# Required Paths
## full path to middleware dll
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  
## path to folder containing PSLF license
pslfPath = r"C:\Program Files (x86)\GE PSLF"  

# fast debug case switching
test_case = 0
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = r"C:\LTD\pslf_systems\eele554\ee554.dyd"
elif test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )
del fullMiddlewareFilePath, pslfPath, savPath, dydPath

simParams = (
    timeStep,
    endTime,
    slackTol,
    Hsys,
    Dsys,
    )
del timeStep, endTime, slackTol, Hsys, Dsys

# these files will change after refactor
execfile('CoreAgents.py')
execfile('Model.py')

# mirror arguments: locations, simParams, debug flag
mir = Model(locations, simParams, 1)

# Pertrubances configured for test case (ee554 files)
mir.addPert('Load',[3,'2'],'Step',['St',2,1])
mir.addPert('Load',[3,'2'],'Step',['St',9,0])
mir.addPert('Load',[3,'2'],'Step',['P',4,50.0])
mir.addPert('Load',[3],'Step',['Q',6,10.0])

mir.runSim()

print("Log and Step check of Load '2' and Pacc:")
print("Time\tSt\tP\tSystem Pacc")
for x in range(len(mir.Load[1].r_P)):
    print("%d\t%d\t%.2f\t%.2f" % (
        mir.r_t[x],
        mir.Load[1].r_St[x],
        mir.Load[1].r_P[x],
        mir.r_ss_Pacc[x],))

print("Check of Pe distribution (H1 = H2):")
print("Time\tG1Pe\tG2Pe\tSystem Pacc delta")
for x in range(len(mir.r_t)):
    print("%d\t%.2f\t%.2f\t%.2f" % (
        mir.r_t[x],
        mir.Machines[0].r_Pe[x],
        mir.Machines[1].r_Pe[x],
        mir.r_Pacc_delta[x],))

raw_input("Press <Enter> to Continue. . . . ")