include(joinpath(@__DIR__(), "utils", "files.jl"))


multiply_tree_counts_for_several_slopes(area_map::Array{String}, slopes::Array{Tuple{Int,Int}})::Int = prod(count_trees(area_map, slope_right, slope_down) for (slope_right, slope_down) in (slopes))

function count_trees(area_map::Array{String}, slope_right::Integer, slope_down::Integer)::Integer
    map_bottom_row = length(area_map)
    map_rightmost_column = length(area_map[begin])
    row, column, tree_count = 1, 1, 0
    while row <= map_bottom_row
        if area_map[row][column] == '#'
            tree_count += 1
        end
        row += slope_down
        column = column + slope_right
        if column > map_rightmost_column
            column -= map_rightmost_column
        end
    end
    return tree_count
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, "day_03", "input.txt")
    input_list::Array{String} = readlines(input_file_path)
    
    # Part 1
    part_1_result::Int = multiply_tree_counts_for_several_slopes(input_list, [(3, 1)])
    @assert part_1_result == 211
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = multiply_tree_counts_for_several_slopes(input_list, [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
    @assert part_2_result == 3584591857
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
