<!DOCTYPE html>
<html>
    <head>

		<title>MNMP</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<link rel="icon" href="icon.png" type="image/png" />
        <link rel="apple-touch-icon" href="icon-apple.png"/>

        <style>
          h1 { font-size: 20px; color: white; }
          div { font-size: 20px; color: white; }

        </style>


	</head>
    <body style="background: #1F2127">

		<?php
			if (!mysql_connect('odroid-u3.local', 'monitor', 'test123'))
			{
				echo "Konnte nicht zu mysql verbinden: " . mysql_error() . "\n";
				exit;
			}

			mysql_select_db('monitor');
			mysql_set_charset('utf8');
			mysql_query("SET NAMES 'utf8'");
			date_default_timezone_set('UTC');

			$today = date("Ymd");
			$data = mysql_query("select * from data{$today}");
			$clusters = array();

			while ($dataset = mysql_fetch_row($data))
			{
				$clusters[$dataset[0]] = (int) $dataset[1];
			}

			arsort($clusters);
			foreach ($clusters as $name => $size)
			{
//				$URLname = str_replace("\"", "", iconv("utf-8", "ascii//IGNORE", $name));
                $URLname = urlencode(base64_encode($name));

                $diameter = sqrt($size) * 60;
				$radius = $diameter / 2;
				$TextSize = sqrt($size) * 10;
				$LineHeight = $radius * 2;

				$destination_url = "/search.php?q={$URLname}";

				$circle_view = "height: {$diameter}px;
						width: {$diameter}px;
						border-radius: {$radius}px;
						background-color: #7f007f;
						text-align: center;
						font-weight: bold;
						font-family: helvetica;
						color: white;
						margin: 30px;
						display: inline-block;
						line-height: {$LineHeight}px;
						font-size: {$TextSize}px;";

                $diameter_Num = sqrt($size) * 20;
                $radius_Num = $diameter_Num / 2;
                $TextSize_Num = sqrt($size) * 4;


                $circle_view_Num = "height: {$diameter_Num}px;
    				width: {$diameter_Num}px;
    				border-radius: {$radius_Num}px;
    				background-color: #7f007f;
    				text-align: center;
    				font-weight: bold;
    				font-family: helvetica;
    				color: white;
    				margin: 30px;
    				display: inline-block;
                    position: absolute;
    				line-height: {$diameter_Num}px;
    				font-size: {$TextSize_Num}px;";

				echo "\t\t<center>
          <a style=\"$circle_view\" href=\"{$destination_url}\">{$name}</a>
          <a style=\"$circle_view_Num\" href=\"{$destination_url}\">{$size}</a>
          </center>\n";

			}
		?>
    </body>
</html>
