function [ devData ] = calcDeviation( t, mir, psdsData, LTDdata )
% calcDeviation Create data for deviation comparison
%   % inputs: psdsT, mirror, psdsData, LTDdata
%
 
    LTDtNdx = 1;
    devData = zeros(size(psdsData));
    for pNdx=1:size(psdsData,1)
        if t(pNdx)> mir.t(LTDtNdx)
            % Adjust LTD index as required
            LTDtNdx = LTDtNdx+1;
            if LTDtNdx > max(size(LTDdata))
                % avoid over adjusting
                LTDtNdx = max(size(LTDdata));
            end
        end
        devData(pNdx) = psdsData(pNdx)-LTDdata(LTDtNdx);
    end

end

