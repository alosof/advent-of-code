include(joinpath(@__DIR__(), "utils", "files.jl"))


autocomplete_score(lines::Array{String})::Int = median(autocomplete_score.(filter(is_incomplete, lines)))


function  autocomplete_score(incomplete_line::String)::Int
    openers = []
    for c in incomplete_line
        if c in ['(', '[', '{', '<']
            push!(openers, c)
        else
            pop!(openers)
        end
    end
    res = foldl((x, y) -> 5 * x + y, pushfirst!((legal_closing_score ∘ opposite).(reverse(openers)), 0))
    return res
end


syntax_error_score(lines::Array{String})::Int = sum(syntax_error_score.(lines))


function syntax_error_score(line::String)::Int
    openers = []
    for c in line
        if c in ['(', '[', '{', '<']
            push!(openers, c)
        else
            last_opener = pop!(openers)
            if opposite(last_opener) != c
                return illegal_closing_score(c)
            end
        end
    end
    return 0
end


is_incomplete(line::String)::Bool = syntax_error_score(line) == 0


function legal_closing_score(character::Char)::Int
    if character == ')'
        return 1
    elseif character == ']'
        return 2
    elseif character == '}'
        return 3
    elseif character == '>'
        return 4
    end
end


function illegal_closing_score(character::Char)::Int
    if character == ')'
        return 3
    elseif character == ']'
        return 57
    elseif character == '}'
        return 1197
    elseif character == '>'
        return 25137
    end
end


function opposite(character::Char)::Char
    if character == '('
        return ')'
    elseif character == '['
        return ']'
    elseif character == '{'
        return '}'
    elseif character == '<'
        return '>'
    elseif character == ')'
        return '('
    elseif character == ']'
        return '['
    elseif character == '}'
        return '{'
    elseif character == '>'
        return '<'
    end
end


median(scores::Array{Int}) = sort(scores)[div(length(scores), 2) + 1]


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    lines::Array{String} = readlines(input_file_path)

    # Part 1
    part_1_result::Int = syntax_error_score(lines)
    @assert part_1_result == 294195
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = autocomplete_score(lines)
    @assert part_2_result == 3490802734
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
