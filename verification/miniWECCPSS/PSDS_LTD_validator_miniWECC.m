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
%   09/10/19    09:47   Used for PSS results.

%% init
clear; format compact; clc; close all;
format long;

% to Export pdfs.
printFigs =  false;% true; %
miniFlag = 1; % decrease plot width by half

%% Knowns
% PSDSfileName = 'miniWECC_loadStep.chf'; % NO PSS, system goes unstable Voltages off - exciters only
% PSDSfileName = 'miniWECC_loadStepPSS.chf'; % With PSS, frq and powers ok, voltages off (exciters + PSS)...
% LTDCaseName = 'miniWECCLTDPSSstep'; % match PSLF 
% genChange = 0;%
% % 
% PSDSfileName = 'miniWECC_genTrip027PSS.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
% LTDCaseName = 'miniWECCgenTrip027PSS';  
% genChange = -212.5; % required for ss freq to be calculated _> Use trip plot function - Doesn't match theoretical...

PSDSfileName = 'miniWECC_loadRampPSS.chf'; 
LTDCaseName = 'miniWECCLTDPSSramp';  
genChange = 0; 


ds = 30; % number of samples to skip in PSDS data plots

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})

fAdj = (300*6.5)/mir.Hsys;% for gen trip 0%
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

%%
%compareFreqTrip(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)

%compareWfreq(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, fAdj) % doesn't handle changes in inertia

% improved frequency plotting...
compareF3( mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, 0) % use zero for steps
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