global d

function [n, m] = do_something()
    n = 10
    m = 45
    if n | m;
        d = [1 2 3; 4 5 6]
    elseif n & m;
        return
    elseif n - m > 0;
        n = n - m
    end
end
