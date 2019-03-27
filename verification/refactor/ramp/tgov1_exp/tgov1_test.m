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

%% simulink
sim('tgov1')

plot(tout,Pmout)
