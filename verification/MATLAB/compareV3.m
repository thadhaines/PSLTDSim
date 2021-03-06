function [  ] = compareV2( mir, psds_data, varargin )
%compareV Compare LTD mirror and psds simulation data
%   optional inputs: case name, print figs, figure size
%   PSDS angles need to have the reference subtracted from them to be centered
%   around 0

% Handle optional inputs

if nargin > 6
    bfz = varargin{5};
else
    bfz = 13;
end

if nargin > 7
    outFile = varargin{6};
else
    outFile = '-pdf';
end

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
%bfz = 13;
t = psds_data.Data(:,1); % PSDS time

% funtion specific
v_col = jfind(psds_data, 'vmeta');
ds = varargin{4};
tds = dsmple(t,ds);
dLeg = false;
%if max(size(v_col)) > 20
%    makeLegend = 0;
%end

% for future RMS calcs
linesPltd = 0;
rSum = tds.*0;
grey = [.75,.75,.75];

                absSum = 0;
%% Voltage Comparison
figure('position',ppos)
legNames = {};
%set(gca,'ColorOrder',flipud(imcomplement(colormap(spring(floor(max(size(v_col)/2))))))) % to make mess of lines look nicer

hold on
% For id, uncomment linestyle and change make legend to 1
%set(gca,'linestyleorder',{'-', '-*', '-x', '-+', '-^', '-v', '--', '--*', '--x', '--+', '--^', '--v', ':', ':*', ':x', ':+', ':^', ':v'})

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
            
            % Comparison and RMS
            LTDdata = mir.(curArea).(curSlack).Vm;
            bNum = mir.(curArea).(curSlack).BusNum;
            bName = mir.(curArea).(curSlack).BusName;
            tarID = 1;
            psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'vmeta' );
            
            
            if max(size(psdsDataNdx))==1
                pData = psds_data.Data(:,psdsDataNdx);
                cData = dsmple(calcPdiff( t, mir, pData, LTDdata),ds);
                plot(tds, cData,'color',grey,'linewidth',.5)
                legNames{end+1} = ['LTD ',name];
                linesPltd = linesPltd+1;
                rSum = rSum+cData.^2;
                absSum = abs(cData)+ absSum;
            end
            
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
            bNum = mir.(curArea).(curGen).BusNum;
            bName = mir.(curArea).(curGen).BusName;
            tarID = 1;
            psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'vmeta' );
            
            
            if max(size(psdsDataNdx))==1
                pData = psds_data.Data(:,psdsDataNdx);
                cData = dsmple(calcPdiff( t, mir, pData, LTDdata ),ds);
                plot(tds, cData,'color',grey,'linewidth',.5)
                
                linesPltd = linesPltd+1;
                rSum = rSum+cData.^2;
                absSum = abs(cData)+ absSum;
            end
            
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
            bNum = mir.(curArea).(curLoadbus).BusNum;
            bName = mir.(curArea).(curLoadbus).BusName;
            tarID = 1;
            psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'vmeta' );
            
            
            if max(size(psdsDataNdx))==1
                pData = psds_data.Data(:,psdsDataNdx);
                cData = dsmple(calcPdiff( t, mir, pData, LTDdata ),ds);
                plot(tds, cData,'color',grey,'linewidth',.5)
                
                linesPltd = linesPltd+1;
                rSum = rSum+cData.^2;
                absSum = abs(cData)+ absSum;
            end
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
            
            bNum = mir.(curArea).(curXbus).BusNum;
            bName = mir.(curArea).(curXbus).BusName;
            tarID = 1;
            psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'vmeta' );
            
            
            if max(size(psdsDataNdx))==1
                pData = psds_data.Data(:,psdsDataNdx);
                cData = dsmple(calcPdiff( t, mir, pData, LTDdata),ds);
                plot(tds, cData,'color',grey,'linewidth',.5)
                
                linesPltd = linesPltd+1;
                rSum = rSum+cData.^2;
                absSum = abs(cData)+ absSum;
            end
            
        end
        
    end
end
    % calculate and plot RMS
    RMS = sqrt(rSum./linesPltd);
    absDevMean = absSum ./ linesPltd;
    datas = plot(tds, absDevMean,'color',grey,'linewidth',1.5);
    rPlot = plot(tds, absDevMean,'k','linewidth',1.5);
    
    
    if makeLegend % make individual legend
        if dLeg
            if max(size(legNames)) > 15
                loc = 'eastoutside';
            else
                loc = 'best';
            end
            
            leg = columnlegend(2, cellstr(legNames), 'location',loc);
            set(leg,'FontSize',bfz)
        else
            legend(legNames,'location','best')
        end
        grid on
    else % make only general legend
        dataName = [int2str(linesPltd),' Comparisons'];
        legend([datas,rPlot],dataName,'Average Absolute Percent Difference','location','best')
    end
    grid on
    if noCase ==1
        title('Bus Voltage Percent Difference')
    else
        title({'Bus Voltage Percent Difference'; ['Case: ', LTDCaseName]})
    end
    xlabel('Time [sec]')
    ylabel('Percent Difference [%]')
    set(gca,'fontsize',bfz)
    xlim(x_lim)
    
    % pdf output code
    if printFigs
        set(gcf,'color','w'); % to remove border of figure
        export_fig([LTDCaseName,'V3'],outFile); % to print fig
    end
    %% end of function
end

