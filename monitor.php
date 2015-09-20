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

			$toDate = date("Ymd");
			$data = mysql_query("select * from data{$toDate}");
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

        $rand = $size * 15;
				$rand2 = $rand / 2;
				$TextSize = $size * 3;
				$LineHeight = $rand2 * 2;

				$url = "/search.php?q={$URLname}";

				$opt = "height: {$rand}px;
						width: {$rand}px;
						border-radius: {$rand2}px;
						background-color: #7f007f;
						text-align: center;
						font-weight: bold;
						font-family: helvetica;
						color: white;
						margin: 30px;
						display: inline-block;
						line-height: {$LineHeight}px;
						font-size: {$TextSize}px;";

        $randNUM = $size * 3;
        $rand2NUM = $randNUM / 2;
        $TextSizeNUM = $size * 1.5;


        $optNUM = "height: {$randNUM}px;
    				width: {$randNUM}px;
    				border-radius: {$rand2NUM}px;
    				background-color: #7f007f;
    				text-align: center;
						font-weight: bold;
    				font-family: helvetica;
    				color: white;
    				margin: 30px;
    				display: inline-block;
            position: absolute;
    				line-height: {$randNUM}px;
    				font-size: {$TextSizeNUM}px;";

				echo "\t\t<center>
          <a style=\"$opt\" href=\"{$url}\">{$name}</a>
          <a style=\"$optNUM\" href=\"{$url}\">{$size}</a>
          </center>\n";

			}
		?>
    </body>
</html>
