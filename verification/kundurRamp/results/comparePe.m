function [  ] = comparePe( mir, psds_data, varargin )
%comparePe Compare LTD mirror and psds simulation data
%   optional inputs: case name, print figs, figure size
%   PSDS angles need to have the reference subtracted from them to be centered
%   around 0

% Handle optional inputs
if nargin == 2
    printFigs = 0;
elseif nargin >= 4
    LTDCaseName = varargin{1};
    printFigs = varargin{2};
end

if nargin < 5
    ppos = [18 521 1252 373];
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
pg_col = jfind(psds_data, 'pg');

%% Pe  Comparison
figure('position',ppos)
legNames ={};
hold on
for curCol=1:max(size(pg_col))
    plot(t, psds_data.Data(:,pg_col(curCol)))
    temp = strsplit(psds_data.Description{pg_col(curCol)});
    legNames{end+1} = ['PSDS ', temp{1}];
end

hold on

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        plot(mir.t, mir.(curArea).(curSlack).S1.Pe,'--o')
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['LTD ',name];
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        
        plot(mir.t, mir.(curArea).(curGen).G1.Pe,'--o')
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = ['LTD ',name];
    end
    
end
if makeLegend
    legend(legNames)
end
grid on
%title('Comparison of Real Power Output')
title({'Comparison of Real Power Output'; ['Case: ', LTDCaseName]})
xlabel('Time [sec]')
ylabel('Power [MW]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Pe'],'-pdf'); % to print fig
end
%% end of function
end

