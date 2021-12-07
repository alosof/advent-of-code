include(joinpath(@__DIR__(), "utils", "files.jl"))


fuel_to_reach_optimal_position(crab_positions::Array{Int}, fuel_consumption::Function)::Int = minimum(
    sum(fuel_consumption(ref_crab, crab) for crab in crab_positions) 
    for ref_crab in crab_positions
)

linear_fuel_consumption(ref_crab::Int, crab::Int)::Int = abs(crab - ref_crab)

quadratic_fuel_consumption(ref_crab::Int, crab::Int)::Int = abs(crab - ref_crab) * (abs(crab - ref_crab) + 1) / 2


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    crab_positions::Array{Int} = parse.(Int, split(read(open(input_file_path), String), ","))
    
    # Part 1
    part_1_result::Int = fuel_to_reach_optimal_position(crab_positions, linear_fuel_consumption)
    @assert part_1_result == 344138
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = fuel_to_reach_optimal_position(crab_positions, quadratic_fuel_consumption)
    @assert part_2_result == 94862124
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
