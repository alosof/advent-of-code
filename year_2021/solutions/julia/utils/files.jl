YEAR_DIRECTORY = dirname(dirname(dirname(@__DIR__())))
INPUTS_FOLDER = joinpath(YEAR_DIRECTORY, "inputs")

function vecofvec_to_matrix(vecofvec:: Vector{Vector{T}})::Matrix{T} where T
    return Matrix(transpose(reshape(vcat(collect.(vecofvec)...), :, length(vecofvec))))
end

read_matrix(input_file_path::String)::Matrix{Int} = vecofvec_to_matrix([[parse(Int, b, base=10) for b in row] for row in readlines(input_file_path)])
