%%  miniWeccQuickPlot.m
%   Thad Haines         Research
%   Program Purpose:    Import data from LTD .mat
%                       Make plots
%                       Attempt at universal plotter

%
%   History:
%   02/03/19    14:05   init
%   02/03/19    14:05   addition of multiple loads and legend
%   02/04/19    18:40   correction of slack info, more legends
%   02/13/19    14:40   addition of x,y labels.

%% init
clear; format compact; clc; close all;

%% Global Flags
makeLegend = 1;
debug = 0;

%% import LTD data = Only field that requires user editing 
dataName = 'plotTest01.mat'% 'miniWeccTest02.mat' % 

% Assumes 1 generator or load per bus... 
% Dictionary does have info available to allow for better looping
% TODO: add functionality to loop though multiple gens per bus

%% Handle data in a universal way
load(dataName)
dataName = strsplit(dataName,'.');
% universalise input
mir = eval(dataName{1});
clear -regexp \d % clear any variable with number in name (assumes data will)
clear dataName

%% plot system frequency
figure
title('System Frequency')
hold on
plot(mir.t,mir.f)
grid on
xlabel('Time [sec]')
ylabel('Frequency [pu]')

%% plot all load power in all areas with state == 1
figure
title('System P Loading')
hold on
legNames = {};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for load = 1:max(size(mir.(curArea).loadBusN))-1
        curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
        if debug
            disp(curLoadbus)
        end
        for loadOnBus = 1:mir.(curArea).(curLoadbus).Nload
            if debug
                disp(loadOnBus)
            end
            curLoad =['L',int2str(loadOnBus)];
            P = mir.(curArea).(curLoadbus).(curLoad).P;
            St = double(mir.(curArea).(curLoadbus).(curLoad).St);
            name = [(curArea),'.',(curLoadbus),'.',(curLoad)];
            legNames{end+1} = name;
            stairs(mir.t, P.*St)
        end
    end
end
if makeLegend
    legend(legNames)
end
grid on
xlabel('Time [sec]')
ylabel('Load [MW]')
clear area curArea areaBus load curLoad P St curLoadbus loadOnBus name legNames

%% plot all gen Pe from all areas
figure
title('System Pe Generated')
hold on
legNames ={};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        stairs(mir.t, mir.(curArea).(curSlack).S1.Pe)
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        
        stairs(mir.t, mir.(curArea).(curGen).G1.Pe)
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = name;
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
xlabel('Time [sec]')
ylabel('Power [MW]')
clear area curArea gen curGen slack curSlack legNames name

%% plot all gen Q from all areas
figure
title('System Q Generated')
hold on
legNames = {};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        stairs(mir.t, mir.(curArea).(curSlack).S1.Q)
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        stairs(mir.t, mir.(curArea).(curGen).G1.Q)
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = name;
        
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
xlabel('Time [sec]')
ylabel('Reactive Power [MVAR]')
clear area curArea gen curGen slack curSlack legNames name

%% plot all bus voltages from all areas
figure
subplot(2, 1, 1)
title('System Bus Voltages')
hold on
legNames = {};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        stairs(mir.t, mir.(curArea).(curSlack).Vm)
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        stairs(mir.t, mir.(curArea).(curGen).Vm)
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = name;
    end
    for load = 1:max(size(mir.(curArea).loadBusN))
        curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
        stairs(mir.t, mir.(curArea).(curLoadbus).Vm)
        name = [(curArea),'.',(curLoadbus)];
        legNames{end+1} = name;
    end
    for xbus = 1:max(size(mir.(curArea).xBusN))
        curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
        stairs(mir.t, mir.(curArea).(curXbus).Vm)
        name = [(curArea),'.',(curXbus)];
        legNames{end+1} = name;
    end
end
if makeLegend
    legend(legNames)
    grid on
end
grid on
xlabel('Time [sec]')
ylabel('Voltage [pu]')

% Angle Plot
subplot(2, 1, 2)
title('System Bus Angles')
hold on
legNames ={};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        stairs(mir.t, rad2deg(mir.(curArea).(curSlack).Va))
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        stairs(mir.t, rad2deg(mir.(curArea).(curGen).Va))
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = name;
    end
    for load = 1:max(size(mir.(curArea).loadBusN))
        curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
        stairs(mir.t, rad2deg(mir.(curArea).(curLoadbus).Va))
        name = [(curArea),'.',(curLoadbus)];
        legNames{end+1} = name;
    end
    for xbus = 1:max(size(mir.(curArea).xBusN))
        curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
        stairs(mir.t, rad2deg(mir.(curArea).(curXbus).Va))
        name = [(curArea),'.',(curXbus)];
        legNames{end+1} = name;
    end
end

if makeLegend
    legend(legNames)
end
grid on
xlabel('Time [sec]')
ylabel('Angle [degree]')

clear area curArea slack gen load xbus curLoad curLoadbus curXbus curGen curSlack legNames name