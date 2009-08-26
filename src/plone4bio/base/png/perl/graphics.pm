#!/usr/bin/perl
#
# Dalla reference di Bio::Graphics::panel
#
# scripts/render_panel-ref.pl inputs/my_file.gb | display -
#
#
# This script parses a GenBank or EMBL file named on the command
# line and produces a PNG rendering of it.

use strict;
# use lib "../perl/lib/perl5/site_perl/";
use Bio::Graphics;
use Bio::SeqIO;
use Bio::Seq;


my %colors = (
      Tmhmm => "lightcoral",
      TRANSMEM => "lightcoral",
      TOPO_DOM => "pink",
      Seg => "moccasin",
      Superfamily => "darkseagreen",
      Prints => "purple",
      Pfam => "peru",
      ncoils => "lightsteelblue",
      CDS => "burlywood",
      Signalp => "gold",
      SIGNAL => "gold",
      sig_peptide => "gold",
      Protein => "antiquewhite",
      Region => "orange",
      VARIANT => "yellow",
      misc_feature => "palevioletred",
      CHAIN => "plum",
      COILED => "lightsteelblue",
      source => "lightsalmon",
      Profile => "khaki",
      Prosite_pattern => "khaki",
      PROSITE => "khaki",
      Prosite => "khaki",
      COMPBIAS => "Lavender",
      CONFLICT => "yellow",
      DNA_BIND => "lime",
      Smart => "green",
      STS => "lightskyblue",
      Site => "greenyellow",
      DOMAIN => "cornflowerblue",
      VAR_SEQ => "yellow",
      REPEAT => "mintcream",
      TIGRFAM => "palegoldenrod",
      TRANSIT => "gold",
      transit_peptide => "gold",
      mat_peptide => "aquamarine", 
      PIRSF => "chartreuse",
      proprotein => "crimson",
);

my %bumps = (
      Tmhmm => 0,
      Seg => 1,
      Superfamily => 1,
      Prints => 1,
      Pfam => 1,
      ncoils => 0,
      Profile => 1,
      Superfamily => 1,
      Prosite_pattern => 1,
      PROSITE => 1,
      Prosite => 1,
      Smart => 1,
      Site => 1,
      STS => 1,
      DOMAIN => 1,
      REPEAT => 1,
      TIGRFAM => 1,
      PIRSF => 1,
);

my %descriptions = (
      Tmhmm => 0,
      TOPO_DOM => \&description,
      Seg => \&hit_id_description,
      Superfamily => \&hit_id_description,
      Prints => \&hit_id_description,
      Pfam => \&hit_id_description,
      ncoils => 0,
      Region => \&hit_id_description,
      VARIANT => \&hit_id_description,
      misc_feature => \&note_description,
      Protein =>  \&note_description,
      Region => \&note_description,
      CDS => \&ft_gene_description,
      source => \&source_map_description,
      VARIANT => \&description,     
      CHAIN => \&description,
      Profile => \&hit_id_description,
      Prosite_pattern => \&hit_id_description, 
      PROSITE => \&hit_id_description, 
      Prosite => \&hit_id_description, 
      COMPBIAS => \&description,
      CONFLICT => \&description,
      DNA_BIND => \&description,
      Smart => \&hit_id_description,
      STS => \&ft_gene_description,
      Site => \&note_description,
      DOMAIN => \&description,
      VAR_SEQ => \&description,
      REPEAT => \&description,
      TIGRFAM => \&hit_id_description,
      mat_peptide => \&note_description,
      PIRSF => \&hit_id_description,
      proprotein => \&note_description,
);

my %glyphs = (
      STS => "primers",
      DISULFID => "anchored_arrow",
      VARIANT => "pinsertion",
      CONFLICT => "pinsertion",
      VAR_SEQ => "pinsertion",
);

sub printSeqRecord {
    my $seq = shift;
    my $req = shift;
    my @features = $seq->all_SeqFeatures;

    # sort features by their primary tags
    my %sorted_features;
    for my $f (@features) {
      my $tag = $f->primary_tag;
      my @notes = eval{$f->get_tag_values("ft_accession")};
      my $ft_accession = $notes[0];
      push @{$sorted_features{"$tag ($ft_accession)"}},$f;
    }

    # my %decription_glob;
    my $pad_left = 100;
    my $panel = Bio::Graphics::Panel->new(
                                     -length    => $seq->length,
				      -key_style => 'left',
				      -width     => 1000,
				      -pad_left  => $pad_left,
				      -pad_right  => 250,
				      #-key_font  => 'gdSmallFont',
				      -key_font  => 'gdMediumBoldFont',
		    		      -key_color => '#ECECEC',
		    		      -key_spacing => 1,
				      -empty_track_style => 'line',
				      -fgcolor   => 'gray',
				      -grid      => 1,
				      -gridcolor => '#ECECEC',
			
				      );
    #$panel->add_track(generic => Bio::SeqFeature::Generic->new(-start=>1,
    #							  -end=>$seq->length),
    #		  -glyph  => 'generic',
    #		  -bgcolor => 'blue',
    #		  -label  => 1,
    #		 );
    my $idx    = 0;
    my $curtag = '';
    my $counter = 100;
    for my $key (sort keys %sorted_features) {
      my $features = $sorted_features{$key};
      my $tag = $features->[0]->primary_tag;
      if (not $curtag eq $tag and $counter > 99)  {
        $panel->add_track( arrow => Bio::SeqFeature::Generic->new(-start=>1,
                                                          -end=>$seq->length),
		  -bump => 0,
		  -double=>1,
		  -bgcolor  => 'yellow',
		  -tick => 2,
		  -fgcolor  => 'grey',
		  -fontcolor => 'grey',
		  -font2color => 'grey');
        $counter = 0;
      }
      my $color = $colors{$tag};
      my $glyph = $glyphs{$tag};
      $panel->add_track($features,
		    -glyph    =>  $glyph,
		    #-bgcolor  =>  $colors[$idx++ % @colors],
		    -bgcolor  =>  $color,
		    -fgcolor  => 'grey',
 		    -connector   => 'dashed',
		    -font2color => 'grey',
		    -key      => "${key}",
		    -key_color => "red",
		    -bump     => $bumps{$tag},
		    -height   => 8,
		    #-description    => \&gene_description,
		    -description    => $descriptions{$tag},
		    -label    => 0,
		   );
      $curtag= $tag;
      $counter = $counter + length(@$features);
    }
    $panel->add_track( arrow => Bio::SeqFeature::Generic->new(-start=>1,
                                                          -end=>$seq->length),
                                                          -bump => 0,
                                                          -double=>1,
                                                          -tick => 2,
							  -fgcolor  => 'grey',
							  -fontcolor => 'grey',
							  -font2color => 'grey',
							);
    if ($req eq 'imagemap') {
      #     $name        The feature's name (display name)
      #     $id          The feature's id (eg, PK from a database)
      #     $class       The feature's class (group class)
      #     $method      The feature's method (same as primary tag)
      #     $source      The feature's source
      #     $ref         The name of the sequence segment (chromosome, contig)
      #                     on which this feature is located
      #     $description The feature's description (notes)
      #     $start       The start position of this feature, relative to $ref
      #     $end         The end position of this feature, relative to $ref
      #     $segstart    The left end of $ref displayed in the detailed view
      #     $segend      The right end of $ref displayed in the detailed view
      # print $cgi->header("text/html");
      # print $panel->create_web_map("imagemap", "a", "b", "c");
      # my $self     = shift;
      # my ($name,$linkrule,$titlerule,$targetrule) = @_;
      my $name = 'graphicsmap';
      my $boxes    = $panel->boxes;
      # my (%track2link,%track2title,%track2target);
      my $map = qq(<map name="$name" id="$name">\n);
      foreach (@$boxes){
        my ($feature,$left,$top,$right,$bottom,$track) = @$_;
        my $start = $feature->start - 1;
        my $end = $feature->end;
        my $tag = eval {$feature->method} || $feature->primary_tag;
        # my $description = $track->option('title');
        # my $description = $panel->make_title($feature);
        $left += $pad_left;
        $right += $pad_left;
        next unless $tag;
        $map .= qq(<area class="tips" shape="rect" coords="$left,$top,$right,$bottom" href="#" rel="#${tag}X${start}X${end}" title="$tag $start $end" alt="" />\n);
      }
  
      $map .= "</map>\n";
      print $map;
      $panel->finished;
    }
    else {
      # print $cgi->header("image/png");
      print $panel->png;
      $panel->finished;
    }
}

1;



sub gene_description {
  use vars qw(%description_glob);
  my $feature = shift;
  my @notes = eval{$feature->get_tag_values("ft_accession")};
  my $ft_accession = $notes[0];
  my $tag = $feature->primary_tag;
  my $key = $tag . "#" . $ft_accession;
  return " " if (exists ($description_glob{$key}));
  $description_glob{$key}=1;
  $ft_accession;
}

sub generic_description {
  my $feature = shift;
  my $description;
  foreach ($feature->get_all_tags) {
    my @values = $feature->get_tag_values($_);
   $description .= $_ eq 'note' ? "@values" : "$_=@values; ";
  }
  $description =~ s/; $//; # get rid of last
  $description;
}

sub hit_id_description {
  my $feature = shift;
  my @notes;
  foreach (qw(hit_id)) {
    @notes = eval{$feature->get_tag_values($_)};
    last;
  }
  return unless @notes;
  substr($notes[0],30) = '...' if length $notes[0] > 30;
  $notes[0];
}

sub note_description {
  my $feature = shift;
  my @notes1; 
  my @notes2; 
  my @notes3; 
  foreach (qw(note)) {
    @notes1 = eval{$feature->get_tag_values($_)};
    last;
  }
  foreach (qw(product)) {
    @notes2 = eval{$feature->get_tag_values($_)};
    last;
  }
  foreach (qw(site_type)) {
    @notes3 = eval{$feature->get_tag_values($_)};
    last;
  }
  my $note = $notes1[0] . $notes2[0] . $notes3[0];
  return unless $note;
  substr($note,120) = '...' if length $note > 120;
  $note;
}


sub ft_gene_description {
 my $feature = shift;
  my @notes1;
  my @notes2;
  foreach (qw(gene)) {
    @notes1 = eval{$feature->get_tag_values($_)};
    last;
  }
  foreach (qw(standard_name)) {
    @notes2 = eval{$feature->get_tag_values($_)};
    last;
  }
  my $note1 = '';
  my $note2 = '';
  my $note1 = 'gene: '.$notes1[0] if  length $notes1[0] > 1;   
  my $note2 = 'st_name: '.$notes2[0] if  length $notes2[0] > 1;   
  my $note = $note1 . " " . $note2;
  return unless $note;
  substr($note,120) = '...' if length $note > 120;
  $note;
}

sub source_map_description {
 my $feature = shift;
  my @notes1;
  my @notes2;
  foreach (qw(map)) {
    @notes1 = eval{$feature->get_tag_values($_)};
    last;
  }
  foreach (qw(ft_source)) {
    @notes2 = eval{$feature->get_tag_values($_)};
    last;
  }
  my $note1 = '';
  my $note1 = 'chromosome_map: '.$notes1[0] if  length $notes1[0] > 1;
  my $note2 = $notes2[0];
  my $note = $note1 . " " . $note2;
  return unless $note;
  substr($note,120) = '...' if length $note > 120;
  $note;
}

sub description {
 my $feature = shift;
  my @notes;
  foreach (qw(ft_description)) {
    @notes = eval{$feature->get_tag_values($_)};
    last;
  }
  return unless @notes;
  substr($notes[0],40) = '...' if length $notes[0] > 40;
  $notes[0];
}


