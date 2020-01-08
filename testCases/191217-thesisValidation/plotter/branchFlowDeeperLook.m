%% init
clear; format compact; clc; close all;
format long;

PSDSfileName = 'sixMachineRamp1.chf'; % 75 MW
%LTDCaseName = 'SixMachineRamp1rev';
LTDCaseName = 'SixMachineRamp1';
genChange = 0;

%% import LTD data in an automatic way
cases = {[LTDCaseName,'F']};
load(cases{1}) % 2 sec
mir = eval(cases{1});
clear eval(cases{1})

%% import PSDS data
psds_data = udread(PSDSfileName,[]);
%cellfun(@disp,psds_data.Name) % display all data types collected from psds


%% LTD Calcs
Vs =  mir.A2.x10.Vm(1)
ds = mir.A2.x10.Va(1)
Vr = mir.A2.L9.Vm(1)
dr = mir.A2.L9.Va(1)

X = 0.001
R = 0.0001
Vbase = 138e3
Sbase = 100E6
zBase = Vbase^2/Sbase

%% power flow
disp('*** Real Power')
PcalcOld = Vr*Vs*Vbase^2*sin(ds-dr)/(X*Vbase^2/Sbase)/1E6 % MW
P_LTD =  mir.branch.br10.Pbr(1)
P_PSDS = psds_data.Data(1,81) % col 81 is pbr for branch 10->9
Pdif = P_PSDS-P_LTD


%% q flow
disp('*** Reactive Power')
QcalcOld = Vr*Vbase/(X*zBase)*(Vs*Vbase*cos(ds-dr)-Vr*Vbase)/1E6 % MW
Q_LTD =  mir.branch.br10.Qbr(1)
Q_PSDS = psds_data.Data(1,82) % col 82 is qbr for branch 10->9
Qdif = Q_PSDS-Q_LTD

%% Amp flow
disp('*** Current Flow')
IcalcOld = abs(PcalcOld+1j*QcalcOld)/(Vr*Vbase*sqrt(3))*1E6
I_LTD =  mir.branch.br10.Amps(1)
I_PSDS = psds_data.Data(1,85) % col 83 is ibr for branch 10->9
I_dif = I_PSDS-I_LTD
%% losses
disp('*** Losses')
Ploss = I_PSDS^2*(R*zBase)
Ploss = I_PSDS^2*(X*zBase)
%% Power flow calcs
disp('*** Real Power using I')
Is = (Vs*Vbase*exp(1j*ds)-Vr*Vbase*exp(1j*dr))/((R+1j*X)*zBase)/sqrt(3) % seems to be very close to PSDS

Idif = I_PSDS-abs(Is)

Pvs = Vs*Vbase*abs(Is)*cos(ds-angle(Is))*sqrt(3)/1E6
dif = P_PSDS - Pvs

Qvs = Vs*Vbase*abs(Is)*sin(ds-angle(Is))*sqrt(3)/1E6
dif = Q_PSDS - Qvs


% %% Using other current
% disp('*** Real Power using I - alt end - not related to PSDS')
% Ir = (Vr*Vbase*exp(1j*dr)-Vs*Vbase*exp(1j*ds))/((R+1j*X)*zBase)/sqrt(3) % seems to be very close to PSDS
% 
% Idif = I_PSDS-abs(Ir)
% 
% 
% Pvr = Vr*Vbase*abs(Ir)*cos(dr-angle(Ir))*sqrt(3)/1E6
% dif = P_PSDS - Pvr
% 
% Qvr = Vr*Vbase*abs(Ir)*sin(dr-angle(Ir))*sqrt(3)/1E6
% dif = Q_PSDS - Qvr
