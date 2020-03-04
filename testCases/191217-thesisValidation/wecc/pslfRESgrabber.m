% Collect index of useful data, store in array for complete pull...

%% init
clear; format compact; clc; close all;
format long;

%% Test of inex finding....

%PSDSfileName = 'miniWECC_loadRampPSS.chf'; % debug
PSDSfileName = '18HSPstep.chf';
chunkSize = 15000;

dataExists = 1;
Sndx = 1;
fbugCol = []; % starting index (time)
disp('*** Start')
iteration = 0
while dataExists
    datetime('now')
    psds_data = udread(PSDSfileName,[Sndx:Sndx+chunkSize]); % always returns a time vector
    
    if size(psds_data.Name,2) > chunkSize
        % data exists
        dataCol = jfind(psds_data, 'fbug');
        if size(dataCol)>0
            
            fbugCol = [fbugCol, dataCol+chunkSize*iteration];
        end
        Sndx = Sndx+chunkSize
    else
        % end of file
        dataExists = 0;
    end
    iteration = iteration+1
end
disp('*** End')
datetime('now')
psds_data = udread(PSDSfileName,[fbugCol]-1);

% it is wise to save teh fbugCol!


% result: 23 iterations till completion using 5000 chunksize -> ~115000 records in full wecc
% with only fmeta
% Tip: read chf in PSLF plot to find when desired data starts and adjsut
% sNdx accordingly.



%%

t = psds_data.Data(:,1); % PSDS time
%cellfun(@disp,psds_data.Name)
dataCol = jfind(psds_data, 'fbug');
grey = [0.7, 0.7, 0.7];
black = [1,1,1];
ds=30;
ppos = [18 312 1252 373];

figure('position',ppos)
hold on
for data=1:max(size(dataCol))-1
    plot( dsmple(t,ds), dsmple(psds_data.Data(:,dataCol(data)),ds), 'color',grey,'linewidth',.5,'HandleVisibility','off') % all others
    
end

plot( dsmple(t,ds), dsmple(psds_data.Data(:,dataCol(max(size(dataCol)))),ds) , 'color',grey,'linewidth',.5)

% compute average
ave = zeros(size(t));
for data=1:max(size(dataCol))
    ave = (ave + psds_data.Data(:,dataCol(data)));
end
ave = ave./max(size(dataCol));
plot( t, ave, 'k','linewidth',1)

% import mirror data...
plot(mir.t,mir.f.*60,'color',[1,0,1],'linewidth',1)

% pretty plots
bfz = 13;
LTDCaseName = mir.meta.fileName(1:size(mir.meta.fileName,2)-1);
grid on
legend({[int2str(max(size(dataCol))) ' PSDS'],'Average PSDS','LTD'})
title('Generator Frequency Comparison')
title({'Generator Frequency Comparison'; ['Case: ', LTDCaseName]})
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
xlim([0,max(mir.t)])
set(gca,'fontsize',bfz)

set(gcf,'color','w'); % to remove border of figure
%export_fig([LTDCaseName,'Freq'],'-pdf'); % to print fig
%export_fig([LTDCaseName,'Freq'],'-png'); % to print fig

%% deviation data

dif = abs(calcDeviation( t, mir, ave, mir.f*60 ));

figure('position',ppos)
plot(t,dif,'m','linewidth',.5)
title({'Absolute Frequency Difference'; ['Case: ', LTDCaseName]})
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)
xlim([0, max(mir.t)])
grid on
set(gcf,'color','w'); % to remove border of figure
%export_fig([LTDCaseName,'absFreqDiff'],'-pdf'); % to print fig