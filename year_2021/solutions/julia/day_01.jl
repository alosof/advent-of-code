include(joinpath(@__DIR__(), "utils", "files.jl"))


count_measurement_increases(measurements::Array{Int})::Int = sum((circshift(measurements, -1) - measurements)[begin:end - 1] .> 0)

compute_size_three_window_sums(measurements::Array{Int})::Array{Int} = [sum(measurements[i:i+2]) for i in 1:length(measurements) - 2]


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    measurements::Array{Int} = parse.(Int, readlines(input_file_path))
    
    # Part 1
    part_1_result::Int = @time count_measurement_increases(measurements)
    @assert part_1_result == 1521
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time (count_measurement_increases ∘ compute_size_three_window_sums)(measurements)
    @assert part_2_result == 1543
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
