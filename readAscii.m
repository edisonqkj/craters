function [dataset,head,img]=readAscii(path)
% Read Ascii file of Raster
% Return without any process on Nodata value, just keep it in matrix.
clc;
% path='F:\Êý¾Ý\moon\moon.txt';
fid = fopen(path, 'r');
%% read head attributes in first partition
% ncols         1452
% nrows         1378
% xllcorner     5689950.6739785
% yllcorner     3307559.3275701
% cellsize      499.542418
% NODATA_value  -9999
head=zeros(1,6);
for i=1:6
    [line,line_count]=fscanf(fid,'%13c %f\r\n',[1 2]);
    head(i)=line(14);
end
% disp(head);
%% read dataset in second partition
col=head(1);
format='%f';
for i=2:col
    format=[format ' %f'];
end
[dataset,dataset_count]=fscanf(fid,format,[col inf]);
fclose(fid);
dataset=dataset';
% dataset(dataset==head(6))=0;
% disp(dataset_count);
%% convert to 0-255
img=dataset;
pos_withvalue=(img~=head(6));
pos_nodata=(img==head(6));

min_v=min(img(pos_withvalue));
max_v=max(img(pos_withvalue));
if(sum(pos_nodata)==0)
    %  0-255
    img(pos_withvalue)=(img(pos_withvalue)-min_v).*(255-0)+0;
    img(pos_withvalue)=img(pos_withvalue)./(max_v-min_v);
else
    % 1-255
    img(pos_withvalue)=(img(pos_withvalue)-min_v).*(255-1)+1;
    img(pos_withvalue)=img(pos_withvalue)./(max_v-min_v);
    img(pos_nodata)=0;
end
img=uint8(img);
end