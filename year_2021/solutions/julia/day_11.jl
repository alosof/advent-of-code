include(joinpath(@__DIR__(), "utils", "files.jl"))


function count_flashes(grid::Matrix{Int}, steps::Int)::Int
    previous_grid = copy(grid)
    flashes = 0
    for _ in 1:steps
        step_flashes, grid_after_step = step(previous_grid)
        flashes += step_flashes
        previous_grid = grid_after_step
    end
    return flashes
end


function first_synchronized_flash(grid::Matrix{Int})::Int
    grid_area = length(grid)
    previous_grid = copy(grid)
    _step = 0
    while true
        _step += 1
        step_flashes, grid_after_step = step(previous_grid)
        if step_flashes == grid_area
            return _step
        end
        previous_grid = grid_after_step
    end
end


function step(grid::Matrix{Int})::Tuple{Int, Matrix{Int}}
    new_grid = copy(grid)
    flashed = Set{CartesianIndex}()
    new_grid = charge(grid)
    octopuses_to_flash = locate_octopuses_to_flash(new_grid, flashed)
    while length(octopuses_to_flash) > 0
        for octopus in octopuses_to_flash
            new_grid = propagate_around(octopus, new_grid)
        end
        flashed = union(flashed, octopuses_to_flash)
        octopuses_to_flash = locate_octopuses_to_flash(new_grid, flashed)
    end
    discharge!(new_grid)
    return length(flashed), new_grid
end


function locate_octopuses_to_flash(grid::Matrix{Int}, already_flashed::Set{CartesianIndex})::Set{CartesianIndex}
    octopuses_to_flash = Set()
    for idx in CartesianIndices(grid)
        if (grid[idx] > 9) & !(idx in already_flashed)
            push!(octopuses_to_flash, idx)
        end
    end
    return octopuses_to_flash
end


function propagate_around(octopus::CartesianIndex, grid::Matrix{Int})::Matrix{Int}
    new_grid = copy(grid)
    for neighbor in map(offset -> octopus + offset, CartesianIndices((-1:1, -1:1)))
        if (neighbor != octopus) & checkbounds(Bool, new_grid, neighbor)
            new_grid[neighbor] = new_grid[neighbor] + 1
        end
    end
    return new_grid
end


charge(grid::Matrix{Int})::Matrix{Int} = grid .+ 1

discharge!(grid::Matrix{Int}) = (grid[grid.>9] .= 0)


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    octopus_grid::Matrix{Int} = read_matrix(input_file_path)

    # Part 1
    part_1_result::Int = count_flashes(octopus_grid, 100)
    @assert part_1_result == 1721
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = first_synchronized_flash(octopus_grid)
    @assert part_2_result == 298
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
