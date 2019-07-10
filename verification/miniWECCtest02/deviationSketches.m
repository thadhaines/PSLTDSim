%% Attempt to make comparison graphs of LTD deviation from PSDS
%% init
clear; format compact; clc; close all;
format long;
%% Data to Load
PSDSfileName = 'miniWECC_genTrip0.chf'; % turning GEN ON, couldn't figute out PSDS simulation - doesn't work right
LTDCaseName = 'miniWECCgenTrip027';  
%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})
%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds


%% proof of concept 
legNames = {};
hold on
t = psds_data.Data(:,1);
v_cols = jfind(psds_data, 'vmeta');
for area = 1:max(size(mir.areaN)) % for each area

    curArea = ['A',int2str(area)];
    uniqueEntry = unique(mir.(curArea).slackBusN);
    for slack = 1:max(size(mir.(curArea).slackBusN))
        if ismember(mir.(curArea).slackBusN(slack),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).slackBusN(slack)) = [];
            curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
            plot(mir.t, mir.(curArea).(curSlack).Vm,'-o')
            name = [(curArea),'.',(curSlack)];
            legNames{end+1} = ['LTD ',name];
            
            LTDdata = mir.(curArea).(curSlack).Vm;
            % Find psds data for current LTD data
            psdsVdataNdx = intersect(jfind(psds_data, mir.(curArea).(curSlack).BusName),jfind(psds_data, 'vmeta'));
            % Find psds data...
            pVdata = psds_data.Data(:,psdsVdataNdx);
            plot(t,pVdata)
            grid()
            
            %{ 
            create data for deviation comparison
            % inputs: psdsT, psdsData, LTDdata
            LTDtNdx = 1;
            cData = zeros(size(pVdata));
            for pNdx=1:size(pVdata,1)
                if t(pNdx)> mir.t(LTDtNdx)
                    % Adjust LTD index as required
                    LTDtNdx = LTDtNdx+1;
                    if LTDtNdx > max(size(LTDdata))
                        LTDtNdx = max(size(LTDdata));
                    end
                end
                cData(pNdx) = pVdata(pNdx)-LTDdata(LTDtNdx);
            end
            %}
            cData = calcDeviation( t, mir, pVdata, LTDdata );
            figure
            plot(t,cData)
            grid()
        end
    end
end

legend(legNames)

%% Attempt at full Voltage Deviation plot
printFigs = 1;
miniFlag =  1;
ds = 30;
compareV2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePe2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%comparePm2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%compareQ2(mir, psds_data, LTDCaseName, printFigs, miniFlag, ds)
%% Closer look at individual item...

% ltdData = mir.A1.G118.G1.Pe;
% peCol = jfind(psds_data,'pg');
% genCols = jfind(psds_data, mir.A1.G118.BusName);
% dataNDX = intersect(peCol, genCols)

% ltdData = mir.A1.G48.G1.Pm;
% pmCol = jfind(psds_data,'pm');
% genCols = jfind(psds_data, mir.A1.G48.BusName);
% dataNDX = intersect(pmCol, genCols)

% ltdData = mir.A1.G34.Vm;
% vmCol = jfind(psds_data,'vmeta');
% genCols = jfind(psds_data, mir.A1.G34.BusName);
% dataNDX = intersect(vmCol, genCols)

ltdData = mir.A1.G34.G1.Q;
vmCol = jfind(psds_data,'qg');
genCols = jfind(psds_data, mir.A1.G34.BusName);
dataNDX = intersect(vmCol, genCols)

x_lim= [0, 100];
pData = psds_data.Data(:,dataNDX);
t = psds_data.Data(:,1);
figure
subplot(2,1,1)
stairs(mir.t, ltdData ,'-o')
hold on
plot(t, pData)
grid on
xlim(x_lim)
legend({'LTD','PSDS'})
ylabel('MW')
xlabel('Time [sec]')

cData = calcDeviation( t, mir, pData, ltdData );
subplot(2,1,2) 
plot(t,cData)
grid on
xlim(x_lim)
ylabel('MW')
xlabel('Time [sec]')
legend({'Deviation'})