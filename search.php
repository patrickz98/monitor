<!doctype html>
<html>
	<head>
		<title>Finder</title>
		<link rel="icon" type="image/x-icon" href="../news.ico" />
		<link rel="apple-touch-icon" href="../news.png"/>

		<script src="../Chart.js"></script>
		<style type="text/css">
			a:link { text-decoration:none; color:#000000; }
			a:visited { text-decoration:none; color:#0063b0; }

		</style>

	</head>
	<body>

<?php

$search = $_GET['search'];

$link = mysql_connect('odroid-u3.local', 'monitor', 'test123');
mysql_select_db('monitor') or die('Could not select database');

$query = 'SELECT * FROM news20141006';
$result = mysql_query($query) or die('Query failed: ' . mysql_error());

echo "<h1>" . $search . "</h1>\n";

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
	</body>
</html>
