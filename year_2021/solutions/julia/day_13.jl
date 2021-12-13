include(joinpath(@__DIR__(), "utils", "files.jl"))


function number_of_dots_after_one_fold(dots::Vector{Tuple{Int, Int}}, folds::Vector{Tuple{String, Int}})::Int
    dots_after_one_fold, _ = fold(dots, [folds[1]])
    return length(dots_after_one_fold)
end


function fold(dots::Vector{Tuple{Int, Int}}, folds::Vector{Tuple{String, Int}})::Tuple{Vector{Tuple{Int, Int}}, Tuple{Int, Int}}
    new_dots = dots
    new_shape = get_shape(dots)
    for _fold in folds
        axis, position = _fold
        if axis == "x"
            new_dots = vertical_fold(new_dots, position)
            new_shape = (new_shape[1], position)
        elseif axis == "y"
            new_dots = horizontal_fold(new_dots, position)
            new_shape = (position, new_shape[2])
        end
    end
    return new_dots, new_shape
end


function vertical_fold(dots::Vector{Tuple{Int, Int}}, x::Int)::Vector{Tuple{Int, Int}}
    new_dots = []
    for dot in dots
        if dot[1] < x
            push!(new_dots, dot)
        elseif dot[1] > x
            push!(new_dots, (2 * x - dot[1], dot[2]))
        end
    end
    return collect(Set(new_dots))
end


function horizontal_fold(dots::Vector{Tuple{Int, Int}}, y::Int)::Vector{Tuple{Int, Int}}
    new_dots = []
    for dot in dots
        if dot[2] < y
            push!(new_dots, dot)
        elseif dot[2] > y
            push!(new_dots, (dot[1], 2 * y - dot[2]))
        end
    end
    return collect(Set(new_dots))
end


get_shape(dots)::Tuple{Int, Int} = maximum([d[1] for d in dots]) + 1, maximum([d[2] for d in dots]) + 1


function to_grid(dots::Vector{Tuple{Int, Int}}, shape::Tuple{Int, Int})::Vector{Vector{String}}
    grid = [["." for _ in 1:shape[2]] for _ in 1:shape[1]]
    for dot in dots
        grid[dot[2] + 1][dot[1] + 1] = "#"
    end
    return grid
end


render(grid::Vector{Vector{String}})::String = join([join(row, " ") for row in grid], "\n")


function read_folding_instructions(input_path::String)::Tuple{Vector{Tuple{Int, Int}}, Vector{Tuple{String, Int}}}
    lines = readlines(input_path)
    separator = findfirst(==(""), lines)
    dots = []
    folds = []
    for line in lines[begin:(separator - 1)]
        dot = split(line, ",")
        push!(dots, Tuple(parse.(Int, dot)))
    end
    for line in lines[(separator + 1):end]
        axis, position = split(split(line, "fold along ")[end], "=")
        push!(folds, (axis, parse(Int, position)))
    end
    return dots, folds
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    result_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "result.txt")
    input_dots, input_folds = read_folding_instructions(input_file_path)

    # Part 1
    part_1_result::Int = number_of_dots_after_one_fold(input_dots, input_folds)
    @assert part_1_result == 770
    println("Part 1 result : ", part_1_result)

    # Part 2
    dots_after_folding, shape_after_folding = fold(input_dots, input_folds)
    rendered_grid_after_folding = render(to_grid(dots_after_folding, shape_after_folding))
    rendered_expected_grid::String = open(f->read(f, String), result_file_path)
    @assert rendered_expected_grid == rendered_grid_after_folding
    println("Part 2 result :")
    println(rendered_grid_after_folding)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
