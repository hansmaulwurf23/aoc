Long hor = 0
Long depth = 0
new File('./input.txt').eachLine { l ->
    def (dir, x) = l.tokenize()
    switch (dir) {
        case 'forward':
            hor += x.toLong()
            break
        case 'down':
            depth += x.toLong()
            break
        case 'up':
            depth -= x.toLong()
    }
}

println "${depth * hor}"