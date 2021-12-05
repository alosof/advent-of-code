include(joinpath(@__DIR__(), "utils", "files.jl"))

import Pkg; Pkg.add("Combinatorics")

using Combinatorics: combinations


process_expense_report(input_sequence::Array{Int}, tuple_size::Int, expected_sum::Int)::Int = prod(
    first(
        Iterators.filter(
            c -> sum(c) == expected_sum, 
            combinations(sort(input_sequence), tuple_size)
        )
    )
)


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, "day_01", "input.txt")
    input_list::Array{Int} = parse.(Int, readlines(input_file_path))

    # Part 1
    part_1_result::Int = process_expense_report(input_list, 2, 2020)
    @assert part_1_result == 270144
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = process_expense_report(input_list, 3, 2020)
    @assert part_2_result == 261342720
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
