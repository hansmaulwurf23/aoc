def opener2Closer = ['(':')', '[':']', '<':'>', '{':'}']
def closer2Opener = [')':'(', ']':'[', '>':'<', '}':'{']
def malusPoints = [')': 1, ']': 2, '}': 3, '>': 4]
def scores = []

new File('./input.txt').eachLine { l, lineNo ->
    def chunkStack = []
    def lineCorrupt = false
    Long score = 0

    l.each { c ->
        if (lineCorrupt) return
        if (c in opener2Closer.keySet()) {
            chunkStack.push(c)
        } else {
            if (chunkStack.last() == closer2Opener[c]) {
                // all good
                chunkStack.pop()
            } else {
                // corrupt
                lineCorrupt = true
            }
        }
    }

    if (!lineCorrupt) {
        while(chunkStack) {
            def last = chunkStack.pop()
            score = (score * 5) + malusPoints[opener2Closer[last]]
        }
    }

    if (score) scores << score
}

scores.sort(true)
println scores
println scores[(scores.size()/2).toInteger()]