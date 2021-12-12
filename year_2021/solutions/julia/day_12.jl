include(joinpath(@__DIR__(), "utils", "files.jl"))


function paths_with_one_small_cave_visited_at_most_twice(cave_system::Dict{String, Vector{String}}, current_cave::String, path::Vector{String})::Int
    if !(current_cave in keys(cave_system)) || (cave_system[current_cave] == [])
        return 0
    elseif current_cave == "end"
        return 1
    else
        path = vcat(path, [current_cave])
        updated_cave_system = cave_system
        if is_endpoint(current_cave) || is_small(current_cave) && at_least_one_small_cave_visited_twice(path)
            updated_cave_system = remove_cave(current_cave, updated_cave_system)
        end
        if at_least_one_small_cave_visited_twice(path)
            visited_small_caves = Set(keys(count_small_caves_visits(path)))
            visited_small_caves_still_in_cave_system = intersect(visited_small_caves, keys(updated_cave_system))
            for cave in visited_small_caves_still_in_cave_system
                updated_cave_system = remove_cave(cave, updated_cave_system)
            end
        end
        return sum([paths_with_one_small_cave_visited_at_most_twice(updated_cave_system, next_cave, path) for next_cave in cave_system[current_cave]])
    end
end


function paths_with_small_caves_visited_at_most_once(cave_system::Dict{String, Vector{String}}, current_cave::String)::Int
    if current_cave == "end"
        return 1
    else
        if is_endpoint(current_cave) || is_small(current_cave)
            updated_cave_system = remove_cave(current_cave, cave_system)
        else
            updated_cave_system = cave_system
        end
        return sum([paths_with_small_caves_visited_at_most_once(updated_cave_system, next_cave) for next_cave in cave_system[current_cave]])
    end
end


at_least_one_small_cave_visited_twice(path::Array{String})::Bool = any(cave_visits > 1 for cave_visits in values(count_small_caves_visits(path)))

count_small_caves_visits(path::Array{String})::Dict{String, Int} = Dict((cave, count(==(cave), path)) for cave in path if is_small(cave))

remove_cave(cave::String, cave_system::Dict{String, Vector{String}})::Dict{String, Vector{String}} = Dict(
    [(k, [e for e in v if e != cave]) for (k, v) in cave_system if k != cave]
)

is_small(cave::String)::Bool = (lowercase(cave) == cave) & !is_endpoint(cave)

is_endpoint(cave::String)::Bool = (cave in ["start", "end"])


function build_cave_system(input_lines::Vector{String})::Dict{String, Vector{String}}
    cave_system = Dict{String, Vector{String}}()
    for path in input_lines
        cave_1, cave_2 = split(path, "-")
        cave_system[cave_1] = vcat(get(cave_system, cave_1, []), [cave_2])
        cave_system[cave_2] = vcat(get(cave_system, cave_2, []), [cave_1])
    end
    return cave_system
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    cave_system::Dict{String, Vector{String}} = build_cave_system(readlines(input_file_path))

    # Part 1
    part_1_result::Int = paths_with_small_caves_visited_at_most_once(cave_system, "start")
    @assert part_1_result == 3450
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = paths_with_one_small_cave_visited_at_most_twice(cave_system, "start", Vector{String}([]))
    @assert part_2_result == 96528
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
