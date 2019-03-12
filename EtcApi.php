<?php
$hostname = "www.mywebsite.com";
$port     = 50005;
$cmd      = "EtcApi";
$url      = "http://$hostname:$port/$cmd?".$_SERVER["QUERY_STRING"];
$fp = fopen($url, "rb");
fpassthru($fp);
?>
