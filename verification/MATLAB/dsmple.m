function [ ds ] = dsmple( data, step )
%dsmple Return 'downsampled' data. 
%   steps through data every x step, ensures same starting and ending value.

    % for optional non-downsample
    if step ==0
        ds = data;
        return
    end
    
    ds = data(1:step:end-1);
    
    % required in case of vector or row vector
    if size(ds,1)>size(ds,2)
        ds = [ds; data(end)];
    else
        ds = [ds, data(end)];
    end
    

end

