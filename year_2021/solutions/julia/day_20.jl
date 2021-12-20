include(joinpath(@__DIR__(), "utils", "files.jl"))


function enhance(image::Matrix{Char}, algorithm::Vector{Char}, times::Int)::Matrix{Char}
    res = image
    for i in 1:times
        if (algorithm[1] == '#') & (algorithm[end] == '.')
            padding_char = isodd(i) ? '.' : '#'
        else
            padding_char = '.'
        end
        res = enhance(res, algorithm, padding_char)
    end
    return res
end


function enhance(image::Matrix{Char}, algorithm::Vector{Char}, padding_char::Char)::Matrix{Char}
    n_pads = 3
    padded_image = pad(image, padding_char, n_pads)
    res = fill('.', size(padded_image) .- 2)
    for idx in CartesianIndices(res)
        res[idx] = algorithm[1 + surrounding_pixels(idx, padded_image, 1)]
    end
    return res
end


function surrounding_pixels(position::CartesianIndex, padded_image::Matrix{Char}, n_pads::Int)::Int
    position_after_padding = position + CartesianIndex(n_pads, n_pads)
    filter_area = padded_image[CartesianIndices((-1:1, -1:1)) .+ position_after_padding]
    binary = join(map(c -> c == '.' ? "0" : "1", vcat(transpose(filter_area)...)))
    return parse(Int, binary, base=2)
end


function pad(matrix::Matrix{Char}, char::Char, n::Int)::Matrix{Char}
    res = matrix
    for _ in 1:n
        res = pad(res, char)
    end
    return res
end


function pad(matrix::Matrix{Char}, char::Char)::Matrix{Char}
    padded = fill(char, size(matrix) .+ 2)
    padded[2:(end - 1), 2:(end - 1)] = matrix
    return padded
end


function read_algorithm_and_image(input_file_path::String)::Tuple{Vector{Char}, Matrix{Char}}
    blocks = split(read(open(input_file_path), String), "\n\n")
    algorithm = collect(blocks[1])
    image = vecofvec_to_matrix(collect.(split(blocks[2], "\n")))
    return algorithm, image
end


function transpose(matrix::Matrix{Char})::Matrix{Char}
    transposed = fill('.', size(matrix))
    for idx in CartesianIndices(transposed)
        transposed[idx] = matrix[idx[2], idx[1]]
    end
    return transposed
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    algorithm, image = read_algorithm_and_image(input_file_path)

    # Part 1
    part_1_result::Int = count(==('#'), enhance(image, algorithm, 2))
    @assert part_1_result == 5291
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = count(==('#'), enhance(image, algorithm, 50))
    @assert part_2_result == 16665
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
