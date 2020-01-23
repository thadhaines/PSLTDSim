function [  ] = compareQ3ALT( mir, psds_data, varargin )
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
pg_col = jfind(psds_data, 'qg');

% for future RMS calcs
linesPltd = 0;
rSum = tds.*0;
grey = [.75,.75,.75];
lineSumd = 0;
absSum = 0;

% large val settings
largeVal = false;
largeValLim = 150;
minVal = 0;
maxVal = 0;
%% Pe  Comparison
figure('position',ppos)
legNames ={};
hold on
%set(gca,'ColorOrder',flipud(imcomplement(colormap(spring(max(size(pg_col)))))))
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
        
        % Comparison and RMS
        bNum = mir.(curArea).(curSlack).BusNum;
        bName = mir.(curArea).(curSlack).BusName;
        tarID = 1;
        psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'qg' );
        
        if max(size(psdsDataNdx))==1
            pData = psds_data.Data(:,psdsDataNdx);
            cData = dsmple(calcPdiff( t, mir, pData, LTDdata),ds);
            plot(tds, cData,'color',grey,'linewidth',.5)
            
            % Handle checking for large values and collecting min/max vals
            if max(abs(cData)) > largeValLim
                largeVal = true;
                
                tempLargeVal = max(cData);
                tempMinVal = min(cData);
                
                if tempLargeVal > maxVal
                    maxVal = tempLargeVal;
                end
                if tempMinVal < minVal
                    minVal = tempMinVal;
                end
            end
            
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
            LTDdata = mir.(curArea).(curGenBus).(curGen).Q;
            % Comparison and RMS
            bNum = mir.(curArea).(curGenBus).BusNum;
            bName = mir.(curArea).(curGenBus).BusName;
            tarID = GenId;
            psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'qg' );
            
            if max(size(psdsDataNdx))==1
                pData = psds_data.Data(:,psdsDataNdx);
                cData = dsmple(calcPdiff( t, mir, pData, LTDdata),ds);
                plot(tds, cData,'color',grey,'linewidth',.5)
                
                % Handle checking for large values and collecting min/max vals
                if max(abs(cData)) > largeValLim
                    largeVal = true;
                    
                    tempLargeVal = max(cData);
                    tempMinVal = min(cData);
                    
                    if tempLargeVal > maxVal
                        maxVal = tempLargeVal;
                    end
                    if tempMinVal < minVal
                        minVal = tempMinVal;
                    end
                end
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
absDevMean = absSum ./ linesPltd;
datas = plot(tds, absDevMean,'color',grey,'linewidth',1.5);
rPlot = plot(tds, absDevMean,'k','linewidth',1.5);

% large val handling
if largeVal
    % adjust y lim to fit absDevMean Data
    newY = max(absDevMean)*1.5;
    if newY > 100
        newY = 100;
    end
    ylim([-newY, newY])
end

if makeLegend
    legend(legNames)
else % make only general legend
    dataName = [int2str(linesPltd),' Comparisons'];
    if largeVal
        point = plot(0,0,'w.','markersize',.001);
        infoCVec = ['Max = ',int2str(maxVal),'%, Min = ',int2str(minVal),'%'];
        legend([datas,rPlot, point],dataName,'Average Absolute Percent Difference', ...
            infoCVec,'location','southeast')
    else
        legend([datas,rPlot],dataName,'Average Absolute Percent Difference','location','best')
    end
end
grid on
if noCase ==1
    title('Reactive Power Percent Difference')
else
    title({'Reactive Power Percent Difference'; ['Case: ', LTDCaseName]})
end

xlabel('Time [sec]')
ylabel('Percent Difference [%]')
set(gca,'fontsize',bfz)
%set(gca,'GridLineStyle','--')
%set(gca, 'GridAlpha', .07)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Q3ALT'],'-pdf'); % to print fig
end
%% end of function
end

