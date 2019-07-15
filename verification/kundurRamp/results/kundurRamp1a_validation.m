%%  miniWECC_validation_weightedF.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD miniWECC results with PSDS

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   05/22/19    14:57   init - attempt at weighted f

%% init
clear; format compact; clc; close all;
format long;

%% Knowns
PSDSfileName = 'kundur.ramp01a.chf'

%% import LTD data
load('kundurRamp01aF') % 2 sec
mir1 = kundurRamp0F;
clear kundurRamp0F

load('kundurRamp11aF') % 1 sec
mir2 = kundurRamp1F;
clear kundurRamp1F

load('kundurRamp21aF') % .5 sec
mir3 = kundurRamp2F;
clear kundurRamp2F

load('kundurRamp31aF') % .25 sec
mir4 = kundurRamp3F;
clear kundurRamp3F

%% import PSDS data
psds_data = udread(PSDSfileName,[]);

%cellfun(@disp,psds_data.Name) % display all data types collected from psds
spd_col = jfind(psds_data, 'spd');
v_col = jfind(psds_data, 'vmeta');
pg_col = jfind(psds_data, 'pg');
pm_col = jfind(psds_data, 'pm'); % governor pm output
qg_col = jfind(psds_data, 'qg');
f_col = jfind(psds_data, 'fbu');
t = psds_data.Data(:,1); % PSDS time

%% sum and average PSDS frequency data
N = max(size(f_col)); %number of frequencies to sum
fAve = psds_data.Data(:,f_col(1));
for freq=2:max(size(f_col))
    fAve = fAve + psds_data.Data(:,f_col(freq));
end
fAve = fAve/N/60; % as PU

%% Calculate weighted freq
mir = mir1;
Hsys = mir.Hsys
weightedF = zeros(size(psds_data.Data(:,1),1),1);
debug = 1;
for area = 1:max(size(mir1.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        psdsName = mir.(curArea).(curSlack).BusName;
        weight = mir.(curArea).(curSlack).S1.Hpu*mir.(curArea).(curSlack).S1.Mbase;
        a = jfind(psds_data, psdsName);
        genFloc = intersect(a,f_col);
        if size(genFloc,2) >1
            disp(psdsName) % prints name with multi intersections 
        end
        genSpd = psds_data.Data(:,genFloc(1)).*(weight/Hsys/60);
        weightedF = weightedF + genSpd;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        psdsName = [int2str(mir.(curArea).genBusN(gen)),':',mir.(curArea).(curGen).BusName];
        weight = mir.(curArea).(curGen).G1.Hpu*mir.(curArea).(curGen).G1.Mbase;
        a = jfind(psds_data, psdsName);
        genFloc = intersect(a,f_col);
        if size(genFloc,2) >1
            disp(psdsName) % prints name with multi intersections 
        end
        genSpd = psds_data.Data(:,genFloc(1)).*(weight/Hsys/60);
        weightedF = weightedF + genSpd;
    end
    
end
% figure
% plot(t, weightedF)
% hold on
% plot(t, fAve)
% legend('Weighted Average','Average')
%% Calculate theoretical ss
beta = 585;
sbase = 100;
deltaP = -270; % load increase

deltaFpu = deltaP/sbase*(1/beta);
ssPu = 1 + deltaFpu
ssF = ssPu*60;
% calculate error for each
PSDSerr = (weightedF(end)-ssPu)*60
mir20err = (mir1.f(end)-ssPu)*60
mir10err = abs(mir2.f(end)-ssPu)*60
mir05err = abs(mir3.f(end)-ssPu)*60
mir02err = abs(mir4.f(end)-ssPu)*60

%% Plot parameters
ppos = [18 521 1252 373];
x_lim = [mir1.t(1), mir1.t(end)];
y_lim = [.9975,1];
bfz = 13;
%% Plot all frequency responses and LTD on top
figure('position',ppos)
axes('ColorOrder',flipud(imcomplement(colormap(spring)))) % to make mess of lines look nicer
hold on
plot(t, psds_data.Data(:,f_col(1)),'linewidth',1.5)
hold on
for freq=2:max(size(f_col)-1)
    plot(t, psds_data.Data(:,f_col(freq)) ,'HandleVisibility','off')
end
plot(mir3.t, mir3.f*60, 'k:','linewidth',1)
plot(mir3.t, mir3.f*60, 'w','linewidth',3,'HandleVisibility','off')
plot(t, psds_data.Data(:,f_col(size(f_col,2))),'linewidth',1.5)
plot(mir3.t, mir3.f*60, 'm-.','linewidth',2)
legend({'PSDS','PSDS','PSDS','LTD 0.5 sec'},'location','southeast')

xlim(x_lim)
%ylim(y_lim)
grid on
title('Comparison of Frequency')
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% Plot Average System frequency responses
figure('position',ppos)

hold on
plot(t, weightedF*60,'color', [0 1 0],'linewidth',1.5)
plot(mir1.t, mir1.f*60 , 'b-.','linewidth',2)
plot(mir2.t, mir2.f*60 , '--','color',[.7 .7 .7],'linewidth',2)
plot(mir3.t, mir3.f*60 , 'm-.','linewidth',2)
plot(mir4.t, mir4.f*60 , 'k--','linewidth',2)

line([mir4.t(1) mir4.t(end)],[ssPu,ssPu]*60,'linestyle',':','color',[.3 0 .7],'linewidth',2)


legend({'Weighted PSDS','LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec','Theoretical SS'},'location','southeast')
xlim(x_lim)
%ylim(y_lim)
grid on
title('Comparison of Average System Frequency')
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% split out PSDS data corresponding to LTD points
% find index of t == 0 in PSLF data
n = 1;
while t(n) ~= 0
    n = n+1;
end
zoft = n; % location of 0 in PSLF data
% first time step from zero used for indexing

mirA = [mir1,mir2,mir3,mir4];
for mirror=1:size(mirA,2)
    LTD_ts = mirA(mirror).t(2);
    ts = t(zoft+1);
    fs = round(LTD_ts/ts);
    
    % Collect PSLF data corresponding to LTD data
    ct = 0;
    while ct<=mirA(mirror).t(end)/LTD_ts
        % find index of time at full second
        n = zoft + fs*ct;
        % pull values
        pulledtime(ct+1) = t(n);
        pulledf(ct+1) = weightedF(n); % system 'mean'
        ct = ct+1;
    end
    
    mirA(mirror).PSDSf = pulledf;
    mirA(mirror).PSDSt = pulledtime;
    clear pulledtime pulledf
end

figure('position',ppos)
hold on
plot(mirA(1).t, abs(mirA(1).f -mirA(1).PSDSf)*60, 'b','linewidth',.5)
plot(mirA(2).t, abs(mirA(2).f -mirA(2).PSDSf)*60,'color',[.7 .7 .7],'linewidth',1)
plot(mirA(3).t, abs(mirA(3).f -mirA(3).PSDSf)*60, 'm','linewidth',.5)
plot(mirA(4).t, abs(mirA(4).f -mirA(4).PSDSf)*60, 'k','linewidth',.5)
legend({'LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec'},'location','northeast')
xlim(x_lim)
grid on
title('Comparison of Absolute Frequency Deviation from PSDS')
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)
%set(gcf,'color','w'); % to remove border of figure
%export_fig('XXXXXX','-pdf'); % to print fig

%% Voltage Comparison
figure

plot(t, psds_data.Data(:,v_col(1)))
hold on
for bv=2:max(size(v_col)-1)
    plot(t, psds_data.Data(:,v_col(bv)) ,'HandleVisibility','off')
end
mir = mir2;
legNames = {};
makeLegend = 1
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).Vm)
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        plot(mir.t, mir.(curArea).(curGen).Vm,'o')
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = name;
    end
    for load = 1:max(size(mir.(curArea).loadBusN))
        curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
        plot(mir.t, mir.(curArea).(curLoadbus).Vm,'x')
        name = [(curArea),'.',(curLoadbus)];
        legNames{end+1} = name;
    end
    for xbus = 1:max(size(mir.(curArea).xBusN))
        curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
        plot(mir.t, mir.(curArea).(curXbus).Vm,'s')
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

%% P  Comparison
figure

plot(t, psds_data.Data(:,pg_col(1)))
hold on
for curCol=2:max(size(pg_col))
    plot(t, psds_data.Data(:,pg_col(curCol)) ,'HandleVisibility','off')
end

hold on
legNames ={};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Pe)
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        
        plot(mir.t, mir.(curArea).(curGen).G1.Pe)
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
%% Q Comparison
figure

plot(t, psds_data.Data(:,qg_col(1)))
hold on
for curCol=2:max(size(qg_col))
    plot(t, psds_data.Data(:,qg_col(curCol)) ,'HandleVisibility','off')
end
hold on
legNames = {};
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Q)
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        plot(mir.t, mir.(curArea).(curGen).G1.Q)
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