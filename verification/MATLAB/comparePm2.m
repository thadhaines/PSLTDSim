function [  ] = comparePe( mir, psds_data, varargin )
%comparePe Compare LTD mirror and psds simulation data
%   optional inputs: case name, print figs, figure size

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
t = psds_data.Data(:,1); % PSDS time
ds = varargin{4};
tds = dsmple(t, ds);
% funtion specific
pm_col = jfind(psds_data, 'pm');

% for future RMS calcs
linesPltd = 0;
rSum = tds.*0;
grey = [.75,.75,.75];
lineSumd = 0;

                absSum = 0;
%% Pm  Comparison
figure('position',ppos)
legNames ={};
hold on
%set(gca,'ColorOrder',flipud(imcomplement(colormap(spring(floor(max(size(pm_col))))))))
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
        LTDdata = mir.(curArea).(curSlack).S1.Pm;
        
        % new find index and RMS
        bNum = mir.(curArea).(curSlack).BusNum;
        bName = mir.(curArea).(curSlack).BusName;
        tarID = 1;
        psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'pm' );
        
        if max(size(psdsDataNdx))==1
            pData = psds_data.Data(:,psdsDataNdx);
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
            LTDdata = mir.(curArea).(curGenBus).(curGen).Pm;
            % Comparison and RMS
            bNum = mir.(curArea).(curGenBus).BusNum;
            bName = mir.(curArea).(curGenBus).BusName;
            tarID = GenId;
            psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'pm' );
            
            if max(size(psdsDataNdx))==1
                pData = psds_data.Data(:,psdsDataNdx);
                if isempty(pData)
                    continue
                end
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
        end
        
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
    title('Mechanical Power Difference')
else
    title({'Mechanical Power Difference'; ['Case: ', LTDCaseName]})
end

xlabel('Time [sec]')
ylabel('Power [MW]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Pm2'],outFile); % to print fig
end
%% end of function
end

