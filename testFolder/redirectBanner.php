<?php
	include('tnzHelper.php');

	// if ($isOnTnz) {
		$redirectBanner = "";
	// } else {
	// 	$actualLink = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://{$_SERVER['HTTP_HOST']}{$_SERVER['REQUEST_URI']}";
	
	//     $patterns = array();
	//     $patterns[0] = "!^http://inthre/!";
	//     $patterns[1] = "!^inthre/!";
	//     $patterns[2] = "!^http://ncerndobedev6794.etv.nce.amadeus.net:8888/!";
	//     $replacements = array();
	//     $replacements[0] = "https://ahp-tools.tnz.amadeus.net/inthre/";
	//     $replacements[1] =  $replacements[0];
	//     $replacements[2] =  $replacements[0];
	//     $newLink = preg_replace($patterns, $replacements, $actualLink);
	
	//     $redirectBanner = "<div style='font-weight:bold;background-color:red;color:black;padding:5;margin:5;'>
	//             <p>This is (or might be) not the inthre you are looking for.<br/>
	//             To access Test or Production data click here <a href=\"" . $newLink . "\">" . $newLink . "</a></p>
	//             </div>";
	// }
?>
