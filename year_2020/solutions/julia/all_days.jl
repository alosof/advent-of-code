for script in(readdir(@__DIR__())) 
    if startswith(script, "day_")
        day_number::String = split(split(script, ".")[1], "_")[2]
        println("\n******* Day $(day_number) *******\n")
        include(script)
        main()
    end
end

println()