function [  ] = comparePbr1( mir, psds_data, varargin )
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
psdsData_col = jfind(psds_data, 'pbr');
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

% create string array from char
numBranch = size(mir.branch.branchN,1);
%branchSTR = strings(numBranch,1);
%for n = 1: numBranch
%    charVec = mir.branch.branchN(n,:);
%    branchSTR(n) = strtrim(string(charVec));
%end
branchSTR = cellstr(mir.branch.branchN);
uniBranch = unique(branchSTR);

legNames = {};
hold on

%% power in MW
psdsData_col = jfind(psds_data, 'pbr');
%
figure('position',ppos)
legNames={};
%% Plot LTD mw flows...
for br = 1:size(uniBranch,1)
    brID = strcat('br',uniBranch(br));
    plot(mir.t, mir.branch.(char(brID)).Pbr,'s') 
    hold on
    legNames{end+1} =  ['LTD ', char(strrep(uniBranch(br),'_',' '))];
end

%% plot psds flows
for index = psdsData_col
    plot(t, psds_data.Data(:,index),'--','linewidth',2)
    fullDesc = cellstr(psds_data.Description{index});
    splitStr = strsplit(fullDesc{1},':');
    legNames{end+1} =  ['PSDS ',splitStr{1} ,' to ',splitStr{4} ];
end

%%
title({'Branch Real Power Flow'; ['Case: ', LTDCaseName]})

legend(legNames,'location','east')
grid on
xlabel('Time [sec]')
ylabel('Power [MW]')
set(gca,'fontsize',bfz)
%set(gcf,'position',ppos)
xlim(x_lim)
    % pdf output code
    if printFigs
        set(gcf,'color','w'); % to remove border of figure
        export_fig([LTDCaseName,'Pbr1'],'-pdf'); % to print fig
    end
    %% end of function
end

