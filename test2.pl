#!/usr/bin/perl
use strict;
use warnings;

my $name = "test";
print "Hello, $name\n";     # works fine
print 'Hello, $name\n'; # prints $name\n literally
print "\n";

my $variables = {
    scalar  =>  {
                 description => "single item",
                 sigil => '$',
                },
    array   =>  {
                 description => "ordered list of items",
                 sigil => '@',
                },
    hash    =>  {
                 description => "key/value pairs",
                 sigil => '%',

                },
};

print "Scalars begin with a $variables->{'scalar'}->{'sigil'}\n";

open(my $in,  "<",  "input.txt")  or die "Can't open input.txt: $!";

use Cwd;
my $here = getcwd;
print $here;
print "\n";

#opendir my $dir, "/home/brenninc/spinnaker/my_spinnaker" or die "Cannot open directory: $!";
while (readdir $dir) {
    print "$_\n";
}
closedir $dir;

opendir(DIR,".") or die "Can't open the current directory: $!\n";
# read file/directory names in that directory into @names
my @names = readdir(DIR) or die "Unable to read current dir:$!\n";

foreach $name (@names) {
    next if ($name eq "."); # skip the current directory entry
    next if ($name eq ".."); # skip the parent directory entry
    if (-d $name){ # is this a directory?
        print "found a directory: $name\n";
        next; # can skip to the next name in the for loop }
    if ($name eq "core") { # is this a file named "core"?
        print "found one!\n";
        }
    }
}
closedir(DIR);

use File::Find qw(find);
my $dir      = '.';
my $pattern  = '.py';
my $callback = sub { print "here", $File::Find::name, "\n" if /$pattern/ };
find $callback, $dir;
