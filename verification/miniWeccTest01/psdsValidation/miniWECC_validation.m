%%  miniWECC_validation.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD miniWECC results with PSDS

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   05/06/19    14:44   init

%% init
clear; format compact; clc; close all;

%% Knowns
LTDfileName = 'miniWECC_loadStep01F.mat'
PSDSfileName = 'miniWECC_loadStep.chf'

%% import LTD data
dataName = LTDfileName(1:size(LTDfileName,2)-4); % remove .mat
load(LTDfileName);
mir = eval(dataName); % set data as common name

%% import PSDS data
psds_data = udread('miniWECC_loadStep.chf',[]);
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

%% split out PSDS data corresponding to LTD points
% find index of t == 0 in PSLF data
n = 1;
while t(n) ~= 0
	n = n+1;
end
zoft = n; % location of 0 in PSLF data
% first time step from zero used for indexing
ts = t(zoft+1); 
fs = round(1/ts);

% Collect PSLF data corresponding to LTD data
for ct=0:mir.t(end)
    % find index of time at full second
    n = zoft + fs*ct;
    % pull values
    pulledtime(ct+1) = t(n);
    pulledf(ct+1) = fAve(n); % system 'mean'
end

%% Plot parameters
ppos = [18 521 1252 457];
x_lim = [mir.t(1), mir.t(end)];
bfz = 13;
%% Plot all frequency responses and LTD on top
figure('position',ppos)
axes('ColorOrder',flipud(imcomplement(colormap(spring)))) % to make mess of lines look nicer
hold on
plot(t, psds_data.Data(:,f_col(1))/60,'linewidth',1.5)


for freq=2:max(size(f_col)-1)
    plot(t, psds_data.Data(:,f_col(freq))/60 ,'HandleVisibility','off')
end
plot(mir.t, mir.f, 'k:','linewidth',1)
plot(mir.t, mir.f, 'w','linewidth',3,'HandleVisibility','off')
plot(t, psds_data.Data(:,f_col(size(f_col,2)))/60,'linewidth',1.5)
plot(mir.t, mir.f, 'm-.','linewidth',2)
legend({'PSDS','PSDS','PSDS','LTD'},'location','southeast')

xlim(x_lim)
grid on
title('Comparison of Frequency')
ylabel('Frequency [PU]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% Plot Average System frequency responses
figure('position',ppos)
plot(t, fAve,'color', [0 1 0],'linewidth',1.5)
hold on

plot(mir.t, mir.f , 'm-.','linewidth',2)

legend({'PSDS Average','LTD'},'location','southeast')
xlim(x_lim)
grid on
title('Comparison of Average System Frequency')
ylabel('Frequency [PU]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% Plot of relative difference
relDif = (mir.f - pulledf)./pulledf*100; % as a percent

figure('position',ppos)
hold on
plot(mir.t, abs(relDif),'ko-.')
xlim(x_lim)
grid on
title('Absolute Relative Percent Difference (PSDS-LTD)')
ylabel('Relative Difference [%]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%% Experimental pm plotting
figure
subplot(2,1,1)
set(gca,'ColorOrder',colormap(cool))
set(gca,'ColorOrderIndex',30)

hold on
for mach=1:max(size(pm_col))
    plot(t, psds_data.Data(:,pm_col(mach))/psds_data.Data(1,pm_col(mach)) ,'HandleVisibility','off')
end
xlim(x_lim)
title('Normalized PSDS Generator Pm')
%

subplot(2,1,2)
set(gca,'ColorOrder',colormap(cool))
set(gca,'ColorOrderIndex',30)
hold on
legNames ={};
for area = 1:max(size(mir.areaN)) % for each area

    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Pm/mir.(curArea).(curSlack).S1.Pm(1))
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = name;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        
        plot(mir.t, mir.(curArea).(curGen).G1.Pm/mir.(curArea).(curGen).G1.Pm(1) )
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = name;
    end
    %legend(legNames)
end
xlim(x_lim)
title('Normalized LTD Generator Pm')
%set(gcf,'color','w'); % to remove border of figure
%export_fig('XXXXXX','-pdf'); % to print fig