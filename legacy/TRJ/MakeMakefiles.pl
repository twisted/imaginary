#!/usr/bin/perl
$tablevel=-1;
mkmf(".");

sub tab()
{
	for ($zz=0;$zz<$tablevel;$zz++)
	{
		print " ";
	}
}

sub mkmf()
{
	$tablevel++;
	my $tmpdot=$dotdot;
	if ($tablevel > 0)
	{$dotdot="../$dotdot";}
	my $xyz=shift;
	my $mfnm="$xyz/Makefile";
	$mfdot="Makefile.dot";
	my $cmd="ln -s $dotdot$mfdot $mfnm";
	if ( -e $mfnm )
	{
		tab();
		print ("NERT!!!!!! ($mfnm already exists)\n");
	}
	else
	{
		tab(); print "$cmd\n"; print `rm -f $mfnm; $cmd`;
	}
	my @drlist=split(/\/\n/,`ls $xyz -p | grep /`);
	my $i=0;
	my $xxx;
	while($xxx=$drlist[$i++])
	{
		my $newxyz="$xyz/$xxx";
		&mkmf($newxyz);
	}
	my $xyxy=$dirlist[$i];
	
	$tablevel--;
	$dotdot=$tmpdot;
}
