def hexString = new File('./input.txt').text.split('')
def sb = new StringBuffer(hexString.size()*4)
def readPosition = 0

hexString.each { hex ->
    if (!(hex ==~ /^[0-9A-F]+$/)) return
    sb.append(Long.toBinaryString(Long.parseLong(hex, 16 )).padLeft(4, '0'))
}
def binaryString = sb.toString()

def readBits = { int count ->
    def r = binaryString[readPosition..(readPosition+count-1)]
    readPosition += + count
    return r
}

def parse = { int length ->
    return Integer.parseInt(readBits(length), 2)
}

def parseLiteralRec
parseLiteralRec = { String readString ->
    def block = readBits(5)
    def value = block[1..-1]
    if (block[0] == '1') {
        return (value + parseLiteralRec())
    } else {
        return value
    }
}

def parseLiteral = {
    return Long.parseLong(parseLiteralRec(""), 2)
}

def parsePacketHeader = {
    def header= [
            version: parse(3),
            type : parse(3)
    ]
    return header
}

def parsePacket
parsePacket = {
    def packetHeader = parsePacketHeader()
    if (packetHeader.type == 4) {
        parseLiteral()
    } else {
        def args = []
        def lengthTypeID = readBits(1).toInteger()
        if (lengthTypeID == 0) {
            def totalLength = Integer.parseInt(readBits(15), 2)
            def subPacketEndPosition = readPosition + totalLength
            while (readPosition < subPacketEndPosition) {
                args << parsePacket()
            }
        } else {
            def numSubPackets = Integer.parseInt(readBits(11), 2)
            (1..numSubPackets).each {
                args << parsePacket()
            }
        }

        switch (packetHeader.type) {
            case 0:
                return args.sum()
            case 1:
                return args.inject(1) { acc, val -> acc * val }
            case 2:
                return args.min()
            case 3:
                return args.max()
            case 5:
                return (args[0] > args[1] ? 1 : 0)
            case 6:
                return (args[0] < args[1] ? 1 : 0)
            case 7:
                return (args[0] == args[1] ? 1 : 0)
        }
    }
}

println parsePacket()