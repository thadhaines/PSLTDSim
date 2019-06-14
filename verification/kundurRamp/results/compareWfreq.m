function [  ] = compareWfreq( mir, psds_data, varargin )
%compareWfreq Compare LTD mirror and psds simulation data
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
f_col = jfind(psds_data, 'fbu');
%% Calculate weighted freq
Hsys = mir.Hss;
weightedF = zeros(size(psds_data.Data(:,1),1),1);
for area = 1:max(size(mir.areaN)) % for each area
    if debug
        fprintf('area %d\n',mir.areaN(area) )
    end
    curArea = ['A',int2str(area)];
    
    for slack = 1:max(size(mir.(curArea).slackBusN))
        curSlack = ['S',int2str(mir.(curArea).slackBusN(slack))];
        psdsName = mir.(curArea).(curSlack).BusName;
        weight = mir.(curArea).(curSlack).S1.Hpu*mir.(curArea).(curSlack).S1.Mbase;
        a = jfind(psds_data, psdsName);
        genFloc = intersect(a,f_col);
        if size(genFloc,2) >1
            disp('mulit intersections slack:')
            disp(psdsName) % prints name with multi intersections
        end
        genSpd = psds_data.Data(:,genFloc(1)).*(weight/Hsys/60);
        weightedF = weightedF + genSpd;
    end
    for gen = 1:max(size(mir.(curArea).genBusN))
        curGen = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        psdsName = [int2str(mir.(curArea).genBusN(gen)),':',mir.(curArea).(curGen).BusName];
        weight = mir.(curArea).(curGen).G1.Hpu*mir.(curArea).(curGen).G1.Mbase;
        a = jfind(psds_data, psdsName);
        genFloc = intersect(a,f_col);
        if size(genFloc,2) >1
            disp('mulit intersections gen:')
            disp(psdsName) % prints name with multi intersections
        end
        genSpd = psds_data.Data(:,genFloc(1)).*(weight/Hsys/60);
        weightedF = weightedF + genSpd;
    end
    
end
%% Calculate theoretical ss f
beta = 0;
for area = 1:max(size(mir.areaN))
    curArea = ['A',int2str(area)];
    beta = beta + mir.(curArea).beta;
end

sbase = mir.Sbase;
deltaP = mir.Pe(1)-mir.Pe(end); % load change

deltaFpu = deltaP/sbase*(1/beta);
ssPu = 1 + deltaFpu;
ssF = ssPu*60;


%% Plot weighted System frequency responses
figure('position',ppos)

hold on
plot(t, weightedF*60,'color', [0 1 0],'linewidth',1.5)
plot(mir.t, mir.f*60 , 'm-.','linewidth',2)
line([mir.t(1) mir.t(end)],[ssF,ssF],'linestyle',':','color',[.3 0 .7],'linewidth',1)

legend({'Weighted PSDS','LTD','Theoretical SS'},'location','southeast')
xlim(x_lim)
grid on
%title('Comparison of Average System Frequency')
title({'Comparison of Average System Frequency'; ['Case: ', LTDCaseName]})
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'AveF'],'-pdf'); % to print fig
end

%% split out PSDS data corresponding to LTD points and plot Hz difference
% find index of t == 0 in PSLF data
n = 1;
while t(n) ~= 0
    n = n+1;
end
zoft = n; % location of 0 in PSLF data
% first time step from zero used for indexing

mirA = [mir];
for mirror=1:size(mirA,2)
    LTD_ts = mirA(mirror).t(2);
    ts = t(zoft+1);
    fs = round(LTD_ts/ts);
    
    % Collect PSLF data corresponding to LTD data
    ct = 0;
    while ct<=mirA(mirror).t(end)/LTD_ts
        % find index of time at full second
        n = zoft + fs*ct;
        % pull values
        pulledtime(ct+1) = t(n);
        pulledf(ct+1) = weightedF(n); % system 'mean'
        ct = ct+1;
    end
    
    mirA(mirror).PSDSf = pulledf;
    mirA(mirror).PSDSt = pulledtime;
    clear pulledtime pulledf
end

figure('position',ppos)
hold on

plot(mir.t, abs(mir.f -mirA(1).PSDSf)*60, 'm','linewidth',.5)
%legend({'LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec'},'location','northeast')
xlim(x_lim)
grid on
%title('Comparison of Absolute Frequency Deviation from PSDS')
title({'Comparison of Absolute Frequency Deviation from PSDS'; ['Case: ', LTDCaseName]})
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'RelF'],'-pdf'); % to print fig
end

%% end of function
end

