include(joinpath(@__DIR__(), "utils", "files.jl"))


compute_power_consumption(report::Matrix{Int})::Int = gamma_rate(report) * epsilon_rate(report)

compute_life_support_rating(report::Matrix{Int})::Int = oxygen_rating(report) * co2_rating(report)

gamma_rate(report::Matrix{Int})::Int = parse(Int, join(map(most_common, eachcol(report))), base=2)

epsilon_rate(report::Matrix{Int})::Int = parse(Int, join(map(least_common, eachcol(report))), base=2)

oxygen_rating(report::Matrix{Int}, column::Int = 1)::Int = size(report, 1) == 1 ? parse(Int, join(report[1, :]), base=2) : oxygen_rating(report[report[:, column] .== most_common(report[:, column]), :], column + 1)

co2_rating(report::Matrix{Int}, column::Int = 1)::Int = size(report, 1) == 1 ? parse(Int, join(report[1, :]), base=2) : co2_rating(report[report[:, column] .== least_common(report[:, column]), :], column + 1)

most_common(column)::Int = count(==(0), column) > count(==(1), column) ? 0 : 1

least_common(column)::Int = count(==(1), column) < count(==(0), column) ? 1 : 0


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    report::Matrix{Int64} = read_matrix(input_file_path)

    # Part 1
    part_1_result::Int = @time compute_power_consumption(report)
    @assert part_1_result == 3309596
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time compute_life_support_rating(report)
    @assert part_2_result == 2981085
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
