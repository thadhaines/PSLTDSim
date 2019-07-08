function [ devData ] = calcDeviation( t, mir, psdsData, LTDdata )
% calcDeviation Create data for deviation comparison
%   % inputs: psdsT, mirror, psdsData, LTDdata
%

LTDtNdx = 1;
devData = zeros(size(psdsData));
for pNdx=1:size(psdsData,1)
    
    nextNdx = LTDtNdx+1;
    if nextNdx > max(size(LTDdata))
        % avoid over adjusting
        nextNdx = max(size(LTDdata));
    end
    
    
    if t(pNdx) >= mir.t(nextNdx)
        % Adjust LTD index as required
        LTDtNdx = nextNdx;
    end
    
    
    devData(pNdx) = psdsData(pNdx)-LTDdata(LTDtNdx);
end

end

