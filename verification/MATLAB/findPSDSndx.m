function [ dataNDX ] = findPSDSndx(psds_data, busNum, busNam, tarId, dType )
%findPSDSndx returns index of psds data
%   Uses jfind and specific data identifiers to search through psds data
%   index.

%% Use data to find easy intersections
typeCols = jfind(psds_data, dType);
nameCols = jfind(psds_data, busNam);
numCols = jfind(psds_data, int2str(busNum));

firstInt = intersect(typeCols,nameCols);
firstInt = intersect(firstInt, numCols);

%% Parse description and match bus num and id (if required)
if max(size(firstInt))>1
    for ndx=1:max(size(firstInt))
        desc = strjoin(psds_data.Description(firstInt(ndx)));
        %disp(desc)
        dSplit = strsplit(desc,':');
        bus = str2double(dSplit(1));
        id = str2double(dSplit(7));
        
        if bus == busNum
            if id == tarId
                secInt = firstInt(ndx);
                break
            end
        end
    end
    
    dataNDX = secInt;
    
elseif max(size(firstInt))==1
    dataNDX = firstInt;
else
    disp('Index Not Found')
    dataNDX = -1;
end
end

