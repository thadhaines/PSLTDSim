%%  pgov1_verification3.m
%   Thad Haines         Research
%   Program Purpose:    Import data from LTD .mat
%                       Make plots 

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   01/24/19    22:46   init
%   01/25/19    07:30   update of outputs
%   01/28/19    16:30   update to compare PSLF to LTD gov steps of 1 MW

%% init
clear; format compact; clc; close all; 

%% import LTD data
load('pgov1TestIAB1.mat')
mir = pgov1TestIAB1;
clear pgov1TestIAB1

t_1 = mir.t;
f_1 = mir.f;
N = mir.N

%% import pslf data
pslf_data = udread('ee554.exc.3.chf',[]);
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

% LTD data
stairs(t_1,mir.A1.S011.S0.Pe,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,mir.A1.G021.G0.Pe,':s','linewidth',1,'color',pltC.dgreen)

stairs(t_1,mir.A1.S011.S0.Pm,':+','linewidth',1.5,'color',pltC.Lblue)
stairs(t_1,mir.A1.G021.G0.Pm,':+','linewidth',1,'color','k')
xlim([0, 60])

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
ylim([49.3, 51.4])
%% plot generator frequency
subplot(2, 2, [3 4])
title_str = 'System Frequency';
hold on
plot(t,fAve/60,'linewidth',2,'color',pltC.magenta)
stairs(t_1,f_1,':+','linewidth',1.5,'color','k') 

xlim([0,60])
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
%{
% Older plots
%% plot pslf Voltage
title_str = 'System Powers';
subplot 2 2 [1 2]
hold on
%LTD data
stairs(t_1,mir.Pload,':o','linewidth',1.5,'color',pltC.grey)
stairs(t_1,mir.Pe,'--','linewidth',1.5,'color','k')
stairs(t_1,mir.Pacc,':s','linewidth',1,'color',pltC.dgreen)
stairs(t_1,mir.Pm,':o','linewidth',1.5,'color',pltC.Lblue)

y_label = 'MW';
grid on
set(gca,'FontSize',.85*bfz)
legend({'P Load','Pe','P acc','Pm'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot pslf q power generated
subplot 224
hold on
stairs(t_1,mir.A1.S011.S0.Q,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,mir.A1.G021.G0.Q,':s','linewidth',1,'color',pltC.dgreen)

%plot(t_1,mir.A1.S011.Vm,':o','linewidth',1.5,'color',pltC.magenta)
%plot(t_1,mir.A1.G021.Vm,':s','linewidth',1,'color',pltC.dgreen)

title_str = 'Generator Reactive Power';
y_label = 'MVAR';

grid on
set(gca,'FontSize',.85*bfz)
legend({'Gen 1 Q','Gen 2 Q','Gen 1 V','Gen 2 V'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

set(gcf,'Position',p_pos)
%% pdf out
if print_f == 1
    set(gcf,'color','w'); % to remove border of figure
    export_fig('pgov1IAB2','-pdf'); % to print fig
end % end print f
%}