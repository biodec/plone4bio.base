from plone.app.layout.viewlets import common as base

class SequenceViewlet(base.ViewletBase):
    """ """
    
    @property
    def sequenceLength(self):
        sequence = self.context.getSequence()
        return len(sequence)
        
    @property
    def sequence(self, n=10, sep= ' '):
        sequence = self.context.getSequence()
        if n:
            rvalue = ''
            while(len(sequence)>n):
                rvalue = rvalue + sep + sequence[:n]
                sequence = sequence[n:]
            rvalue = rvalue + sep + sequence
            return rvalue.strip()
        else:
            return sequence

    @property
    def alphabet(self):
        return self.context.getAlphabet()

