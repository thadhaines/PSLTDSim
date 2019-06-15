%%  PSDS_LTD_validator_sixMachine.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   06/15/19    10:15   init - plots formatted

%% init
clear; format compact; clc; close all;
format long;

% to Export pdfs.
printFigs = 0;

%% Knowns
% PSDSfileName = 'sixMachineStep1.chf'; % fast govs, default exciters
% LTDCaseName = 'SixMachineStep1';

% PSDSfileName = 'sixMachineStep2.chf'; % mixed govs, fast exciters
% LTDCaseName = 'SixMachineStep2';

PSDSfileName = 'sixMachineRamp1.chf'; % mixed govs, fast exciters
LTDCaseName = 'SixMachineRamp1';

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})

%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds

%% external Plot Functions
compareV(mir, psds_data, LTDCaseName, printFigs)
compareQ(mir, psds_data, LTDCaseName, printFigs)
compareAngle(mir, psds_data, LTDCaseName, printFigs)
comparePm(mir, psds_data, LTDCaseName, printFigs)
comparePe(mir, psds_data, LTDCaseName, printFigs)
compareWfreq(mir, psds_data, LTDCaseName, printFigs)