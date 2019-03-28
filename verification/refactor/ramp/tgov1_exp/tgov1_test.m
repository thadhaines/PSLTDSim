%%  tgov1_test.m
%   Thad Haines         research
%   Program Purpose:    figure out whats up with the tgov1
%
%   History:
%   03/27/19    08:13   init

%% init
clear; format compact; clc; close all;
%% Knowns

R = 0.05
Vmax = 1.0
Vmin = 0.0
T1 = 0.5
T2 = 3.0
T3 = 10.0
Dt = 0.0

Pref = .50
delta_w = 0.0

%% simulink comparisons
sim('tgov1')
load('tgovTest.mat')

figure
subplot(3,1,1)
plot(tout,Pmout,'-','linewidth',1.25)
title('MATLAB vs Python Tgov1 Simulation with Zero Initial Conditions')
hold on
plot(t_py, y_py,'--','linewidth',2)

line([tout(1), tout(end)],[Pref,Pref],'color','k')
legend('Simulink','SciPy', 'Pref Input')
set(gca, 'fontsize', 12)
grid on

subplot(3,1,2)
abs_dif = abs(y_py'-Pmout);
plot(tout, abs_dif,'.-')
grid on
title('Absolute Difference')
set(gca, 'fontsize', 12)

subplot(3,1,3)
rel_dif = abs(y_py'-Pmout)./abs(Pmout)*100;
plot(tout, rel_dif,'.-')
grid on
ylabel('Percent')
title('Relative Difference')
set(gca, 'fontsize', 12)

set(gcf, 'position', [680 454 1093 524])

%set(gcf,'color','w'); % to remove border of figure
%export_fig('XXXXXX','-pdf');