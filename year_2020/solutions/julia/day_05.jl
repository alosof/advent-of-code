include(joinpath(@__DIR__(), "utils", "files.jl"))


function get_missing_id(seats::Array{String})::Int
    ordered_seat_ids::Array{Int} = sort([compute_seat_id(seat) for seat in(seats)])
    for i in (1:length(ordered_seat_ids))
        if ordered_seat_ids[i + 1] - ordered_seat_ids[i] == 2
            return ordered_seat_ids[i] + 1
        end
    end
end

get_max_id(seats::Array{String})::Int = maximum((compute_seat_id(seat) for seat in (seats)))

compute_seat_id(seat::String)::Int = get_row(seat) * 8 + get_column(seat)

get_row(seat::String)::Int = parse(Int, replace(replace(seat[begin:(end - 3)], 'F' => '0'), 'B' => '1'), base=2)

get_column(seat::String)::Int = parse(Int, replace(replace(seat[(end - 2):end], 'L' => '0'), 'R' => '1'), base=2)


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, "day_05", "input.txt")
    input_list::Array{String} = readlines(input_file_path)

    # Part 1
    part_1_result::Int = @time get_max_id(input_list)
    @assert part_1_result == 953
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time get_missing_id(input_list)
    @assert part_2_result == 615
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
