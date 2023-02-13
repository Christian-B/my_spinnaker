#!/usr/bin/perl
use strict;
use warnings;
use feature qw(say);

my $line;
my $path;
my $prefix;

#my $line = $top[0];
$path = "/home/brenninc/spinnaker/my_spinnaker/../IntroLab/learning/simple.py";

$line = '//! \copyright      &copy; The University of Manchester - 2012-2015';
#$line =~ s/copyright(.*)(\d{4})(.*)(\d{4})(.*)the university of manchester$/Copyright $2-2023 The University of Manchester/i;
#$line =~ s/copyright(\D*)(\d{4})(\D*)the university of manchester$/Copyright $2-2023 The University of Manchester/i;
#$line =~ s/(.*) 2023-2023(.*)/$1 2023$2/i;
say $line;
say $line !~ /copyright (.)*copy/i;
$line = '* Copyright 2020-2023 The University of Manchester';
say $line;
say $line !~ /copyright (.)*copy/i;
