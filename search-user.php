<?php

	if(isset($_GET["q"]))
	{
		$URLname = urlencode(base64_encode($_GET["q"]));

		$target = "/search.php?q={$URLname}";
		header("Location:$target");
		exit;
	}
	else
	{
		echo '
		<form action="search-user.php">
		Search: <input type="text" name="q"><br>
		<input type="submit" value="Submit">
		</form>';
	}
?>
