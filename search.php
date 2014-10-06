<?php

$link = mysql_connect('odroid-u3.local', 'monitor', 'test123');
if (!$link) {
    die('Verbindung schlug fehl: ' . mysql_error());
}
echo 'Erfolgreich verbunden';

mysql_select_db('monitor') or die('Could not select database');

$query = 'SELECT * FROM data20141006';
$result = mysql_query($query) or die('Query failed: ' . mysql_error());

echo "<table>\n";
while ($line = mysql_fetch_array($result, MYSQL_ASSOC)) {
    echo "\t<tr>\n";
    foreach ($line as $col_value) {
        echo "\t\t<td>$col_value</td>\n";
    }
    echo "\t</tr>\n";
}
echo "</table>\n";

mysql_free_result($result);
mysql_close($link);
?>

