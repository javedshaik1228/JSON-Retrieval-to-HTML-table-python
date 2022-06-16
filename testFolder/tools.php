<?php
	include('tnzHelper.php');

	if ($isOnTnz) {
		// TODO: path optimization to be neet
	    // $TOOLS_REPOSITORY = getenv('HRE_TOOLS_ROOT_DIR');
	    $TOOLS_REPOSITORY = '/var/www/inthre-tnz/hre-tools';
	    $WEB_ROOT_DIR = getenv('INTHRE_WEB_ROOT_DIR');
	    $WEB_URL = getenv('INTHRE_URL_BASE');
	    $LQS_ADMIN_PATH = getenv('LQS_ADMIN_PATH');
	    $EVR_PATH = getenv('EVR_PATH');
	    
	} else {
		if ( file_exists( ".use_local_tools" ) )
		{
		    $TOOLS_REPOSITORY = realpath( getcwd() . "/.." );
		}
		else
		{
		    $TOOLS_REPOSITORY = "~inthre/tools";
		}
	}
?>
