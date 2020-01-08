% MATLAB of delay block

clear; close all; clc

Td = 30;
Ta = 1;
approxN = 15;

s = tf('s')
num = exp(-Td*s)
den = (1+s*Ta)
G = num/den

%% pade testing...
[pNum, pDen] = pade(Td,approxN)
testDelay = tf(pNum, pDen)/den
step(testDelay)
hold on
step(G)

% Result: don't use Pade unless totally required or in freq domain
