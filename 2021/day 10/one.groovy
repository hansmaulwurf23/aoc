def opener = ['(', '[', '<', '{']
def closer2Opener = [')':'(', ']':'[', '>':'<', '}':'{']
def malusPoints = [')': 3, ']': 57, '}': 1197, '>': 25137]
Long score = 0
new File('./input.txt').eachLine { l, lineNo ->
    def chunkStack = []
    def allGood = true
    l.each { c ->
        if (!allGood) return
        if (c in opener) {
            chunkStack.push(c)
        } else {
            if (chunkStack.last() == closer2Opener[c]) {
                // all good
                chunkStack.pop()
            } else {
                // corrupt
                println "${chunkStack.join('')} and found $c"
                score += malusPoints[c]
                allGood = false
            }
        }
    }
}

println score