#!/usr/bin/perl
use strict;
use warnings;
use feature qw(say);
use File::Find qw(find);
use File::Basename;
use File::Spec;

my @ignore_dirs = (
    '/.git/',
    '/.idea/',
    '/doc/build/',
    '/support/',
    '/dist/',
    '\.egg-info/',
    '.coverage',
    '\.ratexclude',
    'project$',
    '.travis.yml$',
    '/modified_src/',
    '/.settings/',
    'cache/',
    '/MANIFEST.in$',
    '/pypi_to_import$',
    );

my %ignore_suffix = (
    '' => 'weird file',
    '.cfg' => 'Config file',
    '.csv' => 'Comman seperated file',
    #dict => 'assumed dictionary',
    #'.ddl' => 'data definition language file',
    '.dll' => 'Dynamic Link Library',
    '.exe' => '"Excutable',
    '.log' => "log file",
    '.md' => 'markdown',
,   '.pyc' => 'Compliled Python',
    '.png' => 'Portable Network Graphic',
    '.rst' => 'reStructuredText markup',
    '.template' => 'cfg template',
    '.ipynb' => 'Jupyter Notebook file'
);

my %check_suffix = (
    '.py' => '"python',
    '.yml' => 'Aint Markup Language'
);

sub print_file {
   my $file_path = $_[0];
   say $file_path;
}

sub check_path {
    if (-d) {
        return;
    }
    my $path = $File::Find::name;
    foreach my $pattern (@ignore_dirs){
        if ($path =~ $pattern) {
            return;
        }
    }
    # say $path;
    (my $n, my $p, my $s) = fileparse($path,qr"\..[^.]*$");
    if (exists $ignore_suffix{$s}){
        return;
    }
    if (exists $check_suffix{$s}){
        return;
    }

    if ($n eq ''){
        return;
    }

    say $n, "   ", $s;
    #my ($ext) = $path =~ /(\.[^.]+)$/;
    #say $ext
    #print_file($path);
}

sub check_apache{
    if (-d) {
        return;
    }
    my $full_path = $File::Find::name;
    open(FILE, $full_path) or die "Can't open: $full_path!\n";
    if (grep{/Apache/} <FILE>){
       say "found", $full_path
    #}else{
    #   say "NO", $full_path
    }
    close FILE;

}
my $rel_path = "../IntroLab";
my $abs_path = File::Spec->rel2abs( $rel_path ) ;

find (\&check_apache, $abs_path);
#find (\&check_path, "temp");
say $abs_path



