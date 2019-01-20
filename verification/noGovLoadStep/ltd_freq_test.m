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

pslf_data = udread('ee554.1.chf',[]);
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

%% plot generator frequency
figure
subplot 211
plot(t,pslf_data.Data(:,f_col(1))/60,'k','linewidth',1,'color',[.7, .7, .7])
hold on

plot(noGov.t,noGov.f,':o','linewidth',1.5,'color',[99 0 5]./100)
plot(noGovAB.t,noGovAB.f,':o','linewidth',1.5,'color',[8.6 91.8 0]./100)
plot(noGovEw.t,noGovEw.f,'k:+','linewidth',1.5)
plot(noGovABHw.t,noGovABHw.f,':+','linewidth',1.5,'color',[56.5, 0.4, 84.1]./100)

title_str = 'System Frequency';
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

%% relative frequency
% index of t == 0 in PSLF data
zoft = 3;
ts = t(zoft+1); % first time step from zero
fs = round(1/ts);

f = pslf_data.Data(:,f_col(2))/60; % per unit freq

for ct=0:20
    % find index of time at full second
    n = zoft + fs*ct;
    % pull values
    pulledtime(ct+1) = t(n);
    pulledf(ct+1) = f(n);
    
    ct= ct+1;
end

% calculate relative freq
rFEw = noGovEw.f-pulledf;
rFE = noGov.f - pulledf;
rFAB = noGovAB.f-pulledf;
rFABw = noGovABHw.f -pulledf;

%% make plot
subplot 212
plot(pulledtime,rFE*100,':o','Linewidth',2,'color',[99 0 5]./100)
hold on
plot(pulledtime,rFAB*100,':o','Linewidth',2,'color',[8.6 91.8 0]./100)
plot(pulledtime,rFEw*100,'k:+','Linewidth',2)
plot(pulledtime,rFABw*100,':+','Linewidth',2,'color',[56.5, 0.4, 84.1]./100)
grid on
xlim([0,16])
xlabel('Time [sec]')
ylabel('Relative Frequency [% pu]')
title('Relative Frequency, PSLF v LTD')
legend({'Euler','A.B.','Euler w Freq Fx','A.B. w Freq Fx'},'location','best')
set(gca,'FontSize',15)
set(gcf,'Position',p_pos)

%% export pdf code
%   set(gcf,'color','w'); % to remove border of figure
%   export_fig('noGov_LTD03','-pdf'); 