include(joinpath(@__DIR__(), "utils", "files.jl"))


count_easy_digits(entries::Array{Array{Array{String}}})::Int = sum(length(pattern) in [2, 3, 4, 7] for entry in entries for pattern in entry[2])

sum_decoded_outputs(entries::Array{Array{Array{String}}}) = sum(decode(entry[2], entry[1]) for entry in entries)

normalize_pattern(pattern::String)::String = join(sort(collect(pattern)))


function decode(four_digit_encoding::Array{String}, unique_signal_patterns::Array{String})::Int
    decoding_map = build_decoding_map(unique_signal_patterns)
    return parse(Int, join([decoding_map[normalize_pattern(pattern)] for pattern in four_digit_encoding]))
end


function build_decoding_map(unique_signal_patterns::Array{String})::Dict{String, Int}
    decoding_map::Dict{String, Int} = Dict{String, Int}()
    for pattern in unique_signal_patterns
        if length(pattern) == 2
            decoding_map[normalize_pattern(pattern)] = 1
        elseif length(pattern) == 3
            decoding_map[normalize_pattern(pattern)] = 7
        elseif length(pattern) == 4
            decoding_map[normalize_pattern(pattern)] = 4
        elseif length(pattern) == 7
            decoding_map[normalize_pattern(pattern)] = 8
        end
    end
    easy_digits_encoding_map::Dict{Int, String} = Dict(digit => code for (code, digit) in decoding_map)
    for pattern in unique_signal_patterns
        normalized_pattern = normalize_pattern(pattern)
        if !(normalized_pattern in keys(decoding_map))
            decoding_map[normalized_pattern] = guess_difficult_digit(normalized_pattern, easy_digits_encoding_map)
        end
    end
    return decoding_map
end


function guess_difficult_digit(normalized_pattern::String, easy_digits_encoding_map::Dict{Int, String})::Int 
    if (length(intersect(normalized_pattern, easy_digits_encoding_map[8])) == 6) & (length(intersect(normalized_pattern, easy_digits_encoding_map[4])) == 4)
        return 9
    elseif (length(intersect(normalized_pattern, easy_digits_encoding_map[8])) == 6) & (length(intersect(normalized_pattern, easy_digits_encoding_map[1])) == 1)
        return 6
    elseif length(intersect(normalized_pattern, easy_digits_encoding_map[8])) == 6
        return 0
    elseif length(intersect(normalized_pattern, easy_digits_encoding_map[1])) == 2
        return 3
    elseif length(intersect(normalized_pattern, easy_digits_encoding_map[4])) == 3
        return 5
    else
        return 2
    end
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    entries::Array{Array{Array{String}}} = map(line -> map(split, split(line, " | ")), readlines(input_file_path))
    
    # Part 1
    part_1_result::Int = count_easy_digits(entries)
    @assert part_1_result == 548
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = sum_decoded_outputs(entries)
    @assert part_2_result == 1074888
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
