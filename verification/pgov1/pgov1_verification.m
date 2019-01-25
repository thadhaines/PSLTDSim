%%  pgov1_verification.m
%   Thad Haines         Research
%   Program Purpose:    Import data from LTD .mat
%                       Make plots 

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   01/24/19    22:46   init

%% init
clear; format compact; clc; close all; 

%% import LTD data
load('pgov1Test.mat')
mir = pgov1Test;
clear pgov1Test
t_1 = mir.t;
f_1 = mir.f;

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
title_str = 'Real Power Generated';
subplot 221
hold on
% LTD data
stairs(t_1,mir.A1.S011.S0.Pe,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,mir.A1.G021.G0.Pe,':s','linewidth',1,'color',pltC.dgreen)


y_label = 'MW';
grid on
set(gca,'FontSize',.85*bfz)
legend({'LTD Gen 1','LTD Gen 2'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot generator frequency
subplot 222
title_str = 'Generator Frequency';
hold on
plot(t_1,f_1,':o','linewidth',1.5,'color',pltC.magenta) 

y_label = 'Frequency [pu]';
grid on
set(gca,'FontSize',.85*bfz)
%legend({'Euler'}, ...
%    'Fontsize',bfz*.9,'location',l_loc) % Legend

title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot pslf Voltage
title_str = 'Mechanical Power Generated';
subplot 223
hold on
%LTD data
stairs(t_1,mir.A1.S011.S0.Pm,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,mir.A1.G021.G0.Pm,':s','linewidth',1,'color',pltC.dgreen)

y_label = 'Voltage [pu]';
grid on
set(gca,'FontSize',.85*bfz)
legend({'LTD Gen 1','LTD Gen 2'}, ...
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

title_str = 'Reactive Power Generated';
y_label = 'MVAR';

grid on
set(gca,'FontSize',.85*bfz)
legend({'LTD Gen 1','LTD Gen 2'}, ...
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