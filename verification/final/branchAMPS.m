% Attempt to validate current calculations in PSLTDSim with PSDS data...
close all
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

x_lim = [mir.t(1), mir.t(end)];
bfz = 13;
t = psds_data.Data(:,1); % PSDS time

%% amps
psdsData_col = jfind(psds_data, 'amps');
figure()
hold on
legNames={};
for index = psdsData_col
    plot(t, psds_data.Data(:,index), 'linewidth',3)
    fullDesc = psds_data.Description{index};
    splitStr = split(fullDesc,':')
    legNames{end+1} =  ['PSDS ',splitStr{1} ,' to ',splitStr{4} ];
end
for br = uniBranch
    brID = ['br',int2str(br)];
    plot(mir.t, mir.branch.(brID).Amps,'--o') 
    legNames{end+1} =  ['LTD ', int2str(br), ' to ', int2str( mir.branch.(brID).Tbus)];
end

title('Branch Current [AMPS]')

legend(legNames,'location','east')
grid on
xlabel('Time [sec]')
ylabel('Current [A]')
set(gca,'fontsize',bfz)
xlim(x_lim)

%% power in MW
psdsData_col = jfind(psds_data, 'pbr');
figure()
hold on
legNames={};
for index = psdsData_col
    plot(t, psds_data.Data(:,index),'linewidth',3)
    fullDesc = psds_data.Description{index};
    splitStr = split(fullDesc,':')
    legNames{end+1} =  ['PSDS ',splitStr{1} ,' to ',splitStr{4} ];
end

% Plot PSLTD mw flows...
hold on
for br = uniBranch
    brID = ['br',int2str(br)];
    plot(mir.t, mir.branch.(brID).Pbr,'--o')    
    legNames{end+1} =  ['LTD ', int2str(br), ' to ', int2str( mir.branch.(brID).Tbus)];
end

title('Real Power Flow [MW]')

legend(legNames,'location','east')
grid on
xlabel('Time [sec]')
ylabel('Power [MW]')
set(gca,'fontsize',bfz)
xlim(x_lim)

%% power in MVAR
psdsData_col = jfind(psds_data, 'qbr');
figure()
hold on
legNames={};
for index = psdsData_col
    plot(t, psds_data.Data(:,index),'linewidth',3)
    fullDesc = psds_data.Description{index};
    splitStr = split(fullDesc,':')
    legNames{end+1} =  ['PSDS ',splitStr{1} ,' to ',splitStr{4} ];
end

% Plot PSLTD flows
hold on
for br = uniBranch
    brID = ['br',int2str(br)];
    plot(mir.t, mir.branch.(brID).Qbr,'--o')
    legNames{end+1} =  ['LTD ', int2str(br), ' to ', int2str( mir.branch.(brID).Tbus)];
end

title('Reactive Power Flow [MVAR]')

legend(legNames,'location','east')
grid on
xlabel('Time [sec]')
ylabel('Power [MVA]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% %