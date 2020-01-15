%%  PSDS_LTD_validator_miniWECC.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   06/15/19    10:15   init - plots formatted
%   06/16/19    09:52   added handling for multigen buses
%   06/29/19    22:22   Changed to miniWECC validator

%% init
clear; format compact; clc; close all;
format long;

% to Export pdfs.
printFigs = false;
miniFlag = 1; % decrease plot width by half

%% Knowns
%PSDSfileName = 'miniWECC_loadStep.chf'; % NO PSS, system goes unstable Voltages off - exciters only
% PSDSfileName = 'miniWECC_loadStepPSS.chf'; % With PSS, frq and powers ok, voltages off (exciters + PSS)...
% LTDCaseName = 'miniWECCstep1'; % match PSLF 
% genChange = -1200;
% 
PSDSfileName = 'miniWECC_genTrip0.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
LTDCaseName = 'miniWECCgenTrip027';  
genChange = -212.5; % required for ss freq to be calculated _> Use trip plot function - Doesn't match theoretical...

% PSDSfileName = 'miniWECC_genTrip032.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
% LTDCaseName = 'miniWECCgenTrip032';  
% genChange = -1429.5; % required for ss freq to be calculated _> Use trip plot function - Doesn't match theoretical...


ds = 30; % number of samples to skip in PSDS data plots

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})

fAdj = (300*6.5)/mir.Hsys;
systemLossAdj = mir.Pe(1)-mir.Pe(end);
genChange = genChange + systemLossAdj;

%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds

%% external Plot Functions
%compareV(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareQ(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareAngle(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePm(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePe(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareFreqTrip(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)

%compareWfreq(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, fAdj) % doesn't handle changes in inertia
%% Frequency plots
compareF3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)
%% Deviation plots
compareV2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePe2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePm2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQ2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAngle2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)

%% percent difference plots
% compareV3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePe3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePm3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQ3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAngle3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)