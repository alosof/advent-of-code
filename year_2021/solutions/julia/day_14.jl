include(joinpath(@__DIR__(), "utils", "files.jl"))


function pair_insertion(polymer::String, rules::Dict{String, Char}, steps::Int)::Int
    chars = count_chars(polymer)
    pairs = count_pairs(polymer)
    for _ in 1:steps
        new_pairs = Dict{String, Int}()
        for pair in keys(pairs)
            inserted_char = rules[pair]
            chars[inserted_char] = get(chars, inserted_char, 0) + pairs[pair]
            left_pair = pair[1] * inserted_char
            right_pair = inserted_char * pair[2]
            new_pairs[left_pair] = get(new_pairs, left_pair, 0) + pairs[pair]
            new_pairs[right_pair] = get(new_pairs, right_pair, 0) + pairs[pair]
        end
        pairs = new_pairs
    end
    return maximum(values(chars)) - minimum(values(chars))
end


count_chars(polymer::String)::Dict{Char, Int} = Dict([(c, count(c, polymer)) for c in Set(polymer)])

count_pairs(polymer::String)::Dict{String, Int} = Dict([(polymer[i:i+1], count(polymer[i:i+1], polymer)) for i in 1:(length(polymer) - 1)])


function read_polymer_and_rules(input_file_path::String)::Tuple{String, Dict{String, Char}}
    lines = readlines(input_file_path)
    polymer = lines[1]
    rules = Dict{String, Char}()
    for line in lines[3:end]
        pair, char = split(line, " -> ")
        rules[pair] = char[1]
    end
    return polymer, rules
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    polymer, rules = read_polymer_and_rules(input_file_path)

    # Part 1
    part_1_result::Int = pair_insertion(polymer, rules, 10)
    @assert part_1_result == 3048
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = pair_insertion(polymer, rules, 40)
    @assert part_2_result == 3288891573057
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
