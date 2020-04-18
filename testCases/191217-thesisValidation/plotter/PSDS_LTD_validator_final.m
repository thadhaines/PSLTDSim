%%  PSDS_LTD_validator_final.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   12/17/19    08:00   init

%% init
clear; format compact; clc; close all;
format long;

%% Plot params
printFigs =  false; % true; %  
miniFlag = 1; % decrease plot width by half
ds = 5; % number of samples to skip in PSDS data plots
%% Knowns - Case file names

% Six Machine -> works with git .p etc.

PSDSfileName = 'sixMachineStep1.chf'; % 75 MW
LTDCaseName = 'SixMachineStep1';
genChange = 0;
% 
% PSDSfileName = 'sixMachineRamp1.chf'; % 75 MW
% LTDCaseName = 'SixMachineRamp1';
% genChange = 0;
% 
% PSDSfileName = 'sixMachineGenTrip0.chf';
% LTDCaseName = 'SixMachineTrip0';
% genChange = -0;

%%
%Mini WECC - No PSS
% PSDSfileName = 'miniWECC_loadStep.chf'; % case used in IEEE paper
% LTDCaseName = 'miniWECCstep'; %
% genChange = 0;
% % 
% PSDSfileName = 'miniWECC_loadRamp.chf'; % case used in IEEE paper
% LTDCaseName = 'miniWECCramp'; %
% genChange = -0; %
% 
% PSDSfileName = 'miniWECC_genTrip027.chf'; %
% LTDCaseName = 'miniWECCgenTrip027';
% genChange = -0;

% %%
% % Mini WECC - PSS
% PSDSfileName = 'miniWECC_loadStepPSS.chf'; % case used in IEEE paper
% LTDCaseName = 'miniWECCstepPSS'; %
% genChange = 0;
% 
% PSDSfileName = 'miniWECC_loadRampPSS.chf'; % case used in IEEE paper
% LTDCaseName = 'miniWECCrampPSS'; %
% genChange = -0; %
% 
% PSDSfileName = 'miniWECC_genTrip027PSS.chf'; %
% LTDCaseName = 'miniWECCgenTrip027PSS';
% genChange = -0;

% % WECC - use seperate matlab file - datagrabber
%PSDSfileName = '18HSPstep.chf'; % case used in IEEE paper
%LTDCaseName = '18HSPweccStep'; %
%genChange = 0;



%% import PSDS data
psds_data = udread(PSDSfileName,[]); % 
%cellfun(@disp,psds_data.Name) % display all data types collected from psds
%psdsData_col = jfind(psds_data, 'spd');
%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})
%% Initial not super useful plots (kind of ... useful in six machine case)
compareVsel(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds,[32,17])
compareQsel(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds,[32,30,68])
comparePmsel(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds,[32,30])
comparePesel(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds,[32,30])
compareAnglesel(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds,[30])

%compareV(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareQ(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareAngle(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePm(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePe(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)

%compareFreqTrip(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)
%compareWfreq(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, fAdj, genChange) % doesn't handle changes in inertia, fAdj used for this

%% Frequency plots
%compareF3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)

%% Difference plots
% compareV2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePe2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePm2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQ2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAngle2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)

%% percent difference plots
% compareV3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePe3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePm3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQ3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQ3ALT(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAngle3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAngle3ALT(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)

%% Branch comparisons
% require matlab ... newer than 2014
% comparePbr1(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePbr2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePbr3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePbr3ALT(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% branch difs
% compareQbr1(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQbr2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQbr3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareQbr3ALT(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% branch % difs
% compareAmp1(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAmp2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAmp3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareAmp3ALT(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)

%% IEEE simplified plots
%compareF3IEEE(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)
%comparePm2IEEE(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePm3IEEE(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)