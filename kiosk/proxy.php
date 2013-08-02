<?php
// File Name: proxy.php
$url = 'http://10.4.32.57:8000/' . $_GET['id']. '/' . (isset($_GET['type']) ? $_GET['type'] : '');
echo file_get_contents($url);
?>