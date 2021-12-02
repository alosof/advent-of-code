function find_encryption_key(door_public_key::Int, card_public_key::Int)::Int
    card_loop_size::Int = 1
    while true
        if powermod(7, card_loop_size, 20201227) == card_public_key
            return powermod(door_public_key, card_loop_size, 20201227)
        end
        card_loop_size += 1
    end
end


function main()
    door_pub = 17607508
    card_pub = 15065270

    # Part 1
    part_1_result::Int = @time find_encryption_key(door_pub, card_pub)
    @assert part_1_result == 12285001
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Char = @time '🎄'
    @assert part_2_result == '🎄'
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
