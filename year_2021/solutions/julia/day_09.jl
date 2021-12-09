include(joinpath(@__DIR__(), "utils", "files.jl"))


compute_product_of_three_largest_basins_sizes(heightmap::Matrix{Int})::Int = prod(sort([get_basin_size_around_point(p, heightmap, Set()) for p in find_low_points(heightmap)])[end-2:end])


function get_basin_size_around_point(point::CartesianIndex, heightmap::Matrix{Int}, visited)::Int
    if (point in visited) | (heightmap[point] == 9)
        return 0
    else
        push!(visited, point)
        return 1 + sum(get_basin_size_around_point(n, heightmap, visited) for n in get_neighbors(point, heightmap))
    end
end


compute_low_points_risk(heightmap::Matrix{Int})::Int = sum(map(p -> heightmap[p] + 1, find_low_points(heightmap)))

find_low_points(heightmap::Matrix{Int}) = filter(p -> is_low_point(p, heightmap), CartesianIndices(heightmap))

is_low_point(point::CartesianIndex, heightmap::Matrix{Int})::Bool = all(heightmap[point] .< [heightmap[neighbor] for neighbor in get_neighbors(point, heightmap)])


function get_neighbors(point::CartesianIndex, heightmap::Matrix{Int})::Set{CartesianIndex}
    neighbors = Set()
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for offset in offsets
        neighbor = point + CartesianIndex(offset)
        if checkbounds(Bool, heightmap, neighbor)
            push!(neighbors, neighbor)
        end
    end
    return neighbors
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    heightmap::Matrix{Int} = read_matrix(input_file_path)

    # Part 1
    part_1_result::Int = compute_low_points_risk(heightmap)
    @assert part_1_result == 508
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = compute_product_of_three_largest_basins_sizes(heightmap)
    @assert part_2_result == 1564640
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
