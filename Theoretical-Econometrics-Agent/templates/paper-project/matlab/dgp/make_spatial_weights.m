function W = make_spatial_weights(N, design)
%MAKE_SPATIAL_WEIGHTS Create row-normalized spatial weights.
%   design = 'ring' or 'block'. Extend as needed for kNN designs.

if nargin < 2
    design = 'ring';
end

W = zeros(N, N);

switch lower(design)
    case 'ring'
        for i = 1:N
            left = mod(i - 2, N) + 1;
            right = mod(i, N) + 1;
            W(i, left) = 1;
            W(i, right) = 1;
        end
    case 'block'
        block_size = max(5, round(sqrt(N)));
        for i = 1:N
            block_id = ceil(i / block_size);
            lo = (block_id - 1) * block_size + 1;
            hi = min(block_id * block_size, N);
            neighbors = setdiff(lo:hi, i);
            W(i, neighbors) = 1;
        end
    otherwise
        error('Unknown spatial weight design: %s', design);
end

row_sums = sum(W, 2);
row_sums(row_sums == 0) = 1;
W = W ./ row_sums;
end

