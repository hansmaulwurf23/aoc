def c = 0
Long prev
def summedReads = new File('./input.txt').text.tokenize()
        *.toLong()
        .collate(3, 1, false)
        *.sum()

summedReads.each { v ->
    if (prev && prev < v) c++
    prev = v
}

println "$c"