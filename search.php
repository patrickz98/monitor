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
	$dbname = 'monitor';

	echo "\t\t<h1>" . $search . "</h1>\n";

	if (!mysql_connect('odroid-u3.local', 'monitor', 'test123')) 
	{
	    echo 'Konnte nicht zu mysql verbinden';
	    exit;
	}

	$sql = "SHOW TABLES FROM $dbname";
	$result = mysql_query($sql);

	if (!$result) 
	{
	    echo "DB Fehler, konnte Tabellen nicht auflisten\n";
	    echo 'MySQL Fehler: ' . mysql_error();
	    exit;
	}

	while ($row = mysql_fetch_row($result)) 
	{
		if (strpos($row[0], "news") !== false) 
		{
				echo "Tabelle: {$row[0]}\n";		
				$query2 = "SELECT * FROM" . " $dbname.{$row[0]}";
				$result2 = mysql_query($query2);

				while ($line = mysql_fetch_array($result2)) 
				{
					if (strpos($line['Headlines'], $search) !== false) 
					{
						echo "\t\t<p style=\"font-size:18px;\"><a href=" 
						. $line['link'] . ">" . $line['Headlines'] . " " 
						. $line['Newspaper'] 
						. "</a></p>\n";  
					}
				}

				mysql_free_result($result2);

			}
		}

		mysql_free_result($result);
	?>

	</body>
</html>
