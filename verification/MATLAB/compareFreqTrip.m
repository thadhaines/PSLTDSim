function [  ] = compareFreqTrip( mir, psds_data, varargin )
%compareWfreq Compare LTD mirror and psds simulation data, ignores tripped  gens
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
makeLegend = 1;
x_lim = [mir.t(1), mir.t(end)];
bfz = 13; 
t = psds_data.Data(:,1); % PSDS time

% funtion specific 
ds = varargin{4};
genChange = varargin{5};

f_col = jfind(psds_data, 'fbu');

%% Calculate theoretical ss f
beta = 0;
for area = 1:max(size(mir.areaN))
    curArea = ['A',int2str(area)];
    beta = beta + mir.(curArea).beta;
end

sbase = mir.Sbase;
deltaP = genChange; % Generation change

deltaFpu = deltaP/sbase*(1/beta);
ssPu = 1 + deltaFpu;
ssF = ssPu*60;


%% Plot System frequency responses
figure('position',ppos)
axes('ColorOrder',flipud(imcomplement(colormap(spring(max(size(f_col))))))) % to make mess of lines look nicer
hold on

plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(1)),ds),'linewidth',1.5 )%,'HandleVisibility','off') % first frequency
for freq=2:max(size(f_col)-1)
    plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(freq)),ds) ,'HandleVisibility','off') % all others
end
plot(dsmple(t,ds), dsmple(psds_data.Data(:,f_col(size(f_col,2))), ds),'linewidth',1.5) % last Freq

plot(mir.t, mir.f*60 , 'w','linewidth',1.5,'HandleVisibility','off')
plot(mir.t, mir.f*60 , 'm-.','linewidth',2)
line([mir.t(1) mir.t(end)],[ssF,ssF],'linestyle',':','color',[.3 0 .7],'linewidth',1)

legend({'PSDS','PSDS','LTD','Theoretical SS'},'location','southeast')
xlim(x_lim)
grid on
if noCase ==1
    title('Comparison of System Frequency')
else
    title({'Comparison of System Frequency'; ['Case: ', LTDCaseName]})
end
ylabel('Frequency [Hz]')
xlabel('Time [sec]')
set(gca,'fontsize',bfz)

% pdf output code
if printFigs
    set(gcf,'color','w'); % to remove border of figure
    export_fig([LTDCaseName,'Freq'],'-pdf'); % to print fig
end

%% end of function
end

