function [ pDiffData ] = calcPdiff( t, mir, psdsData, LTDdata )
% calcDeviation Create data for deviation comparison
%   % inputs: psdsT, mirror, psdsData, LTDdata
%

LTDtNdx = 1;
pDiffData = zeros(size(psdsData));
for pNdx=1:max(max(size(psdsData)))
    
    nextNdx = LTDtNdx+1;
    if nextNdx > max(max(size(LTDdata)))
        % avoid over adjusting
        nextNdx = max(max(size(LTDdata)));
    end
    
    
    if t(pNdx) >= mir.t(nextNdx)
        % Adjust LTD index as required
        LTDtNdx = nextNdx;
    end
    
    
    pDiffData(pNdx) = abs(psdsData(pNdx)-LTDdata(LTDtNdx))/((psdsData(pNdx)+LTDdata(LTDtNdx))/2)*100;
end

end

