function [  ] = compareQsel( mir, psds_data, varargin )
%compareQ Compare LTD mirror and psds simulation data
%   optional inputs: LTDCaseName, printFigs, miniFlag, ds, [select bus nums]
% assumes all optional inputs are inserted, plots only select bus numbers

sel = varargin{5}; % select nums to print
if nargin > 7
    bfz = varargin{6};
else
    bfz = 13;
end
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
% color scheme
ltdColors={ 
   % [.7,.7,.7],% grey
    [0,0,0], % black
    [1,0,1], % magenta
    [0,1,0], % green
    %[0.090196078431373,  0.745098039215686,   0.811764705882353],
    %"#17becf", % light blue
    [0,0.75,1], % blue
    [0,1,1], % cyan
    [1,.647,0],% orange
    };
linesP = 0; % used for index of ltdColors cell structure

% varables for plots to work
debug = 0;
makeLegend = 1;
x_lim = [mir.t(1), mir.t(end)];
%bfz = 13;
t = psds_data.Data(:,1); % PSDS time

% funtion specific
qg_col = jfind(psds_data, 'qg');
ds = varargin{4};
tds = dsmple(t,ds);
dLeg = false;

%% Q Comparison
figure('position',ppos)
set(gca,'linestyleorder',{'-',':.','-.','--',':x'})
legNames = {};
hold on


%% LTD plotting
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        if ismember(mir.(curArea).slackBusN(slack),sel)
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        %plot(mir.t, mir.(curArea).(curSlack).S1.Q,'s')
        stairs(mir.t, mir.(curArea).(curSlack).S1.Q,'-o','color',ltdColors{linesP+1},'linewidth',1)
        linesP = mod(linesP+1 , size(ltdColors,1));
                
        name = [(curArea),'.',(curSlack)];
        legNames{end+1} = ['PSLTDSim ',name];
        end
    end
    
uniueGens = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(uniueGens))
        
        if ismember(mir.(curArea).genBusN(gen),sel)
        curGenBus = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        for GenId = 1:mir.(curArea).(curGenBus).Ngen
            curGen = ['G',int2str(GenId)];
            if GenId > 1
                %plot(mir.t, mir.(curArea).(curGenBus).(curGen).Q,'x')
            stairs(mir.t, mir.(curArea).(curGenBus).(curGen).Q,'-o','color',ltdColors{linesP+1},'linewidth',1)
            linesP = mod(linesP+1 , size(ltdColors,1));
            else
                %plot(mir.t, mir.(curArea).(curGenBus).(curGen).Q,'o')
                stairs(mir.t, mir.(curArea).(curGenBus).(curGen).Q,'-o','color',ltdColors{linesP+1},'linewidth',1)
                linesP = mod(linesP+1 , size(ltdColors,1));
            end
            name = [(curArea),'.',(curGenBus),'.',int2str(GenId)];
            legNames{end+1} = ['PSLTDSim ',name];
        end
        end
    end
    
end
%% PSDS plotting
for curCol=1:max(size(qg_col))
    temp = strsplit(psds_data.Description{qg_col(curCol)});
    busNum = strsplit(temp{1},':');
    busNum = str2num(cell2mat(busNum(1))); % pain in the ass cell->char->num
if ismember(busNum,sel)
%     % handle multiple bus gens
%     if curCol >1
%         dupe = strcmp(['PSDS ', temp{1}],legNames{curCol-1});
%     else
%         dupe = 0;
%     end
    
    legNames{end+1} = ['PSDS ', temp{1}];
    % downsample data for faster plots
    dsData = dsmple(psds_data.Data(:,qg_col(curCol)),ds);
    
%     if dupe == 1
%          plot(tds, dsData,'--')
%     else
        %plot(tds, dsData)
        plot(tds, dsData,'-','color',ltdColors{linesP+1},'linewidth',1.5)
        linesP = mod(linesP+1 , size(ltdColors,1));
%     end
end
    
end
%%
  legend(legNames, 'location', 'best','FontSize',13)

grid on
if noCase ==1
    title('Select Comparison of Reactive Power')
else
    title({'Select Comparison of Reactive Power'; ['Case: ', LTDCaseName]})
end
xlabel('Time [sec]')
ylabel('Reactive Power [MVAR]')
set(gca,'fontsize',bfz)
xlim(x_lim)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Qsel'],'-pdf'); % to print fig
end
%% end of function
end

