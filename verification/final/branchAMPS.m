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

%% amps
psdsData_col = jfind(psds_data, 'amps');
t = psds_data.Data(:,1);
figure()
hold on
legNames={};
for index = psdsData_col
    plot(t, psds_data.Data(:,index), 'linewidth',3)
    legNames{end+1} =  psds_data.Description{index};
end
for br = uniBranch
    brID = ['br',int2str(br)];
    plot(mir.t, mir.branch.(brID).Amps*.575,'--o') % some kind of scaling makes this wrong...
    legNames{end+1} =  brID;
end
legend(legNames)
title('Branch Current [AMPS]')

%% power in MW
psdsData_col = jfind(psds_data, 'pbr');
t = psds_data.Data(:,1);
figure()
hold on
legNames={};
for index = psdsData_col
    plot(t, psds_data.Data(:,index),'linewidth',3)
    legNames{end+1} =  psds_data.Description{index};
end
title('Real Power Flow [MW]')

% Plot PSLTD mw flows...
hold on
for br = uniBranch
    brID = ['br',int2str(br)];
    plot(mir.t, mir.branch.(brID).Pbr,'--o')
    legNames{end+1} =  brID;
end
legend(legNames)

%% power in MVAR
psdsData_col = jfind(psds_data, 'qbr');
t = psds_data.Data(:,1);
figure()
hold on
legNames={};
for index = psdsData_col
    plot(t, psds_data.Data(:,index),'linewidth',3)
    legNames{end+1} =  psds_data.Description{index};
end
title('Reactive Power Flow [MVAR]')

% Plot PSLTD flows
hold on
for br = uniBranch
    brID = ['br',int2str(br)];
    plot(mir.t, mir.branch.(brID).Qbr,'--o')
    legNames{end+1} =  brID;
end
legend(legNames)

% %