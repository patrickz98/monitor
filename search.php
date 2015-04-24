<!doctype html>
<html>
	<head>
		<title>Finder</title>
		<link rel="icon" type="image/x-icon" href="../news.ico" />
		<link rel="apple-touch-icon" href="../news.png"/>

		<script src="../Chart.js"></script>
		<style type="text/css">
			a { font-family: helvetica; }
			a:link { text-decoration:none; color:#ffffff; }
			a:visited { text-decoration:none; color:#7f007f; }

      h1 {
				font-size: 50px;
				color: white;
				height: 150px;
				width: 150px;
				border-radius: 75px;
				background-color: #7f007f;
				text-align: center;
				font-weight: bold;
				font-family: helvetica;
				display: inline-block;
				line-height: 150px;
			}

			h2 { font-family: helvetica; font-size: 30px; color: white; }
			h3 { font-family: helvetica; font-size: 20px; color: white; }

      div { font-family: helvetica; font-size: 20px; color: white; }

			hr {
				border: 0;
				height: 5px;
				background-image: -webkit-linear-gradient(left, rgba(127,0,127,1), rgba(127,0,127,0.75), rgba(127,0,127,0));
				background-image:    -moz-linear-gradient(left, rgba(127,0,127,1), rgba(127,0,127,0.75), rgba(127,0,127,0));
				background-image:     -ms-linear-gradient(left, rgba(127,0,127,1), rgba(127,0,127,0.75), rgba(127,0,127,0));
				background-image:      -o-linear-gradient(left, rgba(127,0,127,1), rgba(127,0,127,0.75), rgba(127,0,127,0));
			}


		</style>

	</head>
	<body style="background: #1F2127">

		<?php

			$search = $_GET["q"];
			$dbname = 'monitor';

			date_default_timezone_set('UTC');

			$todate = date("Ymd");

			if (!mysql_connect('odroid-u3.local', 'monitor', 'test123'))
			{
			    echo 'Konnte nicht zu mysql verbinden';
			    exit;
			}

			echo "\t<h1>" . $search . "</h1>\n";

			$tabels = mysql_query("SHOW TABLES FROM $dbname");
			$traffic_tabels = array();
			$traffic = array();

			while($row = mysql_fetch_array($tabels))
			{
				if (strpos($row[0], "data") !== false)
				{
					$traffic_tabels[] = $row[0];
				}
			}

			foreach ($traffic_tabels as $bla)
			{
				$tmp = mysql_query("SELECT * FROM" . " $dbname.{$bla}");

				while($row = mysql_fetch_array($tmp))
				{
					if (strval($row[0]) == strval($search))
					{
						$traffic[(String) substr($bla, 4)] = $row[1];
					}
				}
			}

			if (sizeof($traffic) >= 4)
			{
				echo "\t<div style=\"width:100%\">\n";
				echo "\t\t<canvas id=\"Euro\" height=\"450\" width=\"600\"></canvas>\n";
				echo "\t</div>\n";

				echo "\t<script>\n";
				echo "\t\tvar lineChartDataEuro = {\n";
				echo "\t\t\tlabels : [";

				foreach ($traffic as $date => $size) { echo "'$date', ";}

				echo "],\n";
				echo "\t\t\tdatasets : [{\n";
				echo "\t\t\tlabel: \"{$search}\",\n";
				echo "\t\t\tfillColor : \"rgba(127, 0, 127, 0.2)\",\n" .
							"\t\t\tstrokeColor : \"rgba(127, 0, 127, 1)\",\n" .
							"\t\t\tpointColor : \"rgba(127, 0, 127, 1)\",\n" .
							"\t\t\tpointStrokeColor : \"#fff\",\n" .
							"\t\t\tpointHighlightFill : \"#fff\",\n" .
							"\t\t\tpointHighlightStroke : \"rgba(127, 0, 127, 1)\",\n" .
							"\t\t\tdata : [";

							foreach ($traffic as $date => $size) { echo "'$size', ";}

				echo "]\n\t\t}]\n\t}\n";

				echo
				"\t\twindow.onload = function(){\n" .
				"\t\t\tvar ctx{$search} = document.getElementById(\"{$search}\").getContext(\"2d\");\n" .
				"\t\t\twindow.myLine{$search} = new Chart(ctx{$search}).Line(lineChartData{$search}, {\n" .
				"\t\t\tresponsive: true, animation: true });\n" .
				"\t\t}\n" .
				"\t</script>\n";

			}


			echo "\t\t<h2>Heute:</h2>\n";

			$Headlines_today = mysql_query("SELECT * FROM" . " $dbname.news{$todate}");

			while ($line = mysql_fetch_array($Headlines_today))
			{

				//
				// check if q-word is in Headlines row
				//

				if (strpos($line['Headlines'], $search) !== false)
				{
					echo "\t\t<p style=\"font-size:20px;\"><a href="
					. $line['link'] . " target='_blank'>" . $line['Headlines'] . " "
					. "(" . $line['Newspaper'] . ")"
					. "</a></p>\n";
				}
			}

			mysql_free_result($Headlines_today);

			$all_rows = array();

			while($row = mysql_fetch_array($tabels))
			{
				if (strpos($row[0], "news") !== false && substr($row[0], 4) !== date("Ymd"))
				{
					$all_rows[] = $row[0];
				}
			}

			$all_rows = array_reverse($all_rows);

			foreach ($all_rows as $news)
			{
					echo "<h3>"
					. substr($news, -2) . "."
					. substr($news, 8, -2) . "."
					. substr($news, 4, -4)
					. "</h3>\n";

					$query2 = "SELECT * FROM" . " $dbname.{$news}";
					$result2 = mysql_query($query2);

					while ($line = mysql_fetch_array($result2))
					{
						if (strpos($line['Headlines'], $search) !== false)
						{
							echo "\t\t<p style=\"font-size:20px;\"><a href="
							. $line['link'] . " target='_blank'>" . $line['Headlines'] . " "
							. "(" . $line['Newspaper'] . ")"
							. "</a></p>\n";
						}
					}
				}
				mysql_free_result($tabels);
			?>
	</body>
</html>
