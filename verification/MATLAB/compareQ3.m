function [  ] = compareQ3( mir, psds_data, varargin )
%comparePe Compare LTD mirror and psds simulation data
%   optional inputs: case name, print figs, figure size

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
ds = varargin{4};
tds = dsmple(t, ds);
% funtion specific
qg_col = jfind(psds_data, 'qg');

%% Pe  Comparison
figure('position',ppos)
legNames ={};
hold on
set(gca,'ColorOrder',flipud(imcomplement(colormap(spring(floor(max(size(qg_col))/1))))))
%set(gca,'linestyleorder',{'-', '-*', '-x', '-+', '-^', '-v', '--', '--*', '--x', '--+', '--^', '--v', ':', ':*', ':x', ':+', ':^', ':v'})
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        name = [(curArea),'.',(curSlack)];
        
        % Comparison addition
        LTDdata = mir.(curArea).(curSlack).S1.Q;
        % find psds data by bus name
        psdsDataNdx = intersect(jfind(psds_data, mir.(curArea).(curSlack).BusName),qg_col);
        if max(size(psdsDataNdx))>1
            % check for multiple intersect, search by bus number
            if debug disp(name); end
            psdsDataNdx = intersect(jfind(psds_data, int2str(mir.(curArea).(curSlack).BusNum)),psdsDataNdx);
            if max(size(psdsDataNdx))>1
                % check for continued multipe intersects... actually
                % compare bus numbers
                for dupe=1:max(size(psdsDataNdx))
                    desc = strjoin(psds_data.Description(psdsDataNdx(dupe)));
                    if debug disp(desc);end
                    bus = strsplit(desc,':');
                    bus = str2double(bus(1));
                    if bus == mir.(curArea).(curSlack).BusNum
                        psdsDataNdx = psdsDataNdx(dupe);
                        break
                    end
                    
                end
            end
        end
        pData = psds_data.Data(:,psdsDataNdx);
        cData = calcPdiff( t, mir, pData, LTDdata );
        plot(tds, dsmple(cData,ds))
        
        legNames{end+1} = [int2str(mir.(curArea).slackBusN(slack))];
        
    end
    uniueGens = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(uniueGens))
        curGenBus = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        for GenId = 1:mir.(curArea).(curGenBus).Ngen
            curGen = ['G',int2str(GenId)];
            
            name = [int2str(mir.(curArea).genBusN(gen)),' ',int2str(GenId)];
            
            %start paste
            % Comparison addition
            LTDdata = mir.(curArea).(curGenBus).(curGen).Q;
            % find psds data by bus name
            psdsDataNdx = intersect(jfind(psds_data, mir.(curArea).(curGenBus).BusName),qg_col);
            if max(size(psdsDataNdx))>1
                % check for multiple intersect, search by bus number
                if debug disp(name); end
                psdsDataNdx = intersect(jfind(psds_data, int2str(mir.(curArea).(curGenBus).BusNum)),psdsDataNdx);
                if max(size(psdsDataNdx))>1
                    % check for continued multipe intersects... actually
                    % compare bus numbers
                    for dupe=1:max(size(psdsDataNdx))
                        desc = strjoin(psds_data.Description(psdsDataNdx(dupe)));
                        if debug disp(desc);end
                        % Should maybe check id?
                        bus = strsplit(desc,':');
                        bus = str2double(bus(1));
                        if bus == mir.(curArea).(curGenBus).BusNum
                            psdsDataNdx = psdsDataNdx(dupe);
                            break
                        end
                        
                    end
                end
            end
            pData = psds_data.Data(:,psdsDataNdx);
            cData = calcPdiff( t, mir, pData, LTDdata );
            plot(tds, dsmple(cData,ds))
            
            legNames{end+1} = [name];
            %end paste
        end
        
    end
    if makeLegend
        legend(legNames)
    end
    grid on
    if noCase ==1
        title('Percent Difference of LTD and PSDS Reactive Power Outputs')
    else
        title({'Percent Difference of LTD and PSDS Reactive Power Outputs'; ['Case: ', LTDCaseName]})
    end
    
    xlabel('Time [sec]')
    ylabel('Percent Difference [%]')
    set(gca,'fontsize',bfz)
    xlim(x_lim)
    
    % pdf output code
    if printFigs
        set(gcf,'color','w'); % to remove border of figure
        export_fig([LTDCaseName,'Q3'],'-pdf'); % to print fig
    end
    %% end of function
end

