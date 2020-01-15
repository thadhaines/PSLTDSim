function [  ] = compareAmp2( mir, psds_data, varargin )
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
psdsData_col = jfind(psds_data, 'amps');
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

% for each col
for dataCol = psdsData_col
    %   get bus num from description
    splitSTR = split(psds_data.Description{dataCol},':');
    busSTR = splitSTR{1};
    %   get ltd data with bus num
    ltdDataName = ['br',busSTR];
    LTDdata =  mir.branch.(ltdDataName).Amps; % Qbr Amps;
    %   compare data
    pData = psds_data.Data(:,dataCol);
    cData = dsmple(calcDeviation( t, mir, pData, LTDdata ),ds); %calcPdiff or calcDeviation
    %   plot
    plot(tds, cData,'color',grey,'linewidth',.5)
    
    
    %   add legend name
    %...
    
    %   add to running for average
    linesPltd = linesPltd+1;
    absSum = abs(cData)+ absSum;
    
end

    % calculate and plot RMS
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
            legend(legNames)
        end
        grid on
    else % make only general legend
        dataName = [int2str(linesPltd),' Comparisons'];
        legend([datas,rPlot],dataName,'Average Absolute Difference','location','best')
    end
    grid on
    if noCase ==1
        title('Branch Current Flow Difference')
    else
        title({'Branch Current Flow Difference'; ['Case: ', LTDCaseName]})
    end
    xlabel('Time [sec]')
    ylabel('Current [A]')
    set(gca,'fontsize',bfz)
    xlim(x_lim)
    
    % pdf output code
    if printFigs
        set(gcf,'color','w'); % to remove border of figure
        export_fig([LTDCaseName,'Amp2'],'-pdf'); % to print fig
    end
    %% end of function
end

