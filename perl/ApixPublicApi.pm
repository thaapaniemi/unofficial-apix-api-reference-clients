package ApixPublicApi;

use strict;
use warnings;
use utf8;

use Time::Piece;
use HTML::Entities;
use HTTP::Request::Common;
use LWP::UserAgent;
use File::Basename;

use Encode;
use Digest::SHA qw(sha256_hex);

sub _calculate_sha256_digest {
    my (@params) = @_;
    my $str      = join("+", @params);
    my $digest   = sha256_hex($str);

    return "SHA-256:" . $digest;
}

sub _generate_url {
    my ($baseurl, $argshash) = @_;

    my @args = ();
    for my $key (keys %{$argshash}) {
        my $value = $argshash->{$key};
        push(@args, "${key}=${value}");
    }

    my $url = "${baseurl}?" . join("&", @args);

    return $url;
}

sub SendInvoiceZIP($$$$$$) {
    my ($url, $software_name, $software_version, $transfer_id, $transfer_key, $data) = @_;

    my $t         = gmtime;
    my $timestamp = $t->strftime("%Y%m%d%H%M%S");

    my %get_args = (
        "soft"  => $software_name,
        "ver"   => $software_version,
        "TraID" => $transfer_id,
        "t"     => $timestamp,
        "d"     => _calculate_sha256_digest($software_name, $software_version, $transfer_id, $timestamp, $transfer_key),
    );

    my $generated_url = _generate_url($url, \%get_args);

    my $req = HTTP::Request->new(PUT => $generated_url);
    $req->content_type('application/octet-stream');
    $req->content($data);

    $req->protocol('HTTP/1.1');
    my $ua = LWP::UserAgent->new;

    #server timeout is 60s
    $ua->timeout(120);

    my $response = $ua->request($req);

    my @xresponse = ($response->code, $response->content());
    return @xresponse;
}

1;
