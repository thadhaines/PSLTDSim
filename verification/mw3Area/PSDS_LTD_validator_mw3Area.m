%%  PSDS_LTD_validator_mw3Area.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   07/10/19    14:44   init - from miniWECC validator
%   06/16/19    09:52   added handling for multigen buses
%   06/29/19    22:22   Changed to miniWECC validator

%% init
clear; format compact; clc; close all;
format long;

% to Export pdfs.
printFigs = false;
miniFlag = 1; % decrease plot width by half

%% Knowns

PSDSfileName = 'miniWECC_genStep47.chf'; 
LTDCaseName = 'miniWECC3A0';  


ds = 30; % number of samples to skip in PSDS data plots

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})

%fAdj = (300*6.5)/mir.Hsys;
%systemLossAdj = mir.Pe(1)-mir.Pe(end);
%genChange = genChange + systemLossAdj;

%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds

%% external Plot Functions
%compareV(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareQ(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareAngle(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% comparePm(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
comparePe(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
% compareFreqTrip(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, genChange)

%compareWfreq(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds, fAdj) % doesn't handle changes in inertia

%% Deviation plots
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
% compareAngle3(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)