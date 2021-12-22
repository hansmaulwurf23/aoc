def valueByLength = [2:1, 3:7, 4:4, 7:8]
def occurance = [1:0, 4:0, 7:0, 8:0]
def result = 0

new File('./input.txt').eachLine { l, lineNo ->
    def (signalString, valueString) = l.tokenize('|')*.trim()

    def signals = signalString.tokenize()
    def values = valueString.tokenize()

    def digits = [:]
    signals.each { signal ->
        if (signal.size() in valueByLength.keySet()) {
            digits[valueByLength[signal.size()]] = signal.split('')
        }
    }

    def valueDigits = []
    values.each { val ->
        def valSegs = val.split('')
        if (val.size() in valueByLength.keySet()) {
            valueDigits << valueByLength[val.size()]
        } else if (val.size() == 6) {
            // 0 6 9
            if ((valSegs - digits[4]).size() == 2) valueDigits << 9
            else if ((valSegs - digits[1]).size() == 5) valueDigits << 6
            else valueDigits << 0
        } else {
            // 2 3 5
            if ((valSegs - digits[4]).size() == 3) valueDigits << 2
            else if ((valSegs - digits[1]).size() == 4) valueDigits << 5
            else valueDigits << 3
        }
    }

    result += valueDigits.join('').toInteger()
}

println result