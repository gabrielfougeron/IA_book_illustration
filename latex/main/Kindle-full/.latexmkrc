@default_files = ('main');


# Main command line options
# -pv  : run file previewer
# -pvc : run file previewer and continually recompile on change
# -C   : clean up by removing all regeneratable files


# add folder to tex visibility
# $set_environ_vars = 'TEXINPUTS=$(TEXINPUTS):"/path/to/new/folder/with/trailing/slash/" ';

# Common options for LaTeX engines
# $common_opts = '-shell-escape -synctex=1 -halt-on-error';
$common_opts = '-interaction=nonstopmode  -halt-on-error -file-line-error -shell-escape -synctex=1';

# specify previewer
# $pdf_previewer = 'start /mnt/c/Users/gfo/AppData/Local/SumatraPDF/SumatraPDF-3.3.3-64.exe %O %S';

$out_dir = 'build';

# Uncomment the following line to enable draft mode
#$pre_tex_code = '\PassOptionsToClass{draft}{beamer}';

$pdf_mode = 1;

# Command for pdflatex ($pdf_mode = 1)
# $pdflatex = "$set_environ_vars pdflatex $common_opts %O %P";

$pdflatex = 'internal musixlatex %R %O %S';
push @generated_exts,"mx2";
push @generated_exts,"mx1";

sub musixlatex {
   my $root = shift;
   # Define root filename for the mx1 and mx2 files
   # Note that $aux_dir1 includes directory separator
   #      and it equals $out_dir1 if only the out_dir is set.
   my $mx = "$aux_dir1$root";
   my @args = @_;
   if ( $pass{$rule} <= 1 ) { 
      print "======= FIRST PASS: Deleting '$mx.mx2' =======\n";
      unlink "$mx.mx2"; 
      print "====   Generating '$mx.mx1' then '$mx.mx2' ===\n";
      my $ret = system( "pdflatex $common_opts @args" );
      if ($ret) { return $ret; }
      $ret = system( "musixflx $mx" );
      if ($ret) { return $ret; }
   }
   return system( "pdflatex $common_opts @args" );
}


# Command for latex with dvipdf ($pdf_mode = 3)
$latex    = "$set_environ_vars uplatex $common_opts $jobname  %O %P";
$dvipdf   = "$set_environ_vars dvipdfmx %O -o %D %S";

# Command for lualatex ($pdf_mode = 4)
$lualatex = "$set_environ_vars lualatex $common_opts $jobname  %O %P";

# Command for xelatex ($pdf_mode = 5)
$xelatex = "$set_environ_vars xelatex $common_opts $jobname  %O %P";

# BibTeX
$bibtex = 'bibtex';

@generated_exts = ( 'aux', 'bcf', 'fls', 'idx', 'ind', 'lof', 'lot', 'out', 'toc', 'nav', 'snm', 'vrb', 'synctex.gz', 'mx1', 'mx2'  );

# Avoid wrapping lines of log output
$ENV{'max_print_line'} = '2147483647';
