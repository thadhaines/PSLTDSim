%%  PSDS_LTD_validator.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations of various time steps to
%                       results generated from PSDS. PDSS results are in a
%                       .chf file and have one fmeta and vmeta that
%                       captures data from all areas.

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   06/04/19    14:15   init - plots formatted
%   06/05/19    12:40   Added handling of plotting only unique bus voltages
%   06/05/19    12:46   Added LTD and PSDS to voltage, p, and q plots
%   06/05/19    12:56   Added comparison of Pm plot

%% init
clear; format compact; clc; close all;
format long;

%% Knowns
PSDSfileName = 'kundur.step0.chf'
LTDCaseName = 'kundurStep'

% PSDSfileName = 'kundur.ramp0.chf'
% LTDCaseName = 'kundurRamp'

% PSDSfileName = 'kundur.gentrip0.chf'
% LTDCaseName = 'kundurGenTrip0'

plotTheoSS = 0; % use for steps only - requires manual calcs of beta, MW delta
%% import LTD data in an automatic way
cases = {[LTDCaseName,'0F'],
    [LTDCaseName,'1F'],
    [LTDCaseName,'2F'],
    [LTDCaseName,'3F'],
    }

load(cases{1}) % 2 sec
mir1 = eval(cases{1});
clear eval(cases{1})

load(cases{2}) % 1 sec
mir2 = eval(cases{2});
clear eval(cases{2})

load(cases{3}) % 0.5 sec
mir3 = eval(cases{3});
clear eval(cases{3})

load(cases{4}) % 1 sec
mir4 = eval(cases{4});
clear eval(cases{4})

mir = mir2; % for comparison plots
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
Hsys = mir.Hsys
weightedF = zeros(size(psds_data.Data(:,1),1),1);
debug = 1;
for area = 1:max(size(mir.areaN)) % for each area
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

%% Calculate theoretical ss
% only useful for step tests
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
x_lim = [mir.t(1), mir.t(end)];
y_lim = [.9975,1];
bfz = 13;

%% Plot all frequency responses and LTD on top
figure('position',ppos)
axes('ColorOrder',flipud(imcomplement(colormap(spring(max(size(f_col))))))) % to make mess of lines look nicer
hold on
plot(t, psds_data.Data(:,f_col(1)),'linewidth',1.5)

for freq=2:max(size(f_col)-1)
    plot(t, psds_data.Data(:,f_col(freq)) ,'HandleVisibility','off')
end

plot(mir3.t, mir3.f*60, 'w','linewidth',3,'HandleVisibility','off')
plot(t, psds_data.Data(:,f_col(size(f_col,2))),'linewidth',1.5)
plot(mir3.t, mir3.f*60, 'm-.','linewidth',2)
legend({'PSDS','PSDS','LTD 0.5 sec'},'location','southeast')

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

if plotTheoSS
    line([mir4.t(1) mir4.t(end)],[ssPu,ssPu]*60,'linestyle',':','color',[.3 0 .7],'linewidth',2)
end

legend({'Weighted PSDS','LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec','Theoretical SS'},'location','southeast')
xlim(x_lim)
%ylim(y_lim)
grid on
title('Comparison of Average System Frequency')
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% split out PSDS data corresponding to LTD points and plot Hz difference
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

%% Voltage Comparison
figure('position',ppos)
legNames = {};

hold on
for bv=1:max(size(v_col))
    plot(t, psds_data.Data(:,v_col(bv)))
    temp = strsplit(psds_data.Description{v_col(bv)});
    legNames{end+1} = ['PSDS ', temp{1}];
end


makeLegend = 1
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    uniqueEntry = unique(mir.(curArea).slackBusN);
    for slack = 1:max(size(mir.(curArea).slackBusN))
        if ismember(mir.(curArea).slackBusN(slack),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).slackBusN(slack)) = [];
            curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
            plot(mir.t, mir.(curArea).(curSlack).Vm,'-o')
            name = [(curArea),'.',(curSlack)];
            legNames{end+1} = ['LTD ',name];
        end
    end
    uniqueEntry = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(mir.(curArea).genBusN))
        if ismember(mir.(curArea).genBusN(gen),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).genBusN(gen)) = [];
            curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
            plot(mir.t, mir.(curArea).(curGen).Vm,'-o')
            name = [(curArea),'.',(curGen)];
            legNames{end+1} = ['LTD ',name];
        end
    end
    uniqueEntry = unique(mir.(curArea).loadBusN);
    for load = 1:max(size(mir.(curArea).loadBusN))
        if ismember(mir.(curArea).loadBusN(load),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).loadBusN(load)) = [];
            curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
            plot(mir.t, mir.(curArea).(curLoadbus).Vm,'x')
            name = [(curArea),'.',(curLoadbus)];
            legNames{end+1} = ['LTD ',name];
        end
    end
    uniqueEntry = unique(mir.(curArea).xBusN);
    for xbus = 1:max(size(mir.(curArea).xBusN))
        % remove number from unique
        if ismember(mir.(curArea).xBusN(xbus),uniqueEntry)
            uniqueEntry(uniqueEntry == mir.(curArea).xBusN(xbus)) = [];
            curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
            plot(mir.t, mir.(curArea).(curXbus).Vm,'s')
            name = [(curArea),'.',(curXbus)];
            legNames{end+1} = ['LTD ',name];
        end
    end
end
if makeLegend
    legend(legNames)
    grid on
end
grid on
title('Comparison of Bus Voltage')
xlabel('Time [sec]')
ylabel('Voltage [pu]')
set(gca,'fontsize',bfz)
xlim(x_lim)

%% Pe  Comparison
figure('position',ppos)
legNames ={};
hold on
for curCol=1:max(size(pg_col))
    plot(t, psds_data.Data(:,pg_col(curCol)))
    temp = strsplit(psds_data.Description{pg_col(curCol)});
    legNames{end+1} = ['PSDS ', temp{1}];
end

hold on

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Pe,'-o')
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['LTD ',name];
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        
        plot(mir.t, mir.(curArea).(curGen).G1.Pe,'-o')
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = ['LTD ',name];
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
title('Comparison of Real Power Output')
xlabel('Time [sec]')
ylabel('Power [MW]')
set(gca,'fontsize',bfz)
xlim(x_lim)

%% Pe  Comparison
figure('position',ppos)
legNames ={};
hold on
for curCol=1:max(size(pm_col))
    plot(t, psds_data.Data(:,pm_col(curCol)))
    temp = strsplit(psds_data.Description{pm_col(curCol)});
    legNames{end+1} = ['PSDS ', temp{1}];
end

hold on

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Pm,'-o')
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['LTD ',name];
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        
        plot(mir.t, mir.(curArea).(curGen).G1.Pm,'-o')
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = ['LTD ',name];
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
title('Comparison of Mechanical Power Output')
xlabel('Time [sec]')
ylabel('Power [MW]')
set(gca,'fontsize',bfz)
xlim(x_lim)

%% Q Comparison
figure('position',ppos)
legNames = {};
hold on
for curCol=1:max(size(qg_col))
    plot(t, psds_data.Data(:,qg_col(curCol)),'-')
    temp = strsplit(psds_data.Description{qg_col(curCol)});
    legNames{end+1} = ['PSDS ', temp{1}];
end
hold on

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Q,'-s')
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['LTD ',name];
    end
    
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        plot(mir.t, mir.(curArea).(curGen).G1.Q,'-s')
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = ['LTD ',name];
        
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
title('Comparison of Reactive Power Output')
xlabel('Time [sec]')
ylabel('Reactive Power [MVAR]')
set(gca,'fontsize',bfz)
xlim(x_lim)

%% pdf output code
%set(gcf,'color','w'); % to remove border of figure
%export_fig('XXXXXX','-pdf'); % to print fig