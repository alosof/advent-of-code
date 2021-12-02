function get_last_spoken_number(starting_sequence::Array{Int}, turns_to_play::Int)::Int
    game_memory::Dict{Int,Int} = Dict((v, k) for (k, v) in enumerate(starting_sequence))
    turn::Int = length(starting_sequence) + 1
    spoken_number::Int = 0
    while turn < turns_to_play
        previous_time::Int = get(game_memory, spoken_number, -1)
        game_memory[spoken_number] = turn
        spoken_number = (previous_time == -1) ? 0 : turn - previous_time
        turn += 1
    end
    return spoken_number
end


function main()
    input_list::Array{Int} = [9, 19, 1, 6, 0, 5, 4]

    # Part 1
    part_1_result::Int = @time get_last_spoken_number(input_list, 2020)
    @assert part_1_result == 1522
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time get_last_spoken_number(input_list, 30000000)
    @assert part_2_result == 18234
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
