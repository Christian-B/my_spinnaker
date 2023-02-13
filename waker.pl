#!/usr/bin/perl
use strict;
use warnings;
use feature qw(say);

sub PrintList {
   my $side = $_[0];
   say $side;
}

sub DoFind {
    #To search only the directory
    my $path = $File::Find::name;
    #say $path;
    PrintList($path)
}

use File::Find qw(find);
my $dir      = '.';
#my $pattern  = '.py';
#my $callback = sub { print "here", $File::Find::name, "\n" if /$pattern/ };
#find $callback, $dir;
find (\&DoFind, ".");


