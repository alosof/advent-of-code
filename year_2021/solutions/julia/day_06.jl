include(joinpath(@__DIR__(), "utils", "files.jl"))


function count_fish_after_n_days(initial_fish_population::Array{Int}, n::Int)::Int
    population_by_timer = Dict{Int, Int}([(timer, count(==(timer), initial_fish_population)) for timer in 0:8])
    for _ in 1:n
        new_population = Dict{Int, Int}()
        for timer in 0:8
            if timer == 8
                new_population[timer] = population_by_timer[0]
            elseif timer == 6
                new_population[timer] = population_by_timer[0] + population_by_timer[7]
            else
                new_population[timer] = population_by_timer[timer + 1]
            end
        end
        population_by_timer = new_population
    end
    return sum(values(population_by_timer))
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    fish_population::Array{Int} = parse.(Int, split(read(open(input_file_path), String), ","))

    # Part 1
    part_1_result::Int = count_fish_after_n_days(fish_population, 80)
    @assert part_1_result == 391671
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = count_fish_after_n_days(fish_population, 256)
    @assert part_2_result == 1754000560399
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
