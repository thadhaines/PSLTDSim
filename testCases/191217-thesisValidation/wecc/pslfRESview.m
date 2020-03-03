% 'easy' view of PSLF datas...

%% init
clear; format compact; clc; close all;
format long;

%%
PSDSfileName = '18HSPRamp.chf'; % 75 MW

%psds_data = udread(PSDSfileName,[]);
psds_data = udread(PSDSfileName,[1,10000:15000]);

t = psds_data.Data(:,1); % PSDS time
cellfun(@disp,psds_data.Name)
dataCol = jfind(psds_data, 'fbug');

figure
hold on
for data=1:max(size(dataCol))
    plot( t, psds_data.Data(:,dataCol(data)))%'color',grey,'linewidth',.5,'HandleVisibility','off') % all others
    
end