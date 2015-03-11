<!DOCTYPE html>
<html>
    <head>
	
		<title>Monitor</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<link rel="icon" href="icon.png" type="image/png" />
<!-- 
		 <meta http-equiv="refresh" content="1" > 
 -->
	</head>
	<body>
		<?php

			function shuffle_assoc($array)
			{
				$shuffled_array = array();

				$shuffled_keys = array_keys($array);
				shuffle($shuffled_keys);


				foreach ( $shuffled_keys AS $shuffled_key )
				{
					$shuffled_array[  $shuffled_key  ] = $array[  $shuffled_key  ];
				}
			
				return $shuffled_array;
			}

			
			if (!mysql_connect('odroid-u3.local', 'monitor', 'test123')) 
			{
				echo "Konnte nicht zu mysql verbinden: " . mysql_error() . "\n";
				exit;
			}

			mysql_select_db('monitor');
			mysql_set_charset('utf8');
			mysql_query("SET NAMES 'utf8'");

// 			$dbname = 'monitor';
// 			$sql = "SHOW TABLES FROM $dbname";
// 			$result = mysql_query($sql);
// 
// 			while ($row = mysql_fetch_row($result)) 
// 			{
// 				if (strpos($row[0], "data") !== false) 
// 				{
// 					echo $row[0] . "\n";
// 				}
// 			}
// 	
// 			mysql_free_result($result);
// 	
			date_default_timezone_set('UTC');
			
			$toDate = date("Ymd");
			$data = mysql_query("select * from data{$toDate}");
			$clusters = array();
			
			while ($dataset = mysql_fetch_row($data))
			{
				$clusters[$dataset[0]] = (int) $dataset[1];
			}
			
			$new_a = shuffle_assoc($clusters);

			foreach ($new_a as $name => $size)
			{
// 				$URLname = $name;
// 				if (strpos($URLname, "ß") !== false)
// 				{
// 					$URLname = str_replace("ß", "ss", $URLname);
// 				}
				
				$URLname = str_replace("\"", "", iconv("utf-8", "ascii//IGNORE", $name));

				$rand = $size * 15;
				$rand2 = $rand / 2;
				$TextSize = $size * 3;
				$LineHeight = $rand2 * 2;
				$url = "http://patrickz.no-ip.org/
					html/" . 
					$URLname . 
					".html";

				$opt = "height: {$rand}px;
						width: {$rand}px;
						border-radius: {$rand2}px;
						background-color: #F59B00;
						text-align: center;
						font-weight: bold;
						font-family: sans-serif;
						color: black;
						margin: 30px;
						display: inline-block;
						line-height: {$LineHeight}px;
						font-size: {$TextSize}px;";

				echo "\t\t<a style=\"$opt\" href=\"{$url}\"><div style=\"font-family:'Helvetica',Times,serif\">{$name}</div></a>\n";

			}
		?>
    </body>
</html>
