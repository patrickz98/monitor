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

		echo "\t\t<h1>" . $search . "</h1>\n";

		$link = mysql_connect('odroid-u3.local', 'monitor', 'test123');
		mysql_select_db('monitor');
		
		while ($data = mysql_fetch_row(mysql_query("SHOW TABLES FROM monitor")))
		{
			if (strpos($data, "news") !== false)
			{
				$query = "SELECT * FROM" . " news" . $date;
				$result = mysql_query($query);

				while ($line = mysql_fetch_array($result)) 
				{
					if (strpos($line['Headlines'], $search) !== false) 
					{
						echo "\t\t<p style=\"font-size:18px;\"><a href=" 
						. $line['link'] . ">" . $line['Headlines'] . " " 
						. $line['Newspaper'] 
						. "</a></p>\n";    
					}
				}
			}
		}
		mysql_free_result($result);
		mysql_close($link);
	?>

	</body>
</html>
