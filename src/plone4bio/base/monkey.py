from Bio.SeqIO.InsdcIO import GenBankWriter

def _write_feature(self, feature):
    """Write a single SeqFeature object to features table.

     source          1..840
                     /organism="Escherichia coli str. K-12 substr. MG1655"
                     /mol_type="genomic DNA"
                     /strain="K-12"
                     /sub_strain="MG1655"
                     /db_xref="taxon:511145"
    """
    self.handle.write("     %s%s %s..%s\n" % (feature.type, " " * max(0, (16 - len(str(feature.type)))),
        feature.location._start.position + 1, feature.location._end))
    for (key, list) in feature.qualifiers.items():
        if type(list) != type([]):
            list = [list,]
        for value in list:
            value = str(value)
            dummy = 1 + len(key) + 2
            end = min(len(value), 58 - dummy)
            self.handle.write('%s/%s="%s' % (" "*21, key, value[0:end]))
            while (end < len(value)):
                start = end
                end = min(len(value), end + 58)
                self.handle.write('\n%s%s' % (" "*21, value[start:end]))
            self.handle.write('"\n')
    
GenBankWriter._write_feature = _write_feature


