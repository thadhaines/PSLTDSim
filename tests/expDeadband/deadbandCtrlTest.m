%%  deadbandCtrlTest.m
%   Thad Haines         Research
%   Program Purpose:    Experiment with deadband control
%                       Attempt to eliminate step

%   History:
%   10/03/19    15:10   init 
%% init
clear; format compact; clc; close all;
format long;

%% Knowns
Mbase = 100;    %MVA
R = 0.05;       %Amount of speed change for 100% change in power
fBase = 60;

deadband = .036;%Hz

xs = .009;
fRange = [fBase*(1-R):xs:fBase*(1+R)];

%% Initial no deadband function
plot(fRange, (fBase-fRange)/fBase*(Mbase/R))

%% step deadband
fInput = (fBase-fRange)/fBase;
fDB = fInput.* (abs(fInput)> (deadband/fBase));
hold on
plot(fRange, fDB*(Mbase/R), '--')

grid on
xlim([59.9,60.1])
xlabel('Frequency [Hz]')
ylabel('Requested MW Change')

%% adjustable ramp input...

%% Experimental ramp