function [hist]=AspectAnalysis(aspect)
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
direction(1)=sum(count(:));
count=(aspect>45-22.5).*(aspect<45+22.5);
direction(2)=sum(count(:));
count=(aspect>90-22.5).*(aspect<90+22.5);
direction(3)=sum(count(:));
count=(aspect>135-22.5).*(aspect<135+22.5);
direction(4)=sum(count(:));
count=(aspect>180-22.5).*(aspect<180+22.5);
direction(5)=sum(count(:));
count=(aspect>225-22.5).*(aspect<225+22.5);
direction(6)=sum(count(:));
count=(aspect>270-22.5).*(aspect<270+22.5);
direction(7)=sum(count(:));
count=(aspect>315-22.5).*(aspect<315+22.5);
direction(8)=sum(count(:));
direction(9)=numel(find(aspect==-1));
% percentage
%direction=direction/numel(aspect);
figure,
subplot(1,2,1),plot(1:8,direction(1:8)/numel(aspect));
axis([1,8,0,1]);
rose_data=[zeros(1,direction(1)),...
           45*ones(1,direction(2)),...
           90*ones(1,direction(3)),...
           135*ones(1,direction(4)),...
           180*ones(1,direction(5)),...
           225*ones(1,direction(6)),...
           270*ones(1,direction(7)),...
           315*ones(1,direction(8))];
rose_data=2*pi/360*rose_data;
subplot(1,2,2),rose(rose_data);
end