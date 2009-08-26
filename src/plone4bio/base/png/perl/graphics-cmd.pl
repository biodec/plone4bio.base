#!/usr/bin/perl

use strict;
use Bio::SeqIO;
use graphics;

my $file = shift                       or die "provide a sequence file as the argument";
my $io = Bio::SeqIO->new(-file=>$file, -format=>"genbank") or die "could not create Bio::SeqIO";
my $seq = $io->next_seq                or die "could not find a sequence in the file";

printSeqRecord($seq);
