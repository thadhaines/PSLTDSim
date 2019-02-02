%  ee554_noGov.m
%   Thad Haines         Research
%   Program Purpose:    Import data from PSLF and LTD .mat
%                       Make plots 
%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   01/19/19    08:32   init
%   01/19/19    12:48   verification of Euler with Frequency effects
%   01/24/19    19:19   split do a load step up


%% init
clear; format compact; clc; %close all; 

print_f = 0;
p_pos = [400 200 1421 734];
bfz = 15;
l_loc = 'best';

%% import pslf data
pslf_data = udread('ee554.exc.1.chf',[]);
cellfun(@disp,pslf_data.Name)

spd_col = jfind(pslf_data, 'spd')
v_col = jfind(pslf_data, 'v')
pg_col = jfind(pslf_data, 'pg')
qg_col = jfind(pslf_data, 'qg')
f_col = jfind(pslf_data, 'fbu')

t = pslf_data.Data(:,1);

%% import LTD data
load('noGov.mat') % euler f integration
load('noGovAB.mat') % adams bashforth integration
load('noGovABHres.mat') % adams bashforth integration, 0.25 timestep
load('noGovABHw.mat') % accounts for freq in swing equation
load('noGovEw.mat') % accounts for freq in swing equation
t_1 = noGov.t;
f_1 = noGov.f;

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
% PSLF data
plot(t,pslf_data.Data(:,pg_col(1)),'.--','linewidth',3,'color',pltC.grey)
plot(t,pslf_data.Data(:,pg_col(2)),'linewidth',1,'color',[0,0,0])
% LTD data
stairs(t_1,noGov.A1.S011.S0.Pe,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,noGov.A1.G021.G0.Pe,':s','linewidth',1,'color',pltC.dgreen)


y_label = 'MW';
grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','LTD Gen 1','LTD Gen 2'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot generator frequency
subplot 222
title_str = 'Generator Frequency';
hold on
plot(t,pslf_data.Data(:,f_col(1))/60,'.--','linewidth',3,'color',pltC.grey)
plot(t,pslf_data.Data(:,f_col(2))/60,'linewidth',1,'color',[0,0,0])

plot(t_1,f_1,':o','linewidth',1.5,'color',pltC.magenta) %  Euler
plot(noGovAB.t,noGovAB.f,':s','linewidth',1.5,'color',pltC.green)
plot(noGovEw.t,noGovEw.f,':+','linewidth',1.5,'color',[0,0,0])
plot(noGovABHw.t,noGovABHw.f,':+','linewidth',1.5,'color',pltC.Lblue)


y_label = 'Frequency [pu]';
grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2', 'LTD Euler','LTD AB','LTD Euler w Freq','LTD AB w Freq'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend

title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot pslf Voltage
title_str = 'Generator Voltage';

subplot 223
hold on
%pslf data
plot(t,pslf_data.Data(:,v_col(1)),'.--','linewidth',3,'color',pltC.grey)
plot(t,pslf_data.Data(:,v_col(2)),'linewidth',1,'color',[0,0,0])
%LTD data
stairs(t_1,noGov.A1.S011.Vm,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,noGov.A1.G021.Vm,':s','linewidth',1,'color',pltC.dgreen)

y_label = 'Voltage [pu]';
grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','LTD Gen 1','LTD Gen 2'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot pslf q power generated
subplot 224
hold on
plot(t,pslf_data.Data(:,qg_col(1)),'.--','linewidth',3,'color',pltC.grey)
plot(t,pslf_data.Data(:,qg_col(2)),'linewidth',1,'color',[0,0,0])

stairs(t_1,noGov.A1.S011.S0.Q,':o','linewidth',1.5,'color',pltC.magenta)
stairs(t_1,noGov.A1.G021.G0.Q,':s','linewidth',1,'color',pltC.dgreen)

title_str = 'Reactive Power Generated';
y_label = 'MVAR';

grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','LTD Gen 1','LTD Gen 2'}, ...
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