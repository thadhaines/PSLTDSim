function [  ] = compareAngle2( mir, psds_data, varargin )
%compareAnlge Compare LTD mirror and psds_data angle data
%   optional inputs: case name, print figs, figure size
%   PSDS angles need to have the reference subtracted from them to be centered
%   around 0
%   Deviation changed to Difference in plot output

% Handle optional inputs
if nargin == 2
    printFigs = 0;
    noCase =1;
elseif nargin >= 4
    LTDCaseName = varargin{1};
    printFigs = varargin{2};
    noCase = 0;
end

if nargin < 5
    ppos = [18 312 1252 373];
else
    if varargin{3} == 1
        ppos = [18 312 626 373];
    else
        ppos = [18 312 1252 373];
    end
end

% varables for plots to work
debug = 0;
makeLegend = 0;
x_lim = [mir.t(1), mir.t(end)];
bfz = 13;
t = psds_data.Data(:,1); % PSDS time

% funtion specific
ag_col = jfind(psds_data, 'abug');
ds = varargin{4};
tds = dsmple(t,ds);

if max(size(ag_col)) > 20
    makeLegend = 0;
end

% for future RMS calcs
linesPltd = 0;
rSum = tds.*0;
grey = [.75,.75,.75];
lineSumd = 0;
absSum = 0;
%% find slack name Area
%cycle through areas until one has a slackbus
for areaN =1:max(size(mir.areaN))
    curArea = ['A',int2str(mir.areaN(areaN))];
    if max(size(mir.(curArea).slackBusN)) > 0
        slackNum = ['S',int2str(mir.(curArea).slackBusN)];
        slackName = mir.(curArea).(slackNum).BusName;
        bNum = mir.(curArea).(slackNum).BusNum;
        bName = mir.(curArea).(slackNum).BusName;
        tarID = 1;
        psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'abug' );
        break
    end % if area has slackBusN
end % for each area in mirror

%% find where ameta and slack name intersect
slackAng = psds_data.Data(:,psdsDataNdx);

%% plot
figure('position',ppos)
%set(gca,'ColorOrder',flipud(imcomplement(colormap(spring(floor(max(size(ag_col)/2)))))))
legNames ={};
hold on

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) );
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        angData = rad2deg(mir.(curArea).(curSlack).Va);
        name = [(curArea),'.',(curSlack)];
        %%
        % Comparison addition
        LTDdata = rad2deg(mir.(curArea).(curSlack).Va);
        
        % new find index and RMS
        bNum = mir.(curArea).(curSlack).BusNum;
        bName = mir.(curArea).(curSlack).BusName;
        tarID = 1;
        psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'abug' );
        
        if max(size(psdsDataNdx))==1
            pData = rad2deg(unwrap(deg2rad(( psds_data.Data(:,psdsDataNdx)- slackAng ))));
            cData = dsmple(calcDeviation( t, mir, pData, LTDdata),ds);
            plot(tds, cData,'color',grey,'linewidth',.5)
            legNames{end+1} = name;
            linesPltd = linesPltd+1;
            if sum(isnan(cData(:))) == 0
                rSum = rSum+cData.^2;
                absSum = abs(cData)+ absSum;
                lineSumd = lineSumd +1;
            end
        else
            disp(name)
        end
        %%
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        name = [(curArea),'.',(curGen)];
        %%
        % Comparison addition
        LTDdata = rad2deg(mir.(curArea).(curGen).Va);
        
        % new find index and RMS
        bNum = mir.(curArea).(curGen).BusNum;
        bName = mir.(curArea).(curGen).BusName;
        tarID = 1;
        psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'abug' );
        
        if max(size(psdsDataNdx))==1
            pData = rad2deg(unwrap(deg2rad(( psds_data.Data(:,psdsDataNdx)- slackAng ))));
            cData = dsmple(calcDeviation( t, mir, pData, LTDdata),ds);
            plot(tds, cData,'color',grey,'linewidth',.5)
            legNames{end+1} = name;
            linesPltd = linesPltd+1;
            if sum(isnan(cData(:))) == 0
                rSum = rSum+cData.^2;
                absSum = abs(cData)+ absSum;
                lineSumd = lineSumd +1;
            end
        else
            disp(name)
        end
        %%
        
    end
end

% calculate and plot RMS
RMS = sqrt(rSum./lineSumd);
absDevMean = absSum ./ lineSumd;
datas = plot(tds, absDevMean,'color',grey,'linewidth',1.5);
rPlot = plot(tds, absDevMean,'k','linewidth',1.5);

if makeLegend
    legend(legNames)
else % make only general legend
    dataName = [int2str(linesPltd),' Comparisons'];
    legend([datas,rPlot],dataName,'Average Absolute Difference','location','best')
end
grid on
if noCase ==1
    title('Difference of LTD Generator Voltage Angle from PSDS')
else
    title({'Difference of LTD Generator Voltage Angle from PSDS'; ['Case: ', LTDCaseName]})
end
xlabel('Time [sec]')
ylabel('Angle Difference [degrees]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Angle2'],'-pdf'); % to print fig
end

end

