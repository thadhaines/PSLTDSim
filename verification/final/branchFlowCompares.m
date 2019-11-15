% First attempts at calculating branch difference and % difference plots

%close all
clc
clear

PSDSfileName = 'sixMachineRamp1.chf'; % 75 MW
LTDCaseName = 'SixMachineRamp1';
genChange = 0;

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})
uniBranch = unique(mir.branch.branchN);

%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds

%%

% get data cols from psds
psdsData_col = jfind(psds_data, 'pbr'); % pbr, qbr, amps
t = psds_data.Data(:,1);

% make single figure
figure()
hold on

% required variables for plot procedures
legNames={};
x_lim = [mir.t(1), mir.t(end)];
ds=30;
grey = [.75,.75,.75];
tds = dsmple(t, ds);
linesPltd = 0;
absSum = 0;
bfz = 13;
printFigs = 0;

% for each col
for dataCol = psdsData_col
    %   get bus num from description
    splitSTR = split(psds_data.Description{dataCol},':');
    busSTR = splitSTR{1};
    %   get ltd data with bus num
    ltdDataName = ['br',busSTR];
    LTDdata =  mir.branch.(ltdDataName).Pbr; % Qbr Amps/sqrt(3);
    %   compare data
    pData = psds_data.Data(:,dataCol);
    cData = dsmple(calcDeviation( t, mir, pData, LTDdata ),ds); %calcPdiff or calcDeviation
    %   plot
    plot(tds, cData,'color',grey,'linewidth',.5)
    
    
    %   add legend name
    %...
    
    %   add to running for average
    linesPltd = linesPltd+1;
    absSum = abs(cData)+ absSum;
    
end
% plot average
absDevMean = absSum ./ linesPltd;
plot(tds, absDevMean,'k','linewidth',1.5);
% make labels
title({'Plot Title'; ['Case: ', LTDCaseName]})
xlabel('Time [sec]')
ylabel('Power [MW]')
xlim(x_lim)
set(gca,'fontsize',bfz)
grid on

% pdf output code
    if printFigs
        set(gcf,'color','w'); % to remove border of figure
        export_fig([LTDCaseName,'V2'],'-pdf'); % to print fig
    end