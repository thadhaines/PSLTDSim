function [  ] = compareAngle3( mir, psds_data, varargin )
%compareAnlge Compare LTD mirror and psds_data angle data
%   optional inputs: case name, print figs, figure size
%   PSDS angles need to have the reference subtracted from them to be centered
%   around 0

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
makeLegend = 1;
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

%% find slack name Area
%cycle through areas until one has a slackbus
for areaN =1:max(size(mir.areaN))
    curArea = ['A',int2str(mir.areaN(areaN))];
    if max(size(mir.(curArea).slackBusN)) > 0
        slackNum = ['S',int2str(mir.(curArea).slackBusN)];
        busNam = mir.(curArea).(slackNum).BusName;
        busNum = mir.(curArea).slackBusN;
        tarId = 1;
        break
    end % if area has slackBusN
end % for each area in mirror

%% find where ameta and slack name intersect
slackNdx = findPSDSndx(psds_data, busNum, busNam, tarId, 'ameta' );
                    
slackAng = psds_data.Data(:,slackNdx);
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
        
        %%
        % Comparison addition
        LTDdata = rad2deg(mir.(curArea).(curSlack).Va);
        
        psdsDataNdx = findPSDSndx(psds_data, mir.(curArea).(curSlack).BusNum, mir.(curArea).(curSlack).BusName, 1, 'ameta' );
        
        if max(size(psdsDataNdx))==1
            pData = rad2deg(unwrap(deg2rad(( psds_data.Data(:,psdsDataNdx)- slackAng ))));
            cData = calcPdiff( t, mir, pData, LTDdata );
            plot(tds, dsmple(cData,ds))
            
            name = [(curArea),'.',(curSlack)];
            legNames{end+1} = ['LTD ',name];
            if debug disp(name); end
        end
        %%
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        
        %%
        % Comparison addition
        LTDdata = rad2deg(mir.(curArea).(curGen).Va);
        psdsDataNdx = findPSDSndx(psds_data, mir.(curArea).(curGen).BusNum, mir.(curArea).(curGen).BusName, 1, 'ameta' );
        
        % check if only one index exist, if so, plot
        if max(size(psdsDataNdx))==1
            pData = rad2deg(unwrap(deg2rad(( psds_data.Data(:,psdsDataNdx)- slackAng ))));
            cData = calcPdiff( t, mir, pData, LTDdata );
            plot(tds, dsmple(cData,ds))
            
            name = [(curArea),'.',(curGen)];
            legNames{end+1} = ['LTD ',name];
            if debug disp(name); end
        end
        %%
        
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
if noCase ==1
    title('Percent Difference of LTD and PSDS Generator Voltage Angles')
else
    title({'Percent Difference of LTD and PSDS Generator Voltage Angles'; ['Case: ', LTDCaseName]})
end
xlabel('Time [sec]')
ylabel('Percent Difference [%]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Angle3'],'-pdf'); % to print fig
end

end

