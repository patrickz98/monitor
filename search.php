<?php

$search = $_GET['search'];

$link = mysql_connect('odroid-u3.local', 'monitor', 'test123');
mysql_select_db('monitor') or die('Could not select database');

$query = 'SELECT * FROM news20141006';
$result = mysql_query($query) or die('Query failed: ' . mysql_error());

while ($line = mysql_fetch_array($result)) 
{ 
	if (strpos($line['Headlines'], $search) !== false) 
	{
		echo "<p><a href=" . $line['link'] . ">" . $line['Headlines'] . " " . $line['Newspaper'] . "</a></p>\n";    
	}
}

mysql_free_result($result);
mysql_close($link);
?>

