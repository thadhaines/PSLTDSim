"""Template starting point for LTD dev"""
print("Start LTD...")

# Required Paths
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  # full path to dll
pslfPath = r"C:\Program Files (x86)\GE PSLF"  # path to folder containing PSLF license
savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
#savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )

execfile('Agents.py')
execfile('Model.py')

env = Model(locations)
env.caseParams()

raw_input("Press <Enter> to Continue. . . . ")