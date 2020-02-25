""" Associated pre-existing code...
Parse timer action string from DTC user input

# related input and other data handling code within software
DTCdict = {
    'bpaTest' : {
        'RefAgents' : {
            'ra1' : 'mirror : f',
            'ra2' : 'gen 2 1 : R', 
            'ra3' : 'gen 2 1 : Pref0',
            'ra4' : 'gen 2 1 : Mbase',
            },# end Referenc Agents
        'TarAgents' : {
            'tar1' : 'gen 2 1 : Pref',
            }, # end Target Agents
        'Timers' : {
            'set' :{ # set Pref
                'logic' : "(ra1 > 0)", # should always eval as true
                'actTime' : 4, # seconds of true logic before act
                'act' : "tar1 = ra3 + (1-ra1)/ra2 * ra4 ", # step 
            },# end set
            'reset' :{ # not used
                'logic' : "0",
                'actTime' : 30, # seconds of true logic before act
                'act' : "0", # set any target On target = 0
            },# end reset
            'hold' : 0, # minimum time between actions
            }, # end timers
        },# end bpaTest
    }# end DTCdict

if actParse[0] in self.tar:
                if type(self.tar[actParse[0]]) != type(None):
                    TA = self.tar[actParse[0]]
                    # actParse[2:] needs to be correctly populated with ra  Vals...

                    updateMSG = TA.setNewAttr(actParse[1] , actParse[2])

def setNewAttr(self, operation, newVAl):
        #Set attribute to newVal via operation returns AMQP update messageexec('self.rtAgent.cv[self.attr]'+ operation + str(newVAl))
        return self.rtAgent.makeAMQPmsg()


Code should be able to parse the input 'act' string

'act' : "tar1 = ra3 + (1-ra1)/ra2 * ra4 ", # step 

and the like, so that TA.setNewAttr(actParse[1] , actParse[2]) <_ should be 2:
works when setNewAttr(self, operation, newVAl):

exec('self.rtAgent.cv[self.attr]'+ operation + str(newVAl))

i.e. 
actParse[1] == operation string
actParse[2:] == newVal == parsed logic string referencing user defined variables

TODO: create input parser / linker that creates a 'nvewVAl' string that can be executed 

ra# is the name of a Reference/Target Agent inside the DTC ra dictionary (likewise wtih tar (Target Agents)

Some useful agent methods may invovle:
GetLinkedVal - used when an ra# is detected -> return a string?
SetLinkedVal - 
Actually already exist inside the DTC

"""
# Actual parseing/linking solution

# test action string via DTC
act = "tar1 = ra14 * ra3 + (1-ra1)/ra2 * ra4 "

# parsing that already happens
actParse = act.split(' ')
targetAtt = actParse[0]
operation = actParse[1]
action = actParse[2:]

# NOTE: splitting string creates list that may not be
# as easy to manipulate as str...

# required checks of action string
tarCheck = 'tar' in act
raCheck = 'ra' in act
print('Action string contains tar variable? ', tarCheck)
print('Action string contains ra variable?  ', raCheck)

# dummy var strings
# in application: values will be gatherd via getSTR methods

tar = {
'tar1' : 'currentPref',
}

ra ={
'ra1': 'omega',
'ra2' : 'droop',
'ra3' : 'Pref0',
'ra4' : 'Mbase',
'ra14' : 'Whoa',
}


# list of tuples for location and name of references/targets
foundNdx = []

#test of enumerate for parse/link action
for ndx, val in enumerate(act):
    print(ndx, val)

    # Target var check
    if val.lower() == 't':
        aCheck = act[ndx+1].lower() == 'a'
        rCheck = act[ndx+2].lower() == 'r'
        digitCheck = act[ndx+3].isdigit()
        try:
            digitCheck2 = act[ndx+4].isdigit() # possible double digit
        except IndexError: # for action ending in tar/ra single digit
            digitCheck2 = False
        
        if all([aCheck,rCheck,digitCheck]):
            if digitCheck2:
                endNdx = ndx+5
                print('Tar found: loc %d:%d'% (ndx,endNdx))
            else:
                endNdx = ndx+4
                print('Tar found: loc %d:%d'% (ndx,endNdx))

            # index found, check if in tar dic
            if act[ndx:endNdx] in tar:
                print('Target %s points to %s' %
                      (act[ndx:endNdx], tar[act[ndx:endNdx]]))
                # create list of tuples for replace vals
                foundNdx.append((act[ndx:endNdx],ndx,endNdx))

    # Reference var check
    if val.lower() == 'r':
        #possible begining of tar variable
        aCheck = act[ndx+1].lower() == 'a'
        digitCheck = act[ndx+2].isdigit()

        try:
            digitCheck2 = act[ndx+3].isdigit() # possible double digit
        except IndexError:
            digitCheck2 = False
        
        
        if all([aCheck,rCheck,digitCheck]):
            if digitCheck2:
                endNdx = ndx+4
                print('Ra found: loc %d:%d'% (ndx,endNdx))
            else:
                endNdx = ndx+3
                print('Ra found: loc %d:%d'% (ndx,endNdx))

            # index found, check if in tar dic
            if act[ndx:endNdx] in ra:
                print('Reference %s points to %s' %
                      (act[ndx:endNdx], ra[act[ndx:endNdx]]))
                # create list of tuples for replace vals
                foundNdx.append((act[ndx:endNdx],ndx,endNdx))

# Found index tuple list foundNdx built, build new string....
#blank string
newAct = ''
refEnd = 0

for tup in foundNdx:
    # Handle assigning index according to foundNdx values
    refStart = tup[1]
    newAct+= act[refEnd:refStart]
    refEnd = tup[2]
    
    # check for targets
    if tup[0][0] == 't':
        # put target value into string
        newAct += tar[tup[0]]

    #check for references
    if tup[0][0] == 'r':
        # put reference value into string
        newAct += ra[tup[0]]

print("input str : %s" % act)
print("output str: %s" % newAct)

# doesn't account for reference/targets not found in dicts...
# will likely cause error due to bad input -> Probably fine


