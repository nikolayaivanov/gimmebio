

################################################################################

class Fastx:
    def __init__(self):
        pass
    
    def parseIdLine(self,sid):
        sid = sid.strip()[1:].split()
        try:
            self.tags = sid[1:]
        except IndexError as ie:
            self.tags = []
        self.sid = sid[0]
    

class Fasta( Fastx):

    def __init__(self, sid, seq):
        super(Fasta, self).__init__()
        self.parseIdLine(sid)
        self.seq = seq.strip()

    def __str__(self):
        tags = '\t'.join( self.tags)
        out = '>{} {}\n{}\n'.format(self.sid, tags, self.seq)
        return out

    @classmethod
    def fromRaw(cls, inp):
        if type(inp) == str:
            inp = inp.split('\n')
        assert len(inp) == 2
        return Fasta( inp[0], inp[1])
    
class Fastq( Fastx):

    def __init__(self, sid, seq, delim, qual):
        self.parseIdLine(sid)
        self.seq = self.seq.strip()
        self.sdelim = delim.strip()
        self.qual = qual.strip()

        assert len(self.qual) == len(self.seq)
        
    def __str__(self):
        tags = '\t'.join(self.tags)
        out = '@{}\t{}\n{}\n{}\n{}'.format(self.sid,
                                           tags,
                                           self.seq,
                                           self.delim,
                                           self.qual)
        return out

    @classmethod
    def fromRaw(cls, inp):
        if type(inp) == str:
            inp = inp.split('\n')
        assert len(inp) == 4
        return Fastq( inp[0], inp[1], inp[2], inp[3])

    
class ReadPair:

    def __init__(self, r1, r2):
        assert r1.sid == r2.sid
        assert type(r1) == type(r2)
        self.r1 = r1
        self.r2 = r2
        
def iterChunks(filelike, n):
    chunk = []
    for line in filelike:
        chunk.append(line)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk

################################################################################
        
def iterFastq(filelike, interleaved=False):
    n = 4
    if interleaved:
        n = 8
    for chunk in iterChunks(filelike, n):
        r1 = Fastq.fromRaw( chunk[:4])
        if interleaved:
            r2 = Fastq.fromRaw( chunk[4:])
            yield ReadPair(r1,r2)
        else:
            yield r1


def iterFasta(filelike, interleaved=False):
    n = 2
    if interleaved:
        n = 4
    for chunk in iterChunks(filelike, n):
        r1 = Fasta.fromRaw( chunk[:2])
        if interleaved:
            r2 = Fasta.fromRaw( chunk[2:])
            yield ReadPair(r1,r2)
        else:
            yield r1
            
            
