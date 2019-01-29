%%  pgov1_verification.m
%   Thad Haines         Research
%   Program Purpose:    Import data from LTD .mat
%                       Make plots 

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   01/24/19    22:46   init
%   01/25/19    07:30   update of outputs

%% init
clear; format compact; clc; close all; 

%% import LTD data
% load('pgov1Test.mat')
% mir = pgov1Test;
% clear pgov1Test
load('pgov1TestA.mat')
mir = pgov1TestA;
clear pgov1TestA
t_1 = mir.t;
f_1 = mir.f;
N = mir.N
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
subplot 221
hold on
% LTD data
stairs(t_1,mir.A1.S011.S0.Pe,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,mir.A1.G021.G0.Pe,':s','linewidth',1,'color',pltC.dgreen)

stairs(t_1,mir.A1.S011.S0.Pm,':+','linewidth',1.5,'color',pltC.Lblue)
stairs(t_1,mir.A1.G021.G0.Pm,':+','linewidth',1,'color',pltC.grey)

y_label = 'MW';
grid on
set(gca,'FontSize',.85*bfz)
legend({'Gen 1 Pe','Gen 2 Pe','Gen 1 Pm','Gen 2 Pm'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot generator frequency
subplot 222
title_str = 'System Frequency';
hold on
plot(t_1,f_1,':+','linewidth',1.5,'color','k') 

y_label = 'Frequency [pu]';
grid on
set(gca,'FontSize',.85*bfz)
%legend({'Euler'}, ...
%    'Fontsize',bfz*.9,'location',l_loc) % Legend

title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot pslf Voltage
title_str = 'System Powers';
subplot 223
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

%stairs(t_1,mir.A1.S011.Vm,':o','linewidth',1.5,'color',pltC.magenta)
%stairs(t_1,mir.A1.G021.Vm,':s','linewidth',1,'color',pltC.dgreen)

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
    export_fig('XXXXXX','-pdf'); % to print fig
end % end print f