def valueByLength = [2:1, 3:7, 4:4, 7:8]
def occurance = [1:0, 4:0, 7:0, 8:0]
new File('./input.txt').eachLine { l, lineNo ->
    def (signalString, valueString) = l.tokenize('|')*.trim()
    def values = valueString.tokenize()*.trim()
    def byLength = values.countBy { it.size() }.findAll { it.key in valueByLength.keySet() }
    byLength.each { length, count ->
        occurance[valueByLength[length]] += count
    }
}

println occurance*.value.sum()