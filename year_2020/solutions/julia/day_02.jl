include(joinpath(@__DIR__(), "utils", "files.jl"))


struct Rule
    password::String
    control_letter::Char
    low::Int
    high::Int
end

count_valid_passwords(input_sequence::Array{String}, check_function::Function)::Int = count(map(check_function ∘ parse_rule, input_sequence))

function parse_rule(line::String)::Rule
    bounds::String, letter_with_colon::String, password::String = split(line, ' ')
    low::Int, high::Int = parse.(Int, split(bounds, '-'))
    control_letter::Char = letter_with_colon[begin]
    return Rule(password, control_letter, low, high)
end

check_validity_old_policy(rule::Rule)::Bool = rule.low <= count(string(rule.control_letter), rule.password) <= rule.high

check_validity_new_policy(rule::Rule)::Bool = xor(rule.password[rule.low] == rule.control_letter, rule.password[rule.high] == rule.control_letter)


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, "day_02", "input.txt")
    input_list::Array{String} = readlines(input_file_path)
    
    # Part 1
    part_1_result::Int = @time count_valid_passwords(input_list, check_validity_old_policy)
    @assert part_1_result == 506
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time count_valid_passwords(input_list, check_validity_new_policy)
    @assert part_2_result == 443
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
