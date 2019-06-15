function [  ] = comparePe( mir, psds_data, varargin )
%compareV Compare LTD mirror and psds simulation data
%   optional inputs: case name, print figs, figure size
%   PSDS angles need to have the reference subtracted from them to be centered
%   around 0

% Handle optional inputs
if nargin == 2
    printFigs = 0;
    noCase = 1;
elseif nargin >= 4
    LTDCaseName = varargin{1};
    printFigs = varargin{2};
    noCase = 0;
end

if nargin < 5
    ppos = [18 312 1252 373];
else
    ppos = varargin{3};
end

% varables for plots to work
debug = 0;
makeLegend = 1;
x_lim = [mir.t(1), mir.t(end)];
bfz = 13;
t = psds_data.Data(:,1); % PSDS time

% funtion specific
v_col = jfind(psds_data, 'vmeta');

%% Voltage Comparison
figure('position',ppos)
legNames = {};

hold on
for bv=1:max(size(v_col))
    plot(t, psds_data.Data(:,v_col(bv)))
    temp = strsplit(psds_data.Description{v_col(bv)});
    legNames{end+1} = ['PSDS ', temp{1}];
end

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    uniqueEntry = unique(mir.(curArea).slackBusN);
    for slack = 1:max(size(mir.(curArea).slackBusN))
        if ismember(mir.(curArea).slackBusN(slack),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).slackBusN(slack)) = [];
            curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
            plot(mir.t, mir.(curArea).(curSlack).Vm,'--o')
            name = [(curArea),'.',(curSlack)];
            legNames{end+1} = ['LTD ',name];
        end
    end
    uniqueEntry = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(mir.(curArea).genBusN))
        if ismember(mir.(curArea).genBusN(gen),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).genBusN(gen)) = [];
            curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
            plot(mir.t, mir.(curArea).(curGen).Vm,'--o')
            name = [(curArea),'.',(curGen)];
            legNames{end+1} = ['LTD ',name];
        end
    end
    uniqueEntry = unique(mir.(curArea).loadBusN);
    for load = 1:max(size(mir.(curArea).loadBusN))
        if ismember(mir.(curArea).loadBusN(load),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).loadBusN(load)) = [];
            curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
            plot(mir.t, mir.(curArea).(curLoadbus).Vm,'x')
            name = [(curArea),'.',(curLoadbus)];
            legNames{end+1} = ['LTD ',name];
        end
    end
    uniqueEntry = unique(mir.(curArea).xBusN);
    for xbus = 1:max(size(mir.(curArea).xBusN))
        % remove number from unique
        if ismember(mir.(curArea).xBusN(xbus),uniqueEntry)
            uniqueEntry(uniqueEntry == mir.(curArea).xBusN(xbus)) = [];
            curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
            plot(mir.t, mir.(curArea).(curXbus).Vm,'s')
            name = [(curArea),'.',(curXbus)];
            legNames{end+1} = ['LTD ',name];
        end
    end
end
if makeLegend
    legend(legNames)
    grid on
end
grid on
if noCase ==1
    title('Comparison of Bus Voltage')
else
    title({'Comparison of Bus Voltage'; ['Case: ', LTDCaseName]})
end
xlabel('Time [sec]')
ylabel('Voltage [pu]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'V'],'-pdf'); % to print fig
end
%% end of function
end

