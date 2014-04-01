function []=scalewin(aspect)
clc;
[row,col]=size(aspect)
if row>col
    num_scale=[1:2:fix(col/2)-1];
else
    num_scale=[1:2:fix(row/2)-1];
end
for i=1:length(num_scale)
    data=aspect(fix(row/2)-num_scale(i):fix(row/2)+num_scale(i),...
                fix(col/2)-num_scale(i):fix(col/2)+num_scale(i));
    [hist,ma(i),mr(i)]=AspectAnalysis(data,i);
end
figure,
subplot(2,1,1),plot(num_scale,ma);
title('mean aspect');
subplot(2,1,2),plot(num_scale,mr);
axis([1,max(num_scale),0,1]);
title('mean R');
end