import org.codehaus.groovy.runtime.DefaultGroovyMethods

def bitsCounter = null

def filterEntriesByCriticalVal = { entries, sIdx, Closure critClosure, defaultCritVal ->
    if (entries.size() == 1) return entries
    Map countedVals = entries*.getAt(sIdx).countBy { it }
    def critVal
    if (countedVals*.value.unique().size() > 1) {
        critVal = critClosure.call(countedVals, { it.value }).key
    } else {
        critVal = defaultCritVal
    }
    // return filtereds
    entries.findAll { it[sIdx] == critVal }
}

def findMost = { entries, sIdx ->
    return filterEntriesByCriticalVal(entries, sIdx, DefaultGroovyMethods.&max, 1)
}

def findLeast = { entries, sIdx ->
    return filterEntriesByCriticalVal(entries, sIdx, DefaultGroovyMethods.&min, 0)
}

def binData = []
new File('./input.txt').eachLine { l ->
    binData << l.collect()*.toInteger()
}

def oxyEntries = binData
def co2Entries = binData
(0..(binData[0].size()-1)).each { curIdx ->
    oxyEntries = findMost(oxyEntries, curIdx)
    co2Entries = findLeast(co2Entries, curIdx)
}

println oxyEntries
println co2Entries

def oxyRate = Integer.parseInt(oxyEntries[0].join(''), 2)
def co2Rate = Integer.parseInt(co2Entries[0].join(''), 2)

println "${oxyRate * co2Rate}"