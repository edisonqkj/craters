function writeAscii(dem,head,path)
[row,col]=size(dem);
fid=fopen(path,'w');
% ncols         1452
% nrows         1378
% xllcorner     5689950.6739785
% yllcorner     3307559.3275701
% cellsize      499.542418
% NODATA_value  -9999
fprintf(fid,'ncols         %f\r\n',int32(head(1)));
fprintf(fid,'nrows         %f\r\n',int32(head(2)));
fprintf(fid,'xllcorner     %f\r\n',head(3));
fprintf(fid,'yllcorner     %f\r\n',head(4));
fprintf(fid,'cellsize      %f\r\n',head(5));
fprintf(fid,'NODATA_value  %f\r\n',int32(head(6)));
fclose(fid);

dlmwrite(path, dem, 'delimiter', ' ','-append','newline','pc');
end