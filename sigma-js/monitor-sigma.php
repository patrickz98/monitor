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

    $end = array();
    $end["nodes"] = array();
    $end["edges"] = array();

	$today = date("Ymd");
	$data = mysql_query("select * from data{$today}");
    $news = mysql_query("select * from news{$today}");
    $headlines = array();
	$clusters = array();

	while ($dataset = mysql_fetch_row($data))
	{
		$clusters[$dataset[0]] = (int) $dataset[1];
	}

    while ($lines = mysql_fetch_row($news))
	{
		array_push($headlines, $lines[0]);
	}

	arsort($clusters);
    $bla = 0;

    foreach ($clusters as $name => $name_count)
    {
        $tmp = array();

        $tmp["id"] = utf8_decode(utf8_encode($name));
        $tmp["label"] = $name;
        $tmp["x"] = $bla;
        $tmp["y"] = rand(0,100);
        $tmp["size"] = $name_count;

        array_push($end["nodes"], $tmp);
        $bla = $bla + 1;
    }

    // echo "<h1>" . count($end["nodes"]) . "</h1>";

    $tmp = array();
    foreach ($clusters as $name => $name_count)
    {
        $tmp[$name] = array();

        foreach ($headlines as $line)
        {
            if (strpos($line, $name) !== false)
            {
                foreach ($clusters as $name_2 => $name_count_2)
                {
                    if (strpos($line, $name_2) !== false && $name_2 != $name)
                    {
                        if (!$tmp[$name]["id"] == $name . "++" . $name_2 && !$tmp[$name]["id"] == $name_2 . "++" . $name)
                        {
                            $tmp[$name]["id"] = $name . "++" . $name_2;
                            $tmp[$name]["source"] = $name_2;
                            $tmp[$name]["target"] = $name;
                            array_push($end["edges"], $tmp[$name]);
                        }
                    }
                }
            }
        }
        // if (!empty($tmp[$name]))
        // {
        //     array_push($end["edges"], $tmp[$name]);
        // }
    }

    echo json_encode($end);
?>
