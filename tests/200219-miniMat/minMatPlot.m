%%  miniMatPlot.m
%   Thad Haines         Research
%   Program Purpose:    Validate LTD simulations to PSDS data.
%                       Assumes .chf files have fmeta, vmeta, and ameta data

%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%                       Uses the mini mat that is only the mirror
%                       dictionary

%   History:
%   02/19/20    18:56   init


% Uses outdated matlab functions....

%% init
clear; format compact; clc; close all;
format long;

%% Plot params
printFigs =  false; % true; %  
miniFlag = 1; % decrease plot width by half
ds = 30; % number of samples to skip in PSDS data plots
%% Knowns - Case file names

% debug

PSDSfileName = 'sixMachineRamp1.chf'; % 75 MW
LTDCaseName = 'SixMachineStep1';
genChange = 0;

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})

%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds

%% Plotting of PSDS generators and LTD system...
f_col = jfind(psds_data, 'spd'); % must use speed, else multibus gens are skipped
t = psds_data.Data(:,1); % PSDS time
x_lim = [mir.t(1), mir.t(end)];

grey = [.75,.75,.75];
%% Calculating weighted f from alternative 'mini'mat (mirror and gen H info only
Hsys = mir.Hss;
weightedF = zeros(size(psds_data.Data(:,1),1),1);

for gen = 1:mir.nGens
    curGen = ['G', int2str(gen)];
    weight = mir.gens.(curGen).H; % multiplied pre mat export
    
    genCols = jfind(psds_data, mir.gens.(curGen).psdsID); % busnum:busnam
    genFloc = intersect(genCols,f_col);
    if size(genFloc,2) >1
        dupeFound = 0;
        for dupe = 1:size(genFloc,2) 
            ndx = genFloc(dupe);
            cleanStr = psds_data.Description{ndx};
            cleanStr(cleanStr == ' ') = []; % remove whitespace
            checkStr = strsplit(cleanStr,':');
            if checkStr{6} == mir.gens.(curGen).id
                dupeFound = 1;
                genSpd = psds_data.Data(:,genFloc(dupe)).*(weight/Hsys);
                weightedF = weightedF + genSpd;
            end
        end
        if dupeFound == 0
            disp('mulit intersection! not summed...')
            disp(curGen) % prints name with multi intersections
        end
    else
        genSpd = psds_data.Data(:,genFloc(1)).*(weight/Hsys);
        weightedF = weightedF + genSpd;
    end
end

%% psds speeds*60
figure()
hold on
numF = 0;
for freq=1:max(size(f_col)-1)
    plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(freq))*60,ds),'color',grey,'linewidth',.5,'HandleVisibility','off') % all others
    numF = numF +1;
end
plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(size(f_col,2)))*60, ds),'color',grey,'linewidth',1) % last Freq
numF = numF +1;
numFstr = [int2str(numF),' PSDS'];

% LTD
plot(mir.t, mir.f*60 , 'm','linewidth',1.5)
% weighted
plot(dsmple(t,ds), dsmple(weightedF*60,ds) , 'k','linewidth',1.5)