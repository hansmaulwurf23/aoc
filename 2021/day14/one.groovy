def template
def rules = [:]
new File('./input.txt').eachLine { l, lineNo ->
    if (lineNo == 1) {
        template = l
    } else if (l.trim()) {
        def (pattern, creation) = l.tokenize('->')*.trim()
        rules[pattern] = creation
    }
}

def cycle = {
    def newTemplate = new StringBuffer()
    (0..(template.size() - 2)).each { pos ->
        def pair = template[pos..(pos+1)]
        def newEl = rules[pair]

        newTemplate.append(template[pos])
        if (newEl) {
            newTemplate.append(newEl)
        }
    }
    newTemplate.append(template[-1])
    template = newTemplate.toString()
}

(1..10).each {
    cycle()
    //println template
}
def stats = template.split('').countBy { it }.values().sort { it.value }
println (stats[-1] - stats[0])