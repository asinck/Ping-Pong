%This graphs a nice 3D graph. 
function status = grapher(size)
    t = 0:pi/10:2*pi;
    [x, y, z] = cylinder(size * cos(t));
    surf(x, y, z);
    hold on;
    status=0;
end

% About the status:
% 
% This has two purposes. First of all, it demonstrates getting a value
% back from the matlab program. Second, the programs didn't want to work
% together unless I made the matlab side return something. I don't have
% to do anything with it on the python side.
