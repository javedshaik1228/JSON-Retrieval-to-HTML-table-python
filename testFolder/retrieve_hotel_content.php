<?php include('redirectBanner.php'); ?>
<?php include('tnzHelper.php'); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="hdc_styles1.css">
<link rel="stylesheet" href="./lib/jquery-ui.css" />
<!-- for icons plus minus font awesome-->
<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <script src="./lib/jquery-1.8.3.js"></script>
    <script src="./lib/jquery-ui.js"></script>
    <script>
            $(document).ready(function(){
                $(".card-header").click(function(){
                    if($(this).next(".card-body").hasClass("active")){
                        $(this).next(".card-body").removeClass("active").slideUp()
                        $(this).children("span").removeClass("fa-minus").addClass("fa-plus")	
                    }
                    else{
                        $(this).next(".card-body").addClass("active").slideDown()
                        $(this).children("span").removeClass("fa-plus").addClass("fa-minus")
                    }
                })

                $(".label-header").click(function(){
                    if($(this).next(".label-body").hasClass("active")){
                        $(this).next(".label-body").removeClass("active").slideUp()
                        $(this).children("span").removeClass("fa-minus").addClass("fa-plus")	
                    }
                    else{
                        $(this).next(".label-body").addClass("active").slideDown()
                        $(this).children("span").removeClass("fa-plus").addClass("fa-minus")
                    }
                })
            })
        
    </script>
    <meta charset="utf-8" />
    <title>Hotel Content UI</title>
</head>
<body>
<?php
include("menu.php");
?>

<div id="container">
<div id="content">

<?php

    print <<<EOD
    <h1>Hotel Descriptive Content UI</h1>
EOD;
    print $redirectBanner;
    $phase = "";         //"PDT";
    $propertyCode = ""; //"ZAXXXSYN"
    $getLongText = false;   //false;
    if (!empty( $_REQUEST[ "PropertyCode" ] ) && !empty( $_REQUEST[ "Phase" ] )) {
        $propertyCode = strtoupper( $_REQUEST[ "PropertyCode" ] );
        $phase = strtoupper( $_REQUEST[ "Phase" ] );
        $getLongText = (filter_has_var(INPUT_POST,'long_text')) ? "true" : "false";

        include("tools.php");
        $command = "";
        if ($isOnTnz) {
            $env = 'env -i NLS_LANG="AMERICAN_AMERICA.WE8ISO8859P1"';
            $env .= ' PYTHONIOENCODING=UTF-8';
            $env .= ' LD_LIBRARY_PATH=/opt/oracle/18.0.0.0.0/lib:$LD_LIBRARY_PATH';
            $env .= ' ORACLE_HOME=/opt/oracle/18.0.0.0.0';
            $env .= ' PATH=/opt/oracle/18.0.0.0.0/bin:$PATH';
            $env .= ' WORK_HOME=/var/www/inthre-tnz';
            $env .= ' HRE_TOOLS_ROOT_DIR=/var/www/inthre-tnz/hre-tools';
            $env .= ' INTHRE_WEB_ROOT_DIR=/var/www/inthre-tnz/web';
            $env .= ' INTHRE_URL_BASE=\'https://ahp-tools.tnz.amadeus.net/inthre/hre-tools/web/\'';
            $env .= ' LQS_ADMIN_PATH=/home/localinthre/lqs_admin';
            $env .= ' EVR_PATH=/var/www/inthre-tnz/hre-tools/scripts/python/evr';
            $env .= ' TNS_ADMIN=/var/www/inthre-tnz/hre-tools/database/';
            $env .= ' PYTHONPATH=/var/www/inthre-tnz/site-packages:/var/www/inthre-tnz/site-packages/suds-0.4-py2.6.egg:/var/www/inthre-tnz/hre-tools/database:/var/www/inthre-tnz/hre-tools/misc:/var/www/inthre-tnz/hre-tools/scripts/python/evr/script:/var/www/inthre-tnz/hre-tools/scripts/python/evr/script/blob:$PYTHONPATH';
            $env .= ' AMDORA_XMLDBFILE=/var/www/inthre-tnz/hre-tools/database/databases-hos.xml';
            $env .= ' python ';

            $command = $env . $TOOLS_REPOSITORY."/misc/retrieve_simple_hotel_config.py ".$propertyCode.' '.$phase;
        }
        else {
            $command = $command = 'python retrieve_json_hotel_content.py 2>&1' . $propertyCode .' '.$phase;  
        }
        $content = shell_exec("$command");
    }
    print "<form method=\"get\" >\n"
    . "<p><label>PropertyCode:</label> <input type=\"text\" value=\"$propertyCode\" name=\"PropertyCode\" />\n"
    . "<label>Phase:</label> <input type=\"text\" value=\"$phase\" name=\"Phase\"/>\n";

    print "<br/><input type=\"submit\" value=\"Display\"/></p>\n</form>";
    ?>
          <div class="accordian">
            <div class="card">
                  <div class="card-header">
                       <h3>Table format </h3>
                       <span class="fa fa-minus"></span>
                  </div>
                  <div class="card-body active">
    <?php
    if (!empty($content)) {
        print "<pre>$content</pre>";
    }



?>

</div></div>
</body>
</html>

