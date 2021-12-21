Long hor = 0
Long depth = 0
Long aim = 0
new File('./input.txt').eachLine { l ->
    def (dir, xStr) = l.tokenize()
    Long x = xStr.toLong()
    switch (dir) {
        case 'forward':
            hor += x
            depth += (x * aim)
            break
        case 'down':
            aim += x
            break
        case 'up':
            aim -= x
    }
}

println "${depth * hor}"