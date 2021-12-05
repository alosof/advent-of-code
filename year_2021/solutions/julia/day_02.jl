include(joinpath(@__DIR__(), "utils", "files.jl"))


function move_with_simple_commands(instructions_list::Array{String})::Int
    position, depth = 0, 0
    for instruction in instructions_list
        command, value = split(instruction)
        if command == "forward"
            position += parse(Int, value)
        elseif command == "down"
            depth += parse(Int, value)
        elseif command == "up"
            depth -= parse(Int, value)
        end
    end
    return position * depth
end


function move_with_advanced_commands(instructions_list::Array{String})::Int
    position, depth, aim = 0, 0, 0
    for instruction in instructions_list
        command, value = split(instruction)
        if command == "forward"
            position += parse(Int, value)
            depth += aim * parse(Int, value)
        elseif command == "down"
            aim += parse(Int, value)
        elseif command == "up"
            aim -= parse(Int, value)
        end
    end
    return position * depth
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    instructions::Array{String} = readlines(input_file_path)
    
    # Part 1
    part_1_result::Int = move_with_simple_commands(instructions)
    @assert part_1_result == 1459206
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = move_with_advanced_commands(instructions)
    @assert part_2_result == 1320534480
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
