function [  ] = comparePe( mir, psds_data, varargin )
%compareV Compare LTD mirror and psds simulation data
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
makeLegend = 0;
x_lim = [mir.t(1), mir.t(end)];
bfz = 13;
t = psds_data.Data(:,1); % PSDS time

% funtion specific
v_col = jfind(psds_data, 'vmeta');
ds = varargin{4};
tds = dsmple(t,ds);
dLeg = false;
%if max(size(v_col)) > 20
%    makeLegend = 0;
%end

%% Voltage Comparison
figure('position',ppos)
legNames = {};

hold on
set(gca,'linestyleorder',{'-', '-*', '-x', '-+', '-^', '-v', '--', '--*', '--x', '--+', '--^', '--v', ':', ':*', ':x', ':+', ':^', ':v'})

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
            name = [(curArea),'.',(curSlack)];
            legNames{end+1} = ['LTD ',name];
            
            % Comparison addition
            LTDdata = mir.(curArea).(curSlack).Vm;
            psdsDataNdx = intersect(jfind(psds_data, mir.(curArea).(curSlack).BusName),jfind(psds_data, 'vbug'));
            if max(size(psdsDataNdx))>1
                % check for multiple intersect
                if debug disp(name);end
                psdsDataNdx = intersect(jfind(psds_data, int2str(mir.(curArea).(curSlack).BusNum)),psdsDataNdx);
            end
            pData = psds_data.Data(:,psdsDataNdx);
            cData = calcDeviation( t, mir, pData, LTDdata );
            plot(tds, dsmple(cData,ds))
            
        end
    end
    uniqueEntry = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(mir.(curArea).genBusN))
        if ismember(mir.(curArea).genBusN(gen),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).genBusN(gen)) = [];
            curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
            name = [(curArea),'.',(curGen)];
            legNames{end+1} = ['LTD ',name];
            
            % Comparison addition
            LTDdata = mir.(curArea).(curGen).Vm;
            psdsDataNdx = intersect(jfind(psds_data, mir.(curArea).(curGen).BusName),jfind(psds_data, 'vbug'));
            if max(size(psdsDataNdx))>1
                % check for multiple names
                if debug disp(name);end;
                psdsDataNdx = intersect(jfind(psds_data, int2str(mir.(curArea).(curGen).BusNum)),psdsDataNdx);
            end
            pData = psds_data.Data(:,psdsDataNdx);
            cData = calcDeviation( t, mir, pData, LTDdata );
            plot(tds, dsmple(cData,ds))
            
        end
    end
    uniqueEntry = unique(mir.(curArea).loadBusN);
    for load = 1:max(size(mir.(curArea).loadBusN))
        if ismember(mir.(curArea).loadBusN(load),uniqueEntry)
            % remove number from unique
            uniqueEntry(uniqueEntry == mir.(curArea).loadBusN(load)) = [];
            curLoadbus = ['L',int2str(mir.(curArea).loadBusN(load))];
            name = [(curArea),'.',(curLoadbus)];
            legNames{end+1} = ['LTD ',name];
            
            % Comparison addition
            LTDdata = mir.(curArea).(curLoadbus).Vm;
            psdsDataNdx = intersect(jfind(psds_data, mir.(curArea).(curLoadbus).BusName),jfind(psds_data, 'vbul'));
            if max(size(psdsDataNdx))>1
                % check for multiple intersect
                if debug disp(name); end;
                psdsDataNdx = intersect(jfind(psds_data, int2str(mir.(curArea).(curLoadbus).BusNum)),psdsDataNdx);
            end
            pData = psds_data.Data(:,psdsDataNdx);
            cData = calcDeviation( t, mir, pData, LTDdata );
            plot(tds, dsmple(cData,ds))
        end
    end
    
    uniqueEntry = unique(mir.(curArea).xBusN);
    for xbus = 1:max(size(mir.(curArea).xBusN))
        % remove number from unique
        if ismember(mir.(curArea).xBusN(xbus),uniqueEntry)
            uniqueEntry(uniqueEntry == mir.(curArea).xBusN(xbus)) = [];
            curXbus = ['x',int2str(mir.(curArea).xBusN(xbus))];
            name = [(curArea),'.',(curXbus)];
            legNames{end+1} = ['LTD ',name];
            
            % Comparison addition
            LTDdata = mir.(curArea).(curXbus).Vm;
            psdsDataNdx = intersect(jfind(psds_data, mir.(curArea).(curXbus).BusName),jfind(psds_data, 'vbus'));
            if max(size(psdsDataNdx))>1
                % check for multiple intersect
                if debug disp(name); end
                psdsDataNdx = intersect(jfind(psds_data, int2str(mir.(curArea).(curXbus).BusNum)),psdsDataNdx);
                if max(size(psdsDataNdx))>1
                    % check for continued multipe intersects...
                    for dupe=1:max(size(psdsDataNdx))
                        desc = strjoin(psds_data.Description(psdsDataNdx(dupe)));
                        if debug disp(desc);end
                        bus = strsplit(desc,':');
                        bus = str2double(bus(1));
                        if bus == mir.(curArea).(curXbus).BusNum
                            psdsDataNdx = psdsDataNdx(dupe);
                            break
                        end
                        
                    end
                end
                pData = psds_data.Data(:,psdsDataNdx);
                cData = calcDeviation( t, mir, pData, LTDdata );
                plot(tds, dsmple(cData,ds))
            end
        end
        
    end
    if makeLegend
        if dLeg
            if max(size(legNames)) > 15
                loc = 'eastoutside';
            else
                loc = 'best';
            end
            
            leg = columnlegend(2, cellstr(legNames), 'location',loc);
            set(leg,'FontSize',bfz)
        else
            legend(legNames)
        end
        grid on
    end
    grid on
    if noCase ==1
        title('Deviation of LTD Bus Voltage from PSDS')
    else
        title({'Deviation of LTD Bus Voltage from PSDS'; ['Case: ', LTDCaseName]})
    end
    xlabel('Time [sec]')
    ylabel('Voltage [pu]')
    set(gca,'fontsize',bfz)
    xlim(x_lim)
    
    % pdf output code
    if printFigs
        set(gcf,'color','w'); % to remove border of figure
        export_fig([LTDCaseName,'V2'],'-pdf'); % to print fig
    end
    %% end of function
end

