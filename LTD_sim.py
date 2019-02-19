"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""
ver = True # for attempting version 3, set to None otherwise

import os
import subprocess
import signal

if ver:
    import builtins
    builtins.ver = ver
else:
    import __builtin__

# workaround for interactive mode runs (Use only if required)
print(os.getcwd())
#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")
#os.chdir(r"D:\Users\jhaines\Source\Repos\thadhaines\LTD_sim")
os.chdir(r"C:\Users\thad\Source\Repos\thadhaines\LTD_sim")
print(os.getcwd())

from parseDyd import *
from distPe import *
from combinedSwing import *
from findFunctions import *
from PerturbanceAgents import *
from pgov1Agent import *
from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent
from Model import Model
from makeModelDictionary import makeModelDictionary
from saveModelDictionary import saveModelDictionary

if ver:
    exec(open("./mergeDicts.py").read())
else:
    execfile('mergeDicts.py')


simNotes = """
Initial test of GE 4 machine, 2 area system.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0,
    'endTime': 30.0,
    'slackTol': .25,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; TODO: Incoroporate into simulation (probably)

    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'Euler',

    # Data Export Parameters
    'fileDirectory' : r"\\verification\\GE4machine\\", # relative path must exist before simulation
    'fileName' : 'ge4test01',
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'exportMat': 1, # requies exportDict == 1 to work
    }

# fast debug case switching
# TODO: enable new dyd replacement
test_case = 4
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc.dyd",
               #r"C:\LTD\pslf_systems\eele554\ee554.ltd.dyd", #pgov1 on gen 2
               ]
elif test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = [r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"]
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = [r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"]
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = [r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"]
elif test_case == 4:
    savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"
    dydPath = [r"C:\LTD\pslf_systems\GE_ex\g4_a.dyd",
               r"C:\LTD\pslf_systems\GE_ex\g4_a.ltd", #pgov1 on slacks
               ]

# Required Paths Dictionary
locations = {
    # full path to middleware dll
    'fullMiddlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    #'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'pslfPath':  r"C:\upslf19",
    'savPath' : savPath,
    'dydPath': dydPath,
    }
del savPath, dydPath

# these files will change after refactor, required after locations definition

if ver:
    exec(open("./initPSLF3.py").read())
    exec(open("./makeGlobals3.py").read())
else:
    execfile('initPSLF.py')
    execfile('makeGlobals.py')

# mirror arguments: locations, simParams, debug flag
mir = Model(locations, simParams, 1)

# Pertrubances configured for test case (eele)
# step up and down (pgov test)
#mir.addPert('Load',[3],'Step',['P',2,101]) # quick 1 MW step
#mir.addPert('Load',[3],'Step',['P',30,100]) # quick 1 MW step

# GE 4 machine test
mir.addPert('Load',[5],'Step',['P',2,4,'rel']) # step 4 MW up
#mir.addPert('Load',[5],'Step',['P',52,-4,'rel']) # step back to normal
#mir.addPert('Load',[5],'Step',['St',2,0]) # turn load off
#mir.addPert('Load',[5],'Step',['St',3,1]) # turn load on
#mir.addPert('Load',[6],'Step',['P',15,4,'rel']) # step 4 MW up
#mir.addPert('Load',[6],'Step',['P',25,4,'rel']) # step 4 MW up
#mir.addPert('Load',[6],'Step',['P',55,-8,'rel']) # step back to normal

mir.runSim()

"""
# Testing of repeated epcl calling
n=0
limit = 1545
noPrintStr = "dispar[0].noprint = 1"
PSLF.RunEpcl(noPrintStr)
Pload = 0.01
import time
while n <limit:
    n+=1
    a=mir.Load[0].getPref()
    sb = str(a.get__Idx())
    epclTest = ("load[%s].p = load[%s].p + %f" % (sb,sb,Pload))
    
    #PSLF.RunEpclScript('test.p') # gets 1541 before crash
    PSLF.RunEpcl(epclTest) # gets 1540 before crash. memory leak...

    b=mir.Load[0].getPref()
    mir.Load[0].getPvals() 

    dif = abs(mir.Load[0].P- b.P)/Pload
    print("%d\t%.2f\tPSLF: %f\tPython: %f" %(n, dif, b.P, mir.Load[0].P))
    #mir.LTD_Solve() # this line not problem

    del a
    del b
    del sb
    del dif

    if (n%1500 == 0):# attempt to restart PSLF doesn't fix leak
        PSLF.SaveCase('tempSav')
        PSLF.Finalize()
        PSLF.ExitPslf()

        del builtins.PSLF
        
        #time.sleep(1)
        builtins.PSLF = mid.Pslf(locations['pslfPath'])
        PSLF.LoadCase('tempSav')
        noPrintStr = "dispar[0].noprint = 1"
        PSLF.RunEpcl(noPrintStr)
        resetFlag = 0


"""
mir.notes = simNotes # update notes before export

# Terminal display output for immediate results
print("Log and Step check of Load, Pacc, and sys f:")
print("Time\tSt\tPacc\tsys f\tdelta f\t\tSlackPe\tGen2Pe")
for x in range(mir.c_dp-1):
    print("%d\t%d\t%.2f\t%.5f\t%.6f\t%.2f\t%.2f" % (
        mir.r_t[x],
        mir.Load[0].r_St[x],
        mir.r_ss_Pacc[x],
        mir.r_f[x],
        mir.r_deltaF[x],
        mir.Slack[0].r_Pe[x],
        mir.Machines[1].r_Pe[x],))
print('End of simulation data.')

# Data export
if simParams['exportDict']:
    # Change current working directory to data destination.
    cwd = os.getcwd()
    if simParams['fileDirectory'] :
        os.chdir(cwd + simParams['fileDirectory'])

    dictName = simParams['fileName']
    D = makeModelDictionary(mir)
    savedName = saveModelDictionary(D,dictName)
    os.chdir(cwd)

    if  simParams['exportMat']:
        # use cmd to run python 3 32 bit script...
        cmd = "py -3-32 makeMat.py " + savedName +" " + dictName  + " "+ simParams['fileDirectory'] 

        matProc = subprocess.Popen(cmd)
        matReturnCode = matProc.wait()
        matProc.send_signal(signal.SIGTERM)


## update to make mat using python 3.6
if simParams['fileDirectory']:
        cwd = os.getcwd()
        os.chdir(cwd + simParams['fileDirectory'])

sysDict = makeModelDictionary(mir)
mirD ={'varName01':sysDict}
import scipy.io as sio
sio.savemat('varName01', mirD)
print("saved?")

# raw_input("Press <Enter> to Continue. . . . ") # Not always needed to hold open console

"""
Results:
The logical choice of using the built-in Save() function to update PSLF doesn't work under pythonnet (python3)
As a work-around, RunEpcl() has been setup to serve a similar purpose
This unfortunately causes a memory leak that eventually crashes any code after calling a certain number of EPCL
Something about a System.Reflection. from the middleware EPCL.CallSpawn...
I don't think there is anything more to do about it without GE fixing their code.
However, the code does run in python3 - max simulation time limted by number of EPCL calls. (1540 ish)
"""