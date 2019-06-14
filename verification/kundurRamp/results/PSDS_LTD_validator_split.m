%%  PSDS_LTD_validator_split.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations of various time steps to
%                       results generated from PSDS. PDSS results are in a
%                       .chf file and have one fmeta and vmeta that
%                       captures data from all areas.

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig

%   History:
%   06/04/19    14:15   init - plots formatted
%   06/05/19    12:40   Added handling of plotting only unique bus voltages
%   06/05/19    12:46   Added LTD and PSDS to voltage, p, and q plots
%   06/05/19    12:56   Added comparison of Pm plot
%   06/10/19    09:41   Added PSDS angles relative to angle col 1 (may or
%                       may not always be the slack bus....
%   06/10/19    14:17   Added an auto-scale to bus angle
%   06/14/19    11:08   Split out plot functions

%% init
clear; format compact; clc; close all;
format long;

% to Export pdfs.
printFigs = 0;

%% Knowns
% PSDSfileName = 'kundur.step0.chf';
% LTDCaseName = 'kundurStep2';

% PSDSfileName = 'kundur.ramp0.chf'; % 40 second ramp down
% LTDCaseName = 'kundurRamp2';

% PSDSfileName = 'kundur.rampReff.chf'; % 1 machine no gov, the rest the same
% LTDCaseName = 'kundurReff0';

% PSDSfileName = 'kundur.rampReff2.chf'; % all gens same H, diff govs
% LTDCaseName = 'kundurReff2';

% PSDSfileName = 'kundur.rampReff3.chf'; % diff H, diff govs.. Handles change in MWcap
% LTDCaseName = 'kundurReff3';

PSDSfileName = 'kundur.rampReff4.chf'; % govs all dif mbase, mwcap, H... seems ok. frequency still not right.
LTDCaseName = 'kundurReff4';

% % % 
% PSDSfileName = 'kundur.ramp1.chf' % 40 second ramp
% LTDCaseName = 'kundurRamp1'

% PSDSfileName = 'kundur.gentrip0.chf'
% LTDCaseName = 'kundurGenTrip0'

plotTheoSS = 0; % use for steps only - requires manual calcs of beta, MW delta

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F'],
    };

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