include(joinpath(@__DIR__(), "utils", "files.jl"))


function find_first_winning_board_score(bingo::Array{Int}, boards::Dict{Int, Matrix{Int}})::Int
    boards_ = copy(boards)
    for number in bingo
        for i in keys(boards_)
            mark_number!(number, boards_[i])
            if has_complete_line(boards_[i])
                return score(number, boards_[i])
            end
        end
    end
end


function find_last_winning_board_score(bingo::Array{Int}, boards::Dict{Int, Matrix{Int}})::Int
    boards_ = copy(boards)
    done_boards = Set()
    for number in bingo
        for i in keys(boards_)
            if !(i in done_boards)
                mark_number!(number, boards_[i])
                if has_complete_line(boards_[i])
                    push!(done_boards, i)
                    if length(done_boards) == length(boards_)
                        return score(number, boards_[i])
                    end
                end
            end
        end
    end
end


score(number::Int, board::Matrix{Int})::Int = number * sum(filter(!=(-1), board))

mark_number!(number::Int, board::Matrix{Int}) = board[board.==number] .= -1

has_complete_line(board::Matrix{Int})::Bool = any(all(map(==(-1), board), dims=1)) | any(all(map(==(-1), board), dims=2))


function read_bingo_and_boards(input_file_path::String)::Tuple{Array{Int}, Dict{Int, Matrix{Int}}}
    content = open(f -> read(f, String), input_file_path)
    blocks = split(content, "\n\n")
    bingo = parse.(Int, split(blocks[1], ","))
    boards = Dict{Int, Matrix{Int}}()
    for (i, block) in enumerate(blocks[2:end])
        boards[i] = vecofvec_to_matrix([[parse(Int, e) for e in split(row)] for row in split(block, "\n")])
    end
    return bingo, boards
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    bingo, boards = read_bingo_and_boards(input_file_path)

    # Part 1
    part_1_result::Int = @time find_first_winning_board_score(bingo, boards)
    @assert part_1_result == 63552
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = @time find_last_winning_board_score(bingo, boards)
    @assert part_2_result == 9020
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
