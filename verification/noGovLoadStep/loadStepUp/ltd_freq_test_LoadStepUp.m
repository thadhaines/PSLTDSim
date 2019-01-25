%%  ltd_freq_test.m
%   Thad Haines         Research
%   Program Purpose:    Import data from PSLF and LTD .mat
%                       Make plots 
%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   01/20/19    08:53   init

%% init
clear; format compact; clc; close all; 

p_pos = [541 100 1366 651]; % plot position and size
%% import pslf data
pslf_data = udread('ee554.exc.1.chf',[]);
cellfun(@disp,pslf_data.Name)

spd_col = jfind(pslf_data, 'spd');
v_col = jfind(pslf_data, 'v');
pg_col = jfind(pslf_data, 'pg');
qg_col = jfind(pslf_data, 'qg');
f_col = jfind(pslf_data, 'fbu');

t = pslf_data.Data(:,1);

%% import LTD data
load('noGov.mat') % euler f integration
load('noGovAB.mat') % adams bashforth integration
load('noGovABHres.mat') % adams bashforth integration, 0.25 timestep
load('noGovABHw.mat') % accounts for freq in swing equation
load('noGovEw.mat') % accounts for freq in swing equation

%% system mean frequency and relative frequency calculations

% sum all frequency data
meanf = pslf_data.Data(:,f_col(1))/60;% per unit freq
for freq=2:size(f_col,2)
    meanf = meanf + pslf_data.Data(:,f_col(freq))/60;
end
% find average
meanf = meanf./size(f_col,2); 

% find index of t == 0 in PSLF data
n = 1;
while t(n) ~= 0
	n = n+1;
end
zoft = n; % location of 0 in PSLF data
% first time step from zero used for indexing
ts = t(zoft+1); 
fs = round(1/ts);

% Collect PSLF data corresponding to LTD data
for ct=0:20
    % find index of time at full second
    n = zoft + fs*ct;
    % pull values
    pulledtime(ct+1) = t(n);
    pulledf(ct+1) = meanf(n); % system 'mean'
end

% calculate relative freq
rFEw = noGovEw.f-pulledf;
rFE = noGov.f - pulledf;
rFAB = noGovAB.f-pulledf;
rFABw = noGovABHw.f -pulledf;

%%
pltColor.grey = [.7, .7, .7];
pltColor.magenta = [1 0 1];
pltColor.green = [8.6 91.8 0]./100;
pltColor.Lblue = [0 .5 1];

%% plot generator frequency
figure
subplot 211
hold on
plot(pulledtime, pulledf,'k','linewidth',3,'color',pltColor.grey)
plot(noGov.t,noGov.f,':o','linewidth',1.5,'color',pltColor.magenta)
plot(noGovAB.t,noGovAB.f,':o','linewidth',1.5,'color',pltColor.green)
plot(noGovEw.t,noGovEw.f,'k:+','linewidth',1.5)
plot(noGovABHw.t,noGovABHw.f,':+','linewidth',1.5,'color',pltColor.Lblue)

title_str = 'Mean System Frequency';
y_label = 'Frequency [pu]';
grid on
legend({'PSLF', 'LTD Euler','LTD AB','LTD Euler w Freq','LTD AB w Freq'}, ...
    'location','best') % Legend
set(gcf,'Position',p_pos)
title(title_str)
ylabel(y_label)
xlabel('Time [sec]')
xlim([0 20])

set(gca,'FontSize',15)

%% make relative frequency plot
subplot 212
plot(pulledtime,rFE*100,':o','Linewidth',2,'color',pltColor.magenta)
hold on
plot(pulledtime,rFAB*100,':o','Linewidth',2,'color',pltColor.green)
plot(pulledtime,rFEw*100,'k:+','Linewidth',2)
plot(pulledtime,rFABw*100,':+','Linewidth',2,'color',pltColor.Lblue)
grid on
%xlim([0,16])
xlabel('Time [sec]')
ylabel('Relative Frequency [% pu]')
title('Relative Frequency, PSLF v LTD')
legend({'Euler','A.B.','Euler w Freq Fx','A.B. w Freq Fx'},'location','best')
set(gca,'FontSize',15)
set(gcf,'Position',p_pos)

%% export pdf code
%   set(gcf,'color','w'); % to remove border of figure
%   export_fig('noGovExc01freq','-pdf'); 