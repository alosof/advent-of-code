include(joinpath(@__DIR__(), "utils", "files.jl"))


count_answered_by_anyone_in_group(groups::Array{Array{String}})::Int = sum(map(length ∘ (group -> mapreduce(Set, union, group)), groups))

count_answered_by_everyone_in_group(groups::Array{Array{String}})::Int = sum(map(length ∘ (group -> mapreduce(Set, intersect, group)), groups))


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, "day_06", "input.txt")
    input_list::Array{Array{String}} = map(block -> split(block, "\n"), split(read(input_file_path, String), "\n\n"))

    # Part 1
    part_1_result::Int = @time count_answered_by_anyone_in_group(input_list)
    @assert part_1_result == 6585
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time count_answered_by_everyone_in_group(input_list)
    @assert part_2_result == 3276
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
