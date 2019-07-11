%%  PSDS_LTD_validator_final.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   07/11/19    10:47   init - regen data with current code and files
%% init
clear; format compact; clc; close all;
format long;

% Plot params
printFigs = false;
miniFlag = 1; % decrease plot width by half
ds = 30; % number of samples to skip in PSDS data plots
%% Knowns - Case file names

% Six Machine
% PSDSfileName = 'sixMachineGenTrip0.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
% LTDCaseName = 'SixMachineTrip0';  
% genChange = -90; % required for ss freq to be calculated _> Use trip plot function
% fAdj = 0;

% PSDSfileName = 'sixMachineRamp1.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
% LTDCaseName = 'SixMachineRamp1';  
% genChange = 0;
% fAdj = 0;
%
% PSDSfileName = 'sixMachineStep1.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
% LTDCaseName = 'SixMachineStep1';  
% genChange = 0;
% fAdj = 0;

% Mini WECC
PSDSfileName = 'miniWECC_loadStep.chf'; % NO PSS, system goes unstable Voltages off - exciters only
LTDCaseName = 'miniWECC3ALTDstep'; % match PSLF 
genChange = -0; % if system losses accounted for
%genChange = -1200;
fAdj = 0;

PSDSfileName = 'miniWECC_loadRamp.chf'; % NO PSS, system goes unstable Voltages off - exciters only
LTDCaseName = 'miniWECC3ALTDramp'; % match PSLF 
genChange = -0; % if system losses accounted for
fAdj = 0;
%
PSDSfileName = 'miniWECC_genTrip027.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
LTDCaseName = 'miniWECCgenTrip027';  
genChange = -201.9; % required for ss freq to be calculated _> Use trip plot function - Doesn't match theoretical...
%fAdj = (300*6.5)/mir.Hsys;

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
% compareV(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQ(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAngle(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePm(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePe(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
compareFreqTrip(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)
% 
compareWfreq(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, fAdj) % doesn't handle changes in inertia, fAdj used for this

%% Deviation plots
compareV2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePe2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePm2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
compareQ2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
compareAngle2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)

%% percent difference plots
compareV3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePe3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePm3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
compareQ3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
compareAngle3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)