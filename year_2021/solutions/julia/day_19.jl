include(joinpath(@__DIR__(), "utils", "files.jl"))


rotation_matrices = [
    [1 0 0; 0 1 0; 0 0 1],
    [1 0 0; 0 0 -1; 0 1 0],
    [1 0 0; 0 -1 0; 0 0 -1],
    [1 0 0; 0 0 1; 0 -1 0],
    [0 0 1; 1 0 0; 0 1 0],
    [0 1 0; 1 0 0; 0 0 -1],
    [0 0 -1; 1 0 0; 0 -1 0],
    [0 -1 0; 1 0 0; 0 0 1],
    [0 1 0; 0 0 1; 1 0 0],
    [0 0 -1; 0 1 0; 1 0 0],
    [0 -1 0; 0 0 -1; 1 0 0],
    [0 0 1; 0 -1 0; 1 0 0],
    [-1 0 0; 0 -1 0; 0 0 1],
    [-1 0 0; 0 0 1; 0 1 0],
    [-1 0 0; 0 1 0; 0 0 -1],
    [-1 0 0; 0 0 -1; 0 -1 0],
    [0 0 1; -1 0 0; 0 -1 0],
    [0 -1 0; -1 0 0; 0 0 -1],
    [0 0 -1; -1 0 0; 0 1 0],
    [0 1 0; -1 0 0; 0 0 1],
    [0 1 0; 0 0 -1; -1 0 0],
    [0 0 1; 0 1 0; -1 0 0],
    [0 -1 0; 0 0 1; -1 0 0],
    [0 0 -1; 0 -1 0; -1 0 0]
]


function find_common_beacons(scanner1, scanner2)
    final_res = Dict{Matrix{Int}, Tuple{Vector, Int}}()
    res = Dict{Matrix{Int}, Dict{Vector, Int}}()
    for R in rotation_matrices
        res[R] = Dict{Vector, Int}()
        translations = []
        rotated_scanner1_beacons = map(b -> R * b, scanner1)
        for s1b in rotated_scanner1_beacons
            for s2b in scanner2
                push!(translations, s2b - s1b)
            end
        end
        for tv in translations
            res[R][tv] = get(res[R], tv, 0) + 1
        end
        final_res[R] = [(k, v) for (k, v) in res[R] if v == maximum(values(res[R]))][1]
    end
    return [(k, v) for (k, v) in final_res if v[2] == maximum(map(pair -> pair[2], values(final_res)))][1]
end

function scanner_pairs_overlaps(scanners)
    scanner_ids = sort(collect(keys(scanners)))
    res = Dict()
    for scanner1 in scanner_ids
        for scanner2 in (scanner1 + 1):maximum(scanner_ids)
            res[(scanner1, scanner2)] = find_common_beacons(scanners[scanner1], scanners[scanner2])
            res[(scanner2, scanner1)] = find_common_beacons(scanners[scanner2], scanners[scanner1])
        end
    end
    return res
end

function coords(scanners)
    res = Dict()
    res[0] = ([0, 0, 0], [1 0 0; 0 1 0; 0 0 1])
    overlaps = scanner_pairs_overlaps(scanners)
    large_overlaps = Dict(filter(
        e -> e[2][2][2] >= 12,
        collect(overlaps)
    ))
    graph = build_graph(large_overlaps)
    for i in 1:(length(scanners) - 1)
        chain_to_0 = find_path(graph, 0, i, Set())
        rotation = [1 0 0; 0 1 0; 0 0 1]
        for p in chain_to_0
            rotation = large_overlaps[p][1] * rotation
        end
        res[i] = (find_absolute_coords(chain_to_0, large_overlaps), rotation)
    end
    return res
end

forward(p, R, T) = R * p + T

backward(p, R, T) = transpose(R) * (p - T)


function find_absolute_coords(chain_to_0, overlaps)
    pos = [0, 0, 0]
    for pair in chain_to_0
        rotation = overlaps[pair][1]
        translation = overlaps[pair][2][1]
        pos = backward(pos, rotation, translation)
    end
    return pos
end

function build_graph(overlaps)
    res = Dict()
    for pair in keys(overlaps)
        res[pair[1]] = vcat(get(res, pair[1], [])..., pair[2])
    end
    return res
end

function find_path(graph, source, destination, visited)
    if source == destination
        return []
    else
        for next_source in graph[source]
            if !(next_source in visited)
                push!(visited, next_source)
                sub_path = find_path(graph, next_source, destination, visited)
                if !isnothing(sub_path)
                    return vcat(sub_path..., (source, next_source))
                end
            end
        end
    end
end

function largest_distance(scanners)
    positions = map(p -> p[1], values(coords(scanners)))
    max_dist = 0
    for a in positions
        for b in positions
            max_dist = max(max_dist, sum(abs.(a - b)))
        end
    end
    return max_dist
end

function beacons(scanners)
    res = Set()
    overlaps = scanner_pairs_overlaps(scanners)
    large_overlaps = Dict(filter(
        e -> e[2][2][2] >= 12,
        collect(overlaps)
    ))
    graph = build_graph(large_overlaps)
    for (sc, beacons) in scanners
        path = find_path(graph, 0, sc, Set())
        for b in beacons
            for edge in path
                rotation = large_overlaps[edge][1]
                translation = large_overlaps[edge][2][1]
                b = backward(b, rotation, translation)
            end
            push!(res, b)
        end
    end
    return length(res)
end

function read_scanners(p)
    blocks = split(read(open(p), String), "\n\n")
    return Dict([
        (i-1, [parse.(Int, split(line, ",")) for line in split(block, "\n")[2:end]]) 
        for (i, block) in enumerate(blocks)
    ])
end


function main()
    input_file_path::String = joinpath(INPUTS_FOLDER, splitext(basename(@__FILE__))[1], "input.txt")
    scanners = read_scanners(input_file_path)

    # Part 1
    part_1_result::Int = beacons(scanners)
    @assert part_1_result == 408
    println("Part 1 result : ", part_1_result)

    # Part 2
    part_2_result::Int = largest_distance(scanners)
    @assert part_2_result == 13348
    println("Part 2 result : ", part_2_result)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
