%%  rampTgov1_validation.m
%   Thad Haines         Research
%   Program Purpose:    Import data from LTD .mat
%                       Make plots to compare PSLF vs LTD data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   03/26/19    15:25   init - attempt to verify Ramp data and tgov 1
%   03/26/19    20:00   success of plotting pgov1 ramp data

%% init
clear; format compact; clc; %close all; 

%% import LTD data
load('stepsTgov101F.mat')
mir = stepsTgov101F;
clear stepsTgov101F

t_1 = mir.t;
f_1 = mir.f;
N = mir.N

%% import pslf data
pslf_data = udread('ee554.steps.chf',[]);
cellfun(@disp,pslf_data.Name)

spd_col = jfind(pslf_data, 'spd')
v_col = jfind(pslf_data, 'v')
pg_col = jfind(pslf_data, 'pg')
qg_col = jfind(pslf_data, 'qg')
f_col = jfind(pslf_data, 'fbu')

t = pslf_data.Data(:,1);
%% sum and average PSLF frequency data
N = max(size(f_col)); %number of frequencies to sum
fAve = pslf_data.Data(:,f_col(1));
for freq=2:max(size(f_col))
    fAve = fAve + pslf_data.Data(:,f_col(freq));
end
fAve = fAve/N;

%% plot definitions
xlimit = [0,60]
p_pos = [400 200 1421 734];
bfz = 15;
l_loc = 'best';
print_f = 0;

%% Color definitions
pltC.grey = [.7, .7, .7];
pltC.magenta = [1 0 1];
pltC.green = [8.6 91.8 0]./100;
pltC.Lblue = [0 .5 1];
pltC.dgreen = pltC.grey.*pltC.green;

%% plot pslf real power generated
figure('pos',p_pos)
title_str = 'Generator Power Distribution';
subplot(2, 2, [1 2])
hold on
% PSLF data
plot(t,pslf_data.Data(:,pg_col(1)),'-','linewidth',3,'color',pltC.grey)
plot(t,pslf_data.Data(:,pg_col(2)),'linewidth',1,'color',[0,0,0])

%LTD data
plot(t_1,mir.A1.S11.S1.Pe,':o','linewidth',1.5,'color',pltC.magenta)
plot(t_1,mir.A1.G21.G1.Pe,':s','linewidth',1,'color',pltC.dgreen)

plot(t_1,mir.A1.S11.S1.Pm,':+','linewidth',1.5,'color',pltC.Lblue)
plot(t_1,mir.A1.G21.G1.Pm,':+','linewidth',1,'color','k')
xlim(xlimit)

y_label = 'MW';
grid on
ax = gca;
ax.GridColor = [.65 .65 .65];  % [R, G, B];
ax.YMinorGrid = 'on';
ax.YMinorTick = 'on';
ax.GridAlpha = 1;

set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','Gen 1 Pe','Gen 2 Pe','Gen 1 Pm','Gen 2 Pm'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)
%ylim([49.3, 51.4])


%% plot generator frequency
subplot(2, 2, [3 4])
title_str = 'System Frequency';
hold on
plot(t,fAve/60,'linewidth',2,'color',pltC.magenta)
plot(t_1,f_1,':+','linewidth',1.5,'color','k') 

xlim(xlimit)
y_label = 'Frequency [pu]';

grid on
ax = gca;
ax.GridColor = [.65 .65 .65];  % [R, G, B];
ax.YMinorGrid = 'on';
ax.YMinorTick = 'on';
ax.GridAlpha = 1;

set(gca,'FontSize',.85*bfz)
legend({'PSLF mean','LTD'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend

title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)
