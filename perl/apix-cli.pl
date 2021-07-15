#! /bin/env perl

use strict;
use warnings;
use utf8;

# ugly way to import
use lib "./";
use ApixPublicApi;

use Getopt::Std;
use Getopt::Long;

#for Getopt
our %CMDARGS = ();

GetOptions(
    "help|h"               => \&getopt_handler,
    "software_name|s=s"    => \&getopt_handler,
    "software_version|v=s" => \&getopt_handler,
    "transfer_id|i=s"      => \&getopt_handler,
    "transfer_key|k=s"     => \&getopt_handler,
    "file|f=s"             => \&getopt_handler,
    "endpoint|u=s"         => \&getopt_handler,
    "environment|e=s"      => \&getopt_handler,
);

############### __main__ ###############

check_help() or exit(1);

eval { main(); };
if ($@) {
    die($@);
}

sub main {

    my $data = "";
    open(my $fh, "<", $main::CMDARGS{"file"}) or die(sprintf("Error opening %s: %s", $main::CMDARGS{"file"}, $!));
    while (<$fh>) {
        $data .= $_;
    }
    close($fh);

    my $url = undef;
    if ($main::CMDARGS{"endpoint"}) {
        $url = $main::CMDARGS{"endpoint"};
    } else {
        if ($main::CMDARGS{"environment"} eq "prod") {
            $url = "https://api.apix.fi/invoices";
        } elsif ($main::CMDARGS{"environment"} eq "test") {
            $url = "https://test-api.apix.fi/invoices";
        }
    }

    my ($code, $response) = ApixPublicApi::SendInvoiceZIP($url, $main::CMDARGS{"software_name"}, $main::CMDARGS{"software_version"}, $main::CMDARGS{"transfer_id"}, $main::CMDARGS{"transfer_key"}, $data);

    if ($code != 200) {
        die("Unknown HTTP error: [${code}] ${response}\n");
    }

    # This is quick-and-dirty solution, real solution would be a use xml parser to get data
    if ($response =~ /<Status>OK<\/Status>/) {
        print "Invoice sent successfully:\n${response}\n";
        exit(0);
    } else {
        print "Invoice was rejected (attach api response for possible questions for Apix):\n${response}\n";
        exit(1);
    }

}

sub check_help {

    my $show_help = 0;

    if (defined($main::CMDARGS{"help"})) {
        $show_help = 1;
    }

    my @required = ("software_name", "software_version", "transfer_id", "transfer_key", "file");
    for my $key (@required) {
        if (!defined($main::CMDARGS{$key})) {
            print STDERR "required argument is missing: $key .\n";
            $show_help = 1;
        }
    }

    if (!defined($main::CMDARGS{"endpoint"}) and !defined($main::CMDARGS{"environment"})) {
        print STDERR "required argument is missing: endpoint OR environment.\n";
        $show_help = 1;
    }

    if (defined($main::CMDARGS{"endpoint"}) and defined($main::CMDARGS{"environment"})) {
        print STDERR "Use only either -endpoint or -environment argument.\n";
        $show_help = 1;
    }

    if (defined($main::CMDARGS{"environment"})) {
        if ($main::CMDARGS{"environment"} !~ /^(test|prod)$/) {
            print STDERR "Allowed arguments for environment is test or prod.\n";
            $show_help = 1;
        }
    }

    if ($main::CMDARGS{"file"} and !-e $main::CMDARGS{"file"}) {
        printf STDERR "File '%s' is missing from path.\n", $main::CMDARGS{"file"};
        $show_help = 1;
    }

    if ($show_help) {
        print STDERR "Usage: $0 -software_name <software_name> -software_version <software_version> -transfer_id <transfer_id> -transfer_key <transfer_key> -file <file> (-endpoint <url> OR -environment <test/prod>\n";
        exit(1);
    }

    return 1;
}

sub getopt_handler {
    my ($opt_name, $opt_value) = @_;
    $main::CMDARGS{$opt_name} = $opt_value;
}

