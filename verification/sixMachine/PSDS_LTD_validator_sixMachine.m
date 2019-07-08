%%  PSDS_LTD_validator_sixMachine.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   06/15/19    10:15   init - plots formatted
%   06/16/19    09:52   added handling for multigen buses

%% init
clear; format compact; clc; close all;
format long;

% to Export pdfs.
printFigs = 1;
miniFlag = 0; % decrease plot width by half

%% Knowns
% % PSDSfileName = 'sixMachineStep1.chf'; % fast govs, default exciters
% % LTDCaseName = 'SixMachineStep1';

% PSDSfileName = 'sixMachineStep2.chf'; % mixed govs, fast exciters
% LTDCaseName = 'SixMachineStep2'; % match PSLF 
%LTDCaseName = 'SixMachineStep3'; % system H reduced by 15% 
%LTDCaseName = 'SixMachineStep4'; % Account for Reff
% 
% PSDSfileName = 'sixMachineRamp1.chf'; % mixed govs, fast exciters
% LTDCaseName = 'SixMachineRamp1';

% PSDSfileName = 'sixMachineGenTrip0.chf'; % Single gen trip off
% LTDCaseName = 'SixMachineTrip0';  
% genChange = -90; % required for ss freq to be calculated _> Use trip plot function


% PSDSfileName = 'sixMachineGenTrip01.chf'; % Single gen trip off/on -> PSDS goes unstable
% LTDCaseName = 'SixMachineTrip01';  
% genChange = -0; % required for ss freq to be calculated _> Use trip plot function

% PSDSfileName = 'sixMachineGenTrip1.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
% LTDCaseName = 'SixMachineTrip1';  
% genChange = 90; % required for ss freq to be calculated _> Use trip plot function
% 
% 
PSDSfileName = 'sixMachineBranchTrip0.chf'; % trip two lines off
LTDCaseName = 'SixMachineBTrip0'; % match PSLF 
genChange = 0;

% PSDSfileName = 'sixMachineBranchTrip1.chf'; % trip two lines off, one on
% LTDCaseName = 'SixMachineTrip2'; % match PSLF 
% genChange = 0;
%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})


fAdj = 0;
%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds
ds = 10;

%% external Plot Functions
%compareV(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareQ(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareAngle(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePm(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePe(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
compareFreqTrip(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)
compareWfreq(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, fAdj) % doesn't handle changes in inertia
%% Multi plot to compare other features
%{
compareWfreq(mir, psds_data)
close % to close relative comparison plot
load('SixMachineStep3F')
mir = SixMachineStep3F;
plot(mir.t,mir.f*60, 'b-.','linewidth',1)
load('SixMachineStep4F')
mir = SixMachineStep4F;
plot(mir.t,mir.f*60, '--','color',[.7 .7 .7],'linewidth',2)
legend({'Weighted PSDS','LTD','Theoretical SS','LTD Scaled Hsys','LTD Reff'},'location','best')
set(gcf, 'position', [18 312 626 373])
%}

%% Multi plot to compare other features RAMP
%{
compareWfreq(mir, psds_data)
close % to close relative comparison plot
load('SixMachineRamp2F')
mir = SixMachineRamp2F;
plot(mir.t,mir.f*60, 'b-.','linewidth',1)
load('SixMachineRamp3F')
mir = SixMachineRamp3F;
plot(mir.t,mir.f*60, '--','color',[.7 .7 .7],'linewidth',2)
legend({'Weighted PSDS','LTD','Theoretical SS','LTD Scaled Hsys','LTD Reff'},'location','best')

set(gcf, 'position', [18 312 626 373])
%}