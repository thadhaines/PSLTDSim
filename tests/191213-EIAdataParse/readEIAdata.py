"""
Read EIA csv data, pull and sort MW load data, and display usable output

Meant to be used to generate input to Load control / Dispatch Control Agents
"""
## User specified input data
# full file Name (assumed in same folder as this file)
fileName = "Balancing_authority_hourly_actual_and_forecast_demand_12_per_05_per_2019_–_12_per_12_per_2019_MST (1).csv"
#fileName = "Balancing_authority_hourly_actual_and_forecast_demand_12_per_05_per_2019_–_12_per_12_per_2019_MST (2).csv"
fileName = "Balancing_authority_hourly_actual_and_forecast_demand_12_per_05_per_2019_–_12_per_12_per_2019_MST.csv"

dataDate = "12/11/2019" # Date format in csv from EIA
dataTimeStart = "05" # hour format as in EIA csv

additionalDate = "12/12/2019"
addDayStop = '14' # time to stop on next day (work around for incomplete data)

shiftTime = True # set shifted time start as 0

firstValMatch = True # Ensure that the first data points match (useful in practice?)

## script start
# open file, initialize line outputD, and dataName
file = open(fileName, 'r')
line = next(file)
outputD = {}
dataName = None

# read file, pull data of interest into outputD
for line in reversed(list(open(fileName, 'r'))):
#while line: # from non-reversed file read
    print(line)
    # get data name from file
    if line.split(',')[0] == 'Category':
        dataName = line.split(',')[1].split()[0]
    
    if line.split()[0] == dataDate:
        mwDemand = line.split()[2].split(',')[1]
        mwForcast = line.split()[2].split(',')[2]
        time = line.split()[1].replace('H','')
        if int(time) >= int(dataTimeStart):
            if shiftTime:
                time = str(int(time)-int(dataTimeStart))
                if int(time) < 10:
                    time = '0'+time
            outputD[time] = { 'demand' : mwDemand, 'forcast': mwForcast}

    # Requires file to be read backwards...
    if additionalDate != None:
        if line.split()[0] == additionalDate:
            mwDemand = line.split()[2].split(',')[1]
            mwForcast = line.split()[2].split(',')[2]
            time = str( int(time)+1 )            
            if int(time) < 10:
                time = '0'+time
            if int(line.split()[1].replace('H',''))<= int(addDayStop):
                outputD[time] = { 'demand' : mwDemand, 'forcast': mwForcast}
        
    #line = next(file,  None) # get next line, if there is one - from non-reversed file read

file.close() # close file

# Format data output for verification
print("# Data from: %s %s" %(dataDate, dataName))
outputTuples = ['demand','forcast']
plotD = {}
firstVal = None

for name in outputTuples:
    outputList = []
    time = []
    
    print("%s = [ \n\t#(time , MW data)" % name)
    for entry in sorted(outputD):
        
        if firstVal == None:
            firstVal = int(outputD[entry][name])

        if firstValMatch and len(time) == 0:
            data = firstVal
        else:
            data = int(outputD[entry][name]) 
            
        outputList.append( data )
        time.append(int(entry))
        
        print("\t(%s, %d)," %(entry, data) )
    print("\t]")
    plotD[name] = outputList
    plotD[name+'Time'] = time 

# Output in Percent change from previous value
firstVal = None
print("# Data from: %s %s" %(dataDate, dataName))
for name in outputTuples:
    print("%s = [ \n\t#(time , Precent change from previous value)" % name)
    prevVal = None
    firstCalc = True
    for entry in sorted(outputD):
        
        if firstVal == None:
            # collect first value only once
            firstVal = float(outputD[entry][name])
            
        if prevVal == None:
            prevVal = float(outputD[entry][name])
        
        if firstCalc and firstValMatch:
            curVal = firstVal
            prevVal = firstVal
            firstCalc = False
        else:
            curVal = float(outputD[entry][name])
            
        print("\t(%d, %.3f)," %(int(entry), (curVal-prevVal)/prevVal*100 ) )
        prevVal = curVal
        
    print("\t]")

# make plot
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(plotD['demandTime'],plotD['demand'] , label='Demand')
ax.plot(plotD['forcastTime'],plotD['forcast'], label = 'Forcast')

ax.set_title('Load Forcast and Demand from %s\nStart Time = %s:00 %s '%
             (dataName, dataTimeStart, dataDate))
ax.set_ylabel('MW')
ax.set_xlabel('Time [Hours]')
ax.grid(True)
ax.legend()
ax.set_xlim(min(plotD['demandTime']),max(plotD['demandTime']))

plt.show()
plt.pause(0.00001)