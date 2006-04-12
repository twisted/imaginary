#!/usr/bin/perl

$i=0;

$prefx=$ARGV[0];

while (<STDIN>)
{
	$z[$i]=$_; $i++;
}

$max=$i;

print "$prefx-targets: ";

$i=0;
while($i<$max)
{
	$_=$z[$i++];
	my $x = '$(BINDIR)/';
	s/.java/.$prefx/g;
	s/\.\//$x/g;
	chop; print;
	print ' ';
}

print "\n\n$prefx-clean: ";

$i=0;
while ($i<$max)
{
	$_=$z[$i++];
	my $x = '$(BINDIR)/';
	$xxx=".$prefx-clean";
	s/.java/$xxx/g;
	s/\.\//$x/g;
	chop; print;
	print ' ';
}

print "\n\n";
