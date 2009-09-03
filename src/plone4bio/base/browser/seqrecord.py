#
from zope.formlib import form
from zope.component import createObject

from plone.app.form import base
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# from plone4bio.base.content.seqrecord import SeqRecordProxy, SeqProxy 
from plone4bio.base.interfaces import ISeqRecord
from plone4bio.base import Plone4BioMessageFactory as _

from Bio import SeqIO
from StringIO import StringIO


"""
class SeqRecordWidget(ObjectWidget):
    # TODO: create a CustomSeqWidget
    seq_widget = CustomWidgetFactory(ObjectWidget, SeqProxy)
"""

class SeqRecordAddForm(base.AddForm):
    """Add form """
    form_fields = form.Fields(ISeqRecord)
    # form_fields['seqrecord'].custom_widget = CustomWidgetFactory(SeqRecordWidget, SeqRecordProxy)
    label = _(u"Add SeqRecord")
    form_name = _(u"Add SeqRecord")
    def create(self, data):
        seqrecord = createObject(u"plone4bio.base.SeqRecord", title=data['title'])
        form.applyChanges(seqrecord, self.form_fields, data)
        return seqrecord

class SeqRecordEditForm(base.EditForm):
    form_fields = form.Fields(ISeqRecord)
    # form_fields['sequence'].field.readonly = True
    # form_fields['seqrecord'].custom_widget = CustomWidgetFactory(SeqRecordWidget, SeqRecordProxy)
    label = _(u"Edit SeqRecord")
    form_name = _(u"Edit SeqRecord")

#TODO: adapter ???
class SeqRecord2Genbank(BrowserView):
    """ """
    def __call__(self):
        io = StringIO()
        # FIXME:
        self.context.Description()
	## CHECK LUNGHEZZA LOCUS < 16
	seqrecord = self.context.seqrecord
	if len(seqrecord.name) > 16:
		seqrecord.name = ''
        SeqIO.write([seqrecord, ], io, "genbank")
        return io.getvalue()
    
#TODO: adapter ???
class SeqRecord2Fasta(BrowserView):
    """ """
    def __call__(self):
        io = StringIO()
        # FIXME:
        self.context.Description()
        SeqIO.write([self.context.seqrecord, ], io, "fasta")
        return io.getvalue()

#TODO: use viewlet
class SeqRecordAnnotationsView(BrowserView):
    """ """
    __call__ = ViewPageTemplateFile('templates/annotations.pt')

#TODO: use viewlet
class SeqRecordFeaturesView(BrowserView):
    """ """
    __call__ = ViewPageTemplateFile('templates/features.pt')

#TODO: use viewlet
class SeqRecordDbxrefsView(BrowserView):
    """ """
    __call__ = ViewPageTemplateFile('templates/dbxrefs.pt')
    def getdbxref_url(self, dbxrefdb, key):
        if urldict.has_key(dbxrefdb):
                if dbxrefdb == 'Internal':
                        dbid, accessionv = key.split(':')
                        try :
                                accession = accessionv.split('.')[0]
                                seqrecord = self.getSeqRecordFromAccession(accession, dbid)
                                id = seqrecord._primary_id
                                url = '/'.join(self.getURL().split('/')[:-2] + [dbid, str(id)])
                                return url
                        except:
                                return '#'
                if dbxrefdb == 'UniGene':
                        cid = key.split('.')[-1]
                        org = key.split('.')[0]
                        return urldict[dbxrefdb] % (org, cid)
                if dbxrefdb == 'Ensemble':
                        dbxrefdb = key[:4]
                if dbxrefdb == 'HGNC':
                        key = key.split(':')[-1]
                        if key.isdigit():  dbxrefdb = 'HGNC_ID'
                        else:  dbxrefdb = 'HGNC_NAME'
                if dbxrefdb == 'HPRD':
                        key = key.split('HPRD_')[-1]
                if dbxrefdb == 'IPI':
                        key = key.split('.')[0]
                ## Othewise
                return urldict[dbxrefdb] % key

class SeqRecordView(BrowserView):
    """ """
    def Sequence(self, n=10, sep= ' '):
        sequence = self.context.Sequence()
        if n:
            rvalue = ''
            while(len(sequence)>n):
                rvalue = rvalue + sep + sequence[:n]
                sequence = sequence[n:]
            rvalue = rvalue + sep + sequence
            return rvalue.strip()
        else:
            return sequence

class SeqRecordPredictors(BrowserView):
    """ """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.tool = getToolByName(self.context, "plone4bio_predictors")

    #@property
    #@memoize
    #def tool(self):
    #    return getToolByName(self.context, "plone4bio_predictors")

    def getPredictors(self):
        return self.tool.values()

    def runPredictor(self):
        self.tool(self.request.form['predictor'], self.context, store=True)


#TODO: move on registry ?
urldict = {
       'GO': 'http://amigo.geneontology.org/cgi-bin/amigo/term-details.cgi?term=%s',
       'EMBL':'http://www.ebi.ac.uk/cgi-bin/sva/sva.pl/?search=Go!&query=%s',
       'Ensembl' : 'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=%s',
       'ENSG' : 'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=%s',
       'ENST' : 'http://www.ensembl.org/Homo_sapiens/Transcript/Summary?t=%s',
       'ENSP' : 'http://www.ensembl.org/Homo_sapiens/Transcript/ProteinSummary?p=%s',
       'GermOnline' : 'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=%s',
       'OTTHUMG' : 'http://vega.sanger.ac.uk/Homo_sapiens/geneview?gene=%s',
       'OTTT' : 'http://vega.sanger.ac.uk/Homo_sapiens/transview?transcript=%s',
       'OTTP' : 'http://vega.sanger.ac.uk/Homo_sapiens/protview?peptide=%s',
       'shares_CDS_with_OTTT' : 'http://vega.sanger.ac.uk/Homo_sapiens/transview?transcript=%s',
       'EMBL' : 'http://www.ebi.ac.uk/cgi-bin/sva/sva.pl/?search=Go!&query=%s',
       'PUBMED' : 'http://www.ncbi.nlm.nih.gov/sites/entrez/%s',
       'EntrezGene' : 'http://www.ncbi.nlm.nih.gov/sites/entrez?db=gene&term=%s',
       'GeneID' : 'http://www.ncbi.nlm.nih.gov/sites/entrez?db=gene&term=%s',
       'IPI' : 'http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-newId+[IPI-AllText:%s*]+-view+SwissEntry',
       'InterPro' : 'http://www.ebi.ac.uk/interpro/ISearch?query=%s',
       'PIR' : 'http://pir.georgetown.edu/cgi-bin/textsearch.pl?submit.x=0&submit.y=0&field0=ALL&search=1&query0=%s',
       'PIRSF' : 'http://pir.georgetown.edu/cgi-bin/ipcSF?id=%s',
       'PROSITE' : 'http://www.expasy.ch/prosite/%s',
       'Pfam' : 'http://pfam.sanger.ac.uk//family/%s',
       'SMART' : 'http://smart.embl-heidelberg.de/smart/do_annotation.pl?BLAST=DUMMY&DOMAIN=%s',
       'Uniprot/SPTREMBL' : 'http://www.uniprot.org/uniprot/%s',
       'Uniprot/SWISSPROT' : 'http://www.uniprot.org/uniprot/%s',
       'Uniprot/Varsplic' : 'http://www.uniprot.org/uniprot/%s',
       'HGNC_NAME' : 'http://www.genenames.org/data/hgnc_data.php?match=%s',
       'HGNC_ID' : 'http://www.genenames.org/data/hgnc_data.php?hgnc_id=%s',
       'HGNC' : 'http://www.genenames.org/data/hgnc_data.php?hgnc_id=%s',
       'RefSeq' : 'http://www.ncbi.nlm.nih.gov/protein/%s',
       'RefSeq_dna' : 'http://www.ncbi.nlm.nih.gov/nuccore/%s',
       'RefSeq_peptide' : 'http://www.ncbi.nlm.nih.gov/protein/%s',
       'CCDS' : 'http://www.ncbi.nlm.nih.gov/projects/CCDS/CcdsBrowse.cgi?REQUEST=ALLFIELDS&DATA=%s',
       'UniGene' : 'http://www.ncbi.nlm.nih.gov/UniGene/clust.cgi?ORG=%s&CID=%s',
       'UniSTS' : 'http://www.ncbi.nlm.nih.gov/genome/sts/sts.cgi?uid=%s',
       'PANTHER' : 'http://www.pantherdb.org/panther/family.do?clsAccession=%s',
       'protein_id' : 'http://www.ncbi.nlm.nih.gov/protein/%s',
       'HPRD' : 'http://www.hprd.org/resultsQuery?multiplefound=&prot_name=&external=Ref_seq&accession_id=&gene_symbol=&chromo_locus=&function=&ptm_type=&localization=&domain=&motif=&expression=&prot_start=&prot_end=&limit=0&mole_start=&mole_end=&disease=&query_submit=Search&hprd=%s',
       'PeptideAtlas' : 'https://db.systemsbiology.net/sbeams/cgi/PeptideAtlas/Search?action=GO&build_type_name=Any&all_fields=on&search_key=%s',
       'PDB' : 'http://www.rcsb.org/pdb/explore/explore.do?structureId=%s',
       'CDD' : 'http://www.ncbi.nlm.nih.gov/sites/entrez/query.fcgi?db=cdd&term=%s',
       'PRINTS' : 'http://www.bioinf.manchester.ac.uk/cgi-bin/dbbrowser/sprint/searchprintss.cgi?display_opts=Prints&category=None&queryform=false&prints_accn=%s',
       'PharmGKB' : 'http://www.pharmgkb.org/do/serve?objId=%s',
       'KEGG' : 'http://www.genome.jp/dbget-bin/www_bget?%s',
       'MIM' : 'http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=%s',
       'MIM_GENE' : 'http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=%s',
       'MIM_MORBID' : 'http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=%s',
       'PDBsum' : 'http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?template=main.html&EBI=TRUE&pdbcode=%s',
       'UCSC' : 'http://genome.ucsc.edu/cgi-bin/hgGene?hgg_prot=Q9HAU5&hgg_chrom=chr10&hgg_start=12002026&hgg_end=12124814&hgg_type=knownGene&db=hg18&hgg_gene=%s',
       'MEROPS' : 'http://merops.sanger.ac.uk/cgi-bin/make_frame_file?id=%s',
       'GI' : 'http://www.ncbi.nlm.nih.gov/protein/%s',
       'Internal' : '',
}
