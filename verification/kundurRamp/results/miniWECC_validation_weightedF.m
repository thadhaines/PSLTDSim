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
PSDSfileName = 'kundur.ramp0.chf'

%% import LTD data
load('miniWECC_loadStep01F.mat')
mir1 = miniWECC_loadStep01F;
clear miniWECC_loadStep01F

load('miniWECC_loadStep02F.mat')
mir2 = miniWECC_loadStep02F;
clear miniWECC_loadStep02F

load('miniWECC_loadStep03F.mat')
mir3 = miniWECC_loadStep03F;
clear miniWECC_loadStep03F

load('miniWECC_loadStep04F.mat')
mir4 = miniWECC_loadStep04F;
clear miniWECC_loadStep04F

%% import PSDS data
psds_data = udread(PSDSfileName,[]);

%cellfun(@disp,psds_data.Name) % display all data types collected from psds
spd_col = jfind(psds_data, 'spd');
v_col = jfind(psds_data, 'v');
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
beta = 15555;
sbase = 100;
deltaP = -1200; % load increase

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
plot(t, psds_data.Data(:,f_col(1))/60,'linewidth',1.5)

for freq=2:max(size(f_col)-1)
    plot(t, psds_data.Data(:,f_col(freq))/60 ,'HandleVisibility','off')
end
plot(mir3.t, mir3.f, 'k:','linewidth',1)
plot(mir3.t, mir3.f, 'w','linewidth',3,'HandleVisibility','off')
plot(t, psds_data.Data(:,f_col(size(f_col,2)))/60,'linewidth',1.5)
plot(mir3.t, mir3.f, 'm-.','linewidth',2)
legend({'PSDS','PSDS','PSDS','LTD 0.5 sec'},'location','southeast')

xlim(x_lim)
%ylim(y_lim)
grid on
title('Comparison of Frequency')
ylabel('Frequency [PU]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% Plot Average System frequency responses
figure('position',ppos)

hold on

plot(mir1.t, mir1.f , 'b-.','linewidth',2)
plot(mir2.t, mir2.f , '--','color',[.7 .7 .7],'linewidth',2)
plot(mir3.t, mir3.f , 'm-.','linewidth',2)
plot(mir4.t, mir4.f , 'k--','linewidth',2)
plot(t, weightedF,'color', [0 1 0],'linewidth',1.5)
line([mir4.t(1) mir4.t(end)],[ssPu,ssPu],'linestyle',':','color',[.3 0 .7],'linewidth',2)


legend({'LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec','Weighted PSDS','Theoretical SS'},'location','southeast')
xlim(x_lim)
%ylim(y_lim)
grid on
title('Comparison of Average System Frequency')
ylabel('Frequency [PU]')
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

