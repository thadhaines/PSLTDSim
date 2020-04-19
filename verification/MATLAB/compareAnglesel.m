function [  ] = compareAnglesel( mir, psds_data, varargin )
%compareAnlge Compare LTD mirror and psds_data angle data
%   optional inputs: LTDCaseName, printFigs, miniFlag, ds, [select bus nums]
% assumes all optional inputs are inserted, plots only select bus numbers

sel = varargin{5} % select nums to print

% color scheme
ltdColors={ [0,0,0], % black
            [1,0,1], % magenta
            [0,1,0], % green
            %[0.090196078431373,  0.745098039215686,   0.811764705882353],
            %"#17becf", % light blue
            [0,1,1], % cyan
            [1,.647,0],% orange
            [.7,.7,.7]% grey
        };

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

linesP = 0; % used for index of ltdColors cell structure

%% find slack name Area
%cycle through areas until one has a slackbus
for areaN =1:max(size(mir.areaN))
    curArea = ['A',int2str(mir.areaN(areaN))];
    if max(size(mir.(curArea).slackBusN)) > 0
        slackNum = ['S',int2str(mir.(curArea).slackBusN)];
        slackName = mir.(curArea).(slackNum).BusName;
        bNum = mir.(curArea).(slackNum).BusNum;
        bName = mir.(curArea).(slackNum).BusName;
        tarID = 1;
        psdsDataNdx = findPSDSndx(psds_data, bNum, bName, tarID, 'abug' );
        break
    end % if area has slackBusN
end % for each area in mirror

%% find where ameta and slack name intersect
slackAng = psds_data.Data(:,psdsDataNdx);

%% plot
figure('position',ppos)

legNames ={};
hold on
for curCol=1:max(size(ag_col))
    
    temp = strsplit(psds_data.Description{ag_col(curCol)});
      busNum = strsplit(temp{1},':');
    busNum = str2num(cell2mat(busNum(1))); % pain in the ass cell->char->num
if ismember(busNum,sel)
    angleData = rad2deg(unwrap(deg2rad(( psds_data.Data(:,ag_col(curCol))- slackAng ))));
    plot(tds, dsmple(angleData,ds),'.-','color',ltdColors{linesP+1})
    legNames{end+1} = ['PSDS ', temp{1}];
    linesP = mod(linesP+1 , size(ltdColors,1));
end
end

hold on
% Find nicer y limits..
ymax = 0;
ymin = 0;

for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) );
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        if ismember(mir.(curArea).slackBusN(slack),sel)
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        angData = rad2deg(mir.(curArea).(curSlack).Va);
        stairs(mir.t, angData,'-o','color',ltdColors{linesP+1},'linewidth',1.5)
        
        linesP = mod(linesP+1 , size(ltdColors,1));
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['PSLTDSim ',name];
        
        if max(angData) > ymax
            ymax = max(angData);
        end
        if min(angData) < ymin
            ymin = mmin(angData);
        end
        end
    end
    
    uniqueEntry = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(mir.(curArea).genBusN))
        if ismember(mir.(curArea).genBusN(gen),sel)
            if ismember(mir.(curArea).genBusN(gen),uniqueEntry)
                % remove from unique Entry
            uniqueEntry(uniqueEntry == mir.(curArea).genBusN(gen)) = [];
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        % if same bus, will have same voltage and angle...
        angData = rad2deg(mir.(curArea).(curGen).Va);
        stairs(mir.t, angData,'-o','color',ltdColors{linesP+1},'linewidth',1.5)
        linesP = mod(linesP+1 , size(ltdColors,1));       
        name = [(curArea),'.',(curGen)];
        legNames{end+1} = ['PSLTDSim ',name];
        
         if max(angData) > ymax
            ymax = max(angData);
        end
        if min(angData) < ymin
            ymin = min(angData);
        end
            end
        end
    end
    
end
%if makeLegend
    legend(legNames, 'location','east')
%end
grid on
if noCase ==1
    title('Select Comparison of Generator Voltage Angle')
else
    title({'Select Comparison of Generator Voltage Angle'; ['Case: ', LTDCaseName]})
end
xlabel('Time [sec]')
ylabel('Generator Angle [degrees]')
set(gca,'fontsize',bfz)
xlim(x_lim)
%ylim([ymin*1.5,ymax*1.5]);

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Anglesel'],'-pdf'); % to print fig
end

end

