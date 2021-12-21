def c = 0
Long prev
new File('./input.txt').eachLine { l ->
    Long v = new Long(l)
    if (prev && prev < v) c++
    prev = v
}

println "$c"