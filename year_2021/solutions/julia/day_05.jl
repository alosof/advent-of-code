include(joinpath(@__DIR__(), "utils", "files.jl"))


struct Point
    x::Int
    y::Int
end


struct Segment
    start_::Point
    end_::Point
end


function count_segment_overlaps(segments::Array{Segment}, use_diagonals::Bool)::Int
    visits = Dict{Point, Int}()
    for segment in segments
        if !use_diagonals & !is_horizontal_or_vertical(segment)
            continue
        end
        for point in get_points(segment)
            visits[point] = point in keys(visits) ? visits[point] + 1 : 1
        end
    end
    return length([p for p in keys(visits) if visits[p] > 1])
end


get_points(segment::Segment)::Array{Point} = [
    Point(x, y) 
    for (x, y) in ziplongest(segment.start_.x:x_growth_step(segment):segment.end_.x, segment.start_.y:y_growth_step(segment):segment.end_.y)
]

is_horizontal_or_vertical(segment::Segment)::Bool = (segment.start_.x == segment.end_.x) | (segment.start_.y == segment.end_.y)

x_growth_step(segment::Segment)::Int = segment.start_.x <= segment.end_.x ? 1 : -1

y_growth_step(segment::Segment)::Int = segment.start_.y <= segment.end_.y ? 1 : -1


function ziplongest(range_x::StepRange, range_y::StepRange)
    if (length(range_x) == 1) | (length(range_y) == 1)
        return [(x, y) for x in range_x for y in range_y]
    elseif (length(range_x) == length(range_y))
        return zip(range_x, range_y)
    else
        throw(ErrorException("The ranges $range_x and $range_y have different sizes and cannot be zipped."))
    end
end


read_segments(input_file_path::String)::Array{Segment} = [
    Segment(map(p -> Point(parse.(Int, split(p, ","))...), split(line, " -> "))...) 
    for line in readlines(input_file_path)
]


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    segments::Array{Segment} = read_segments(input_file_path)

    # Part 1
    part_1_result::Int = count_segment_overlaps(segments, false)
    @assert part_1_result == 5774
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = count_segment_overlaps(segments, true)
    @assert part_2_result == 18423
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
