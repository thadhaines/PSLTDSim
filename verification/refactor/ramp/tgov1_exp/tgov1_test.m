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
plot(tout,Pmout,'linewidth',1)
title('MATLAB v Python Tgov1')
hold on
plot(t_py, y_py,'--','linewidth',1)
legend('simulink','python')
grid on

subplot(3,1,2)
abs_dif = abs(y_py'-Pmout);
plot(tout, abs_dif)
grid on
title('Absolute Difference')

subplot(3,1,3)
rel_dif = abs(y_py'-Pmout)./abs(Pmout)*100;
plot(tout, rel_dif)
grid on
ylabel('Percent')
title('Relative Difference')