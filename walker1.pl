#!/usr/bin/perl
use strict;
use warnings;
use feature qw(say);

sub print_file {
   my $file_path = $_[0];
   say $file_path;
}

sub check_path {
    if (-f) {
         print_file($File::Find::name);
    }
    ##To search only the directory
    #my $path = $File::Find::name;
    ##say $path;
    #PrintList($path)
}

use File::Find qw(find);
my $dir      = '.';
#my $pattern  = '.py';
#my $callback = sub { print "here", $File::Find::name, "\n" if /$pattern/ };
#find $callback, $dir;
find (\&check_path, "../IntroLab");


