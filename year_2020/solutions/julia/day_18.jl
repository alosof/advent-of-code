include(joinpath(@__DIR__(), "utils", "files.jl"))


∧(a::Int, b::Int) = a + b       # Custom addition operator with multiplication precedence

∨(a::Int, b::Int) = a * b       # Custom multiplication operator with addition precedence

do_homework_with_no_precedence(exprs::Array{String})::Int = sum(map(eval ∘ Meta.parse ∘ (e -> replace(e, '+' => '∧')), exprs))

do_homework_with_addition_precedence(exprs::Array{String})::Int = sum(map(eval ∘ Meta.parse ∘ (e -> replace(e, '+' => '∧')) ∘ (e -> replace(e, '*' => '∨')), exprs))


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, "day_18", "input.txt")
    input_list::Array{String} = readlines(input_file_path)

    # Part 1
    part_1_result::Int = do_homework_with_no_precedence(input_list)
    @assert part_1_result == 1890866893020
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = do_homework_with_addition_precedence(input_list)
    @assert part_2_result == 34646237037193
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
