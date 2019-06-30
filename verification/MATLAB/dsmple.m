function [ ds ] = dsmple( data, step )
%dsmple Return 'downsampled' data. 
%   steps through data every x step, ensures same starting and ending value.

    ds = data(1:step:end);
    if ds(end) ~= data(end)
        ds = [ds, data(end)];
    end

end

