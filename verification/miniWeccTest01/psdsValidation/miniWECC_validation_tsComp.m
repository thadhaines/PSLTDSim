%%  miniWECC_validation.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD miniWECC results with PSDS

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   05/06/19    14:44   init
%   05/14/19    14:03   added automatic LTD timestep accounting
%   05/15/19    11:19   New plots to compare timestep

%% init
clear; format compact; clc; close all;
format long;

%% Knowns
PSDSfileName = 'miniWECC_loadStep.chf'

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

%% Plot parameters
ppos = [18 521 1252 457];
x_lim = [mir1.t(1), mir1.t(end)];
bfz = 13;
%% Plot all frequency responses and LTD on top
figure('position',ppos)
axes('ColorOrder',flipud(imcomplement(colormap(spring)))) % to make mess of lines look nicer
hold on
plot(t, psds_data.Data(:,f_col(1))/60,'linewidth',1.5)

for freq=2:max(size(f_col)-1)
    plot(t, psds_data.Data(:,f_col(freq))/60 ,'HandleVisibility','off')
end
plot(mir4.t, mir4.f, 'k:','linewidth',1)
plot(mir4.t, mir4.f, 'w','linewidth',3,'HandleVisibility','off')
plot(t, psds_data.Data(:,f_col(size(f_col,2)))/60,'linewidth',1.5)
plot(mir4.t, mir4.f, 'm-.','linewidth',2)
legend({'PSDS','PSDS','PSDS','LTD'},'location','southeast')

xlim(x_lim)
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
plot(t, fAve,'color', [0 1 0],'linewidth',1.5)

legend({'LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec','PSDS'},'location','southeast')
xlim(x_lim)
grid on
title('Comparison of Average System Frequency')
ylabel('Frequency [PU]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

%set(gcf,'color','w'); % to remove border of figure
%export_fig('XXXXXX','-pdf'); % to print fig