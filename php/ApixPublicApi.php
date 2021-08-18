#!/bin/php
<?php

function get_digest(){
    $arg_list = func_get_args();
    $digest_str = implode("+",$arg_list);
    return hash("sha256", $digest_str);
}

/* Send invoice file to Apix REST API"""

    # needed params:
    # endpoint (https://test-api.apix.fi/invoices, https://api.apix.fi/invoices)
    # transfer_id
    # transfer_key
    # software_name
    # software_version
    # invoice_data

    Returns (HTTP Status Code, API response)
*/
function SendInvoiceZIP($endpoint, $transfer_id, $transfer_key, $software_name, $software_version, $invoice_data){

    $timestamp=gmdate("YmdHis");
    $digest = "SHA-256:" . get_digest($software_name, $software_version, $transfer_id, $timestamp, $transfer_key);
    
    $args = http_build_query(
        array(
            "soft" => $software_name,
            "ver" => $software_version,
            "TraID" => $transfer_id,
            "t" => $timestamp,
            "d" => $digest,
        )
    );

    $opts = array("http" =>
        array(
            "method"  => "PUT",
            "header"  => "Content-Type: application/octet-stream",
            "content" => $invoice_data,
            "ignore_errors" => true,
        )
    );

    $url = "$endpoint?$args";

    $context  = stream_context_create($opts);
    $result = file_get_contents($url, false, $context);

    #var_dump($http_response_header);
    $hdrs = array('HTTP/1.1 400 Bad request');
    !empty($htp_response_header) && $hdrs = $http_response_headers;

    $status_line = $http_response_header[0];
    preg_match('{HTTP\/\S*\s(\d{3})}', $status_line, $match);
    $status_code = $match[1];

    return array($status_code, $result);
}


?>