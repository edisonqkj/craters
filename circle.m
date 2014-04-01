function [circle_mask]=circle(r)
[x, y] = meshgrid(-r:r);
circle_mask = sqrt(x.^2 + y.^2);
% figure,imshow(circle_mask<=r);
% title('Circle Mask');
circle_mask(circle_mask<=r)=1;
circle_mask(circle_mask>r)=0;
% circle_mask=[circle_mask(1:r,:);circle_mask(r+2:end,:)];
end