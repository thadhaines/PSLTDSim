%%  miniWeccQuickPlot.m
%   Thad Haines         Research
%   Program Purpose:    Import data from LTD .mat
%                       Make plots 
%                       Attempt at universal plotter

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   02/03/19    hh:mm   init

%% init
clear; format compact; clc; close all; 

%% import LTD data
dataName = 'miniWeccTest02.mat' % 'plotTest01.mat'%
% Assumes 1 generator or load per bus... Dictionary does have info available to allow for better looping

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

%% plot all load power in all areas
figure
title('System P Loading')
hold on
for area = 1:max(size(mir.areaN)) % for each area
    fprintf('area %d\n',mir.areaN(area) )
    curArea = ['A',int2str(area)];
    
    for load = 1:max(size(mir.(curArea).loadBusN))
        curLoad = ['L',int2str(mir.(curArea).loadBusN(load))];
        stairs(mir.t, mir.(curArea).(curLoad).L1.P)
    end
end
clear area curArea areaBus load curLoad

%% plot all gen Pe from all areas
figure
title('System Pe Generated')
hold on
for area = 1:max(size(mir.areaN)) % for each area
    fprintf('area %d\n',mir.areaN(area) )
    curArea = ['A',int2str(area)];
    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        stairs(mir.t, mir.(curArea).(curGen).G1.Pe)
    end
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curGen = ['S',int2str(mir.(curArea).slackBusN(slack))];
        stairs(mir.t, mir.(curArea).(curGen).S1.Pe)
    end
end
clear area curArea gen curGen

%% plot all gen Q from all areas
figure
title('System Q Generated')
hold on
for area = 1:max(size(mir.areaN)) % for each area
    fprintf('area %d\n',mir.areaN(area) )
    curArea = ['A',int2str(area)];
    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        stairs(mir.t, mir.(curArea).(curGen).G1.Q)
    end
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curGen = ['S',int2str(mir.(curArea).slackBusN(slack))];
        stairs(mir.t, mir.(curArea).(curGen).S1.Q)
    end
end
clear area curArea gen curGen

%% plot all bus voltages from all areas
figure
subplot(2, 1, 1)
title('System Bus Voltages')
hold on
for area = 1:max(size(mir.areaN)) % for each area
    fprintf('area %d\n',mir.areaN(area) )
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(slack))];
        stairs(mir.t, mir.(curArea).(curGen).Vm)
    end    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        stairs(mir.t, mir.(curArea).(curGen).Vm)
    end
    for load = 1:max(size(mir.(curArea).loadBusN))
        curLoad = ['L',int2str(mir.(curArea).loadBusN(load))];
        stairs(mir.t, mir.(curArea).(curLoad).Vm)
    end
    for xbus = 1:max(size(mir.(curArea).xBusN))
        curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
        stairs(mir.t, mir.(curArea).(curXbus).Vm)
    end
end

subplot(2, 1, 2)
title('System Bus Angles')
hold on
for area = 1:max(size(mir.areaN)) % for each area
    fprintf('area %d\n',mir.areaN(area) )
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(slack))];
        stairs(mir.t, rad2deg(mir.(curArea).(curGen).Va))
    end    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        stairs(mir.t, rad2deg(mir.(curArea).(curGen).Va))
    end
    for load = 1:max(size(mir.(curArea).loadBusN))
        curLoad = ['L',int2str(mir.(curArea).loadBusN(load))];
        stairs(mir.t, rad2deg(mir.(curArea).(curLoad).Va))
    end
    for xbus = 1:max(size(mir.(curArea).xBusN))
        curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
        stairs(mir.t, rad2deg(mir.(curArea).(curXbus).Va))
    end
end
clear area curArea slack gen load xbus curLoad curXbus curGen