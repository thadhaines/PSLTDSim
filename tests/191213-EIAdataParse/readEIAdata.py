"""
Read EIA csv data, pull and sort MW load data, and display usable output
"""
## User specified input data
# full file Name (assumed in same folder as this file)
#fileName = "Balancing_authority_hourly_actual_and_forecast_demand_12_per_05_per_2019_–_12_per_12_per_2019_MST (1).csv"
#fileName = "Balancing_authority_hourly_actual_and_forecast_demand_12_per_05_per_2019_–_12_per_12_per_2019_MST (2).csv"
fileName = "Balancing_authority_hourly_actual_and_forecast_demand_12_per_05_per_2019_–_12_per_12_per_2019_MST.csv"

dataDate = "12/11/2019" # Date format in csv from EIA

## script start
# open file, initialize line outputD, and dataName
file = open(fileName, 'r')
line = next(file)
outputD = {}
dataName = None

# read file, pull data of interest into outputD
while line:
    print(line)
    # get data name from file
    if line.split(',')[0] == 'Category':
        dataName = line.split(',')[1].split()[0]
    
    if line.split()[0] == dataDate:
        mwDemand = line.split()[2].split(',')[1]
        mwForcast = line.split()[2].split(',')[2]
        time = line.split()[1].replace('H','')
        outputD[time] = { 'demand' : mwDemand, 'forcast': mwForcast}
    
    line = next(file,  None) # get next line, if there is one

file.close() # close file

# Format data output for verification
print("# Data from: %s %s" %(dataDate, dataName))
outputTuples = ['demand','forcast']
plotD = {}

for name in outputTuples:
    outputList = []
    time = []
    
    print("%s = [ \n\t#(time , MW data)" % name)
    for entry in sorted(outputD):
        time.append(int(entry))
        outputList.append( int(outputD[entry][name]) )
        print("\t(%s, %s)," %(entry,outputD[entry][name] ) )
    print("\t]")
    plotD[name] = outputList
    plotD[name+'Time'] = time 

# Output in Percent change from previous value
print("# Data from: %s %s" %(dataDate, dataName))
for name in outputTuples:
    print("%s = [ \n\t#(time , Precent change from previous value)" % name)
    initVal = None
    for entry in sorted(outputD):
        if initVal == None:
            initVal = float(outputD[entry][name])
            prevVal = initVal
        
        curVal = float(outputD[entry][name])
        print("\t(%s, %.3f)," %(entry, (curVal-prevVal)/initVal*100 ) )
        prevVal = curVal
        
    print("\t]")

# make plot for fun
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(plotD['demandTime'],plotD['demand'] , label='Demand')
ax.plot(plotD['forcastTime'],plotD['forcast'], label = 'Forcast')

ax.set_title('Load Forcast and Demand on %s from %s'%(dataDate, dataName))
ax.set_ylabel('MW')
ax.set_xlabel('Time [Hours]')
ax.grid(True)
ax.legend()
ax.set_xlim(min(plotD['demandTime']),max(plotD['demandTime']))

plt.show()
plt.pause(0.00001)
