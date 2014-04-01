function [hist,mean_aspect,mean_R]=AspectAnalysis(aspect,id)
% make circle mask
[row,col]=size(aspect);
if row<=col
    r=fix(row/2);
    [mask]=circle(r);
    if mod(row,2)==0
        mask=[mask(1:r,:);mask(r+2:end,:)];
    end
    mask=[zeros(row,fix((col-row)/2)),...
          mask,...
          zeros(row,col-fix((col-row)/2)-size(mask,2))];
else
    r=fix(col/2);
    [mask]=circle(r);
    if mod(col,2)==0
        mask=[mask(:,1:r);mask(:,r+2:end)];
    end
    mask=[zeros(fix((row-col)/2),col);...
          mask;...
          zeros(row-fix((row-col)/2)-size(mask,1),col)];
end
% figure,imshow(mask);
aspect=aspect.*mask;
aspect(find(mask==0))=-1;
% figure,imshow(aspect,[]);
%%
% histogram of each direction
% north       [0-22.5,0+22.5]
% northeast	  [45-22.5,45+22.5]
% east        [90-22.5,90+22.5]
% southeast	  [135-22.5,135+22.5]
% south       [180-22.5,180+22.5]
% southwest	  [225-22.5,225+22.5]
% west        [270-22.5,270+22.5]
% northwest	  [315-22.5,315+22.5]
% undefine    [-1]
count=(aspect>=0).*(aspect<22.5)+(aspect>360-22.5);
direction(1)=0;
hist(1)=sum(count(:));
count=(aspect>45-22.5).*(aspect<45+22.5);
direction(2)=45;
hist(2)=sum(count(:));
count=(aspect>90-22.5).*(aspect<90+22.5);
direction(3)=90;
hist(3)=sum(count(:));
count=(aspect>135-22.5).*(aspect<135+22.5);
direction(4)=135;
hist(4)=sum(count(:));
count=(aspect>180-22.5).*(aspect<180+22.5);
direction(5)=180;
hist(5)=sum(count(:));
count=(aspect>225-22.5).*(aspect<225+22.5);
direction(6)=225;
hist(6)=sum(count(:));
count=(aspect>270-22.5).*(aspect<270+22.5);
direction(7)=270;
hist(7)=sum(count(:));
count=(aspect>315-22.5).*(aspect<315+22.5);
direction(8)=315;
hist(8)=sum(count(:));
direction(9)=-1;
hist(9)=numel(find(aspect==-1));
%%
% convert aspect domain into the polar coordinate
aspect_polar=aspect(aspect~=-1);
% aspect_polar(aspect_polar>180)=aspect_polar(aspect_polar>180)-360;
% aspect_polar(aspect_polar~=-1)=90-aspect_polar(aspect_polar~=-1);
cos_theta=cos(aspect_polar*pi/180);
sin_theta=sin(aspect_polar*pi/180);
res_x=sum(cos_theta(:));
res_y=sum(sin_theta(:));
mean_aspect=atan(res_y/res_x)*180/pi;
if res_x>0 && res_y<0
    mean_aspect=360+mean_aspect;
elseif res_x<0 && res_y>0
    mean_aspect=180+mean_aspect;
elseif res_x<0 && res_y<0
    mean_aspect=180+mean_aspect;
end
mean_R=sqrt(res_x.^2+res_y.^2)/numel(sin_theta);
%%
% figure('Name',['ID= ' num2str(id)]),
% subplot(1,2,1),plot(direction(1:8),hist(1:8)/numel(aspect_polar));
% axis([0,315,0,1]);
% rose_data=[zeros(1,hist(1)),...
%            45*ones(1,hist(2)),...
%            90*ones(1,hist(3)),...
%            135*ones(1,hist(4)),...
%            180*ones(1,hist(5)),...
%            225*ones(1,hist(6)),...
%            270*ones(1,hist(7)),...
%            315*ones(1,hist(8))];
% rose_data=2*pi/360*rose_data;
% subplot(1,2,2),rose(rose_data);
% title(['mean_a= ' num2str(mean_aspect) ' mean_R= ' num2str(mean_R)]);
end