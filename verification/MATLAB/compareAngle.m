function [  ] = compareAngle( mir, psds_data, varargin )
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

%% 
figure('position',ppos)
legNames ={};
hold on
for curCol=1:max(size(ag_col))
    angleData = ( psds_data.Data(:,ag_col(curCol))- psds_data.Data(:,ag_col(1)) ) ./180.*pi;
    
    plot(tds, dsmple(angleData,ds),'.')
    temp = strsplit(psds_data.Description{ag_col(curCol)});
    legNames{end+1} = ['PSDS ', temp{1}];
end

hold on
% Find nicer y limits..
ymax = 0;
ymin = 0;

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).Va,'o')
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['LTD ',name];
        
        if max(mir.(curArea).(curSlack).Va) > ymax
            ymax = max(mir.(curArea).(curSlack).Va);
        end
        if min(mir.(curArea).(curSlack).Va) < ymin
            ymin = mmin(mir.(curArea).(curSlack).Va);
        end
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        % if same bus, will have same voltage and angle...
        plot(mir.t, mir.(curArea).(curGen).Va,'o')
        
        
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = ['LTD ',name];
        
        if max(mir.(curArea).(curGen).Va) > ymax
            ymax = max(mir.(curArea).(curGen).Va);
        end
        if min(mir.(curArea).(curGen).Va) < ymin
            ymin = min(mir.(curArea).(curGen).Va);
        end
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
if noCase ==1
    title('Comparison of Generator Voltage Angle')
else
    title({'Comparison of Generator Voltage Angle'; ['Case: ', LTDCaseName]})
end
xlabel('Time [sec]')
ylabel('Generator Angle [degrees]')
set(gca,'fontsize',bfz)
xlim(x_lim)
ylim([ymin*1.5,ymax*1.5])

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Angle'],'-pdf'); % to print fig
end

end

