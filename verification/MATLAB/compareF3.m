function [  ] = compareF3( mir, psds_data, varargin )
%compareF3 Compare LTD mirror and psds simulation data
%   optional inputs: case name, print figs, figure size
%   Handles trips (change of weights for ave freq), and system losses

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
f_col = jfind(psds_data, 'fbu');

ds = varargin{4}
genChange = varargin{5}


grey = [.75,.75,.75];
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
        
        % consider only generators that stay on entire sim
        genSt = mir.(curArea).(curSlack).S1.St;
        if all(genSt, 1)
        weight = mir.(curArea).(curSlack).S1.Hpu * mir.(curArea).(curSlack).S1.Mbase;
        else
            weight = 0;
        end
        a = jfind(psds_data, psdsName);
        genFloc = intersect(a,f_col);
        if size(genFloc,2) >1
            disp('mulit intersections slack:')
            disp(psdsName) % prints name with multi intersections
        end
        genSpd = psds_data.Data(:,genFloc(1)).*(weight/Hsys/60);
        weightedF = weightedF + genSpd;
    end
    uniueGens = unique(mir.(curArea).genBusN);
    for gen = 1:max(size(uniueGens))
        curGenBus = ['G',int2str(mir.(curArea).genBusN(gen))];
        % place for for each gen in Ngen...
        for GenId = 1:mir.(curArea).(curGenBus).Ngen
            curGen = ['G',int2str(GenId)];
            psdsName = [int2str(mir.(curArea).(curGenBus).BusNum),':',mir.(curArea).(curGenBus).BusName];
            
            % consider only generators that stay on entire sim
        genSt = mir.(curArea).(curGenBus).(curGen).St;
        if all(genSt, 1)
        weight = mir.(curArea).(curGenBus).(curGen).Hpu * mir.(curArea).(curGenBus).(curGen).Mbase;
        else
            weight = 0;
        end
        
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
    
end
%% Calculate theoretical ss f
beta = 0;
for area = 1:max(size(mir.areaN))
    curArea = ['A',int2str(area)];
    beta = beta + mir.(curArea).beta;
end

sbase = mir.Sbase;
deltaP = genChange + mir.Pe(1)-mir.Pe(end); % load change
%deltaP = -212.5 + deltaP % specific to miniWECC gen trip 0
deltaFpu = deltaP/sbase*(1/beta);
ssPu = 1 + deltaFpu;
ssF = ssPu*60;


%% Plot weighted System frequency responses
figure('position',ppos)

hold on
% plot all freq
numF = 0;
for freq=1:max(size(f_col)-1)
    plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(freq)),ds),'color',grey,'linewidth',.5,'HandleVisibility','off') % all others
    numF = numF +1;
end
plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(size(f_col,2))), ds),'color',grey,'linewidth',1) % last Freq
numF = numF +1;
numFstr = [int2str(numF),' PSDS'];


% weighted psds
plot(dsmple(t,ds), dsmple(weightedF*60,ds) ,'k','linewidth',1.75)

% LTD
plot(mir.t, mir.f*60 , 'm','linewidth',1.5)
% Theoretical SS
line([mir.t(1) mir.t(end)],[ssF,ssF],'linestyle','--')%,'color',[0,1,1],'linewidth',1) %[.3 0 .7]

legend({numFstr,'Weighted PSDS','LTD','Theoretical SS'},'location','best')
xlim(x_lim)
grid on
if noCase ==1
    title('Comparison of Average System Frequency')
else
    title({'Comparison of Average System Frequency'; ['Case: ', LTDCaseName]})
end
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'F3'],'-pdf'); % to print fig
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
% % LTDdata =  mir.f;
% % pData = weightedF;
% % hold on
% % plot( t, abs(calcDeviation(t, mir, pData, LTDdata)*60 ))
%legend({'LTD 2 sec','LTD 1 sec','LTD 0.5 sec','LTD 0.25 sec'},'location','northeast')
xlim(x_lim)
grid on
if noCase ==1
    title('Comparison of Absolute Frequency Difference from PSDS')
else
    title({'Comparison of Absolute Frequency Difference from PSDS'; ['Case: ', LTDCaseName]})
end
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

