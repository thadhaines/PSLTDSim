"""Template starting point for LTD dev"""

# Required Paths
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  # full path to dll
pslfPath = r"C:\Program Files (x86)\GE PSLF"  # path to folder containing PSLF license
savPath = r"D:\Users\jthaines\Desktop\pslf_systems\MicroWECC_PSLF\microBusData.sav"
dydPath = r"D:\Users\jthaines\Desktop\pslf_systems\MicroWECC_PSLF\microDynamicsData.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )

execfile('Model.py')
execfile('Agents.py')

mirror = Model(locations)

raw_input("Press <Enter> to Continue. . . . ")