<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="mystyles.css">
    <title>Hotel Descriptive Content UI</title>

    <script>
        function alertMessage(message) {
            alert(message);
        }
    </script>

</head>



<body>

<?php
include("menu.php");

$phase; // = "UAT";
$property_code; // = "ZAXXXSYN";
$getLongText; // = false;

?> 
   <div id = "container"> 
    <div class = "tablecontent">
        <h1>Hotel Descriptive Content UI</h1>    
        <BR><BR>
        <form method="post" >
            <label>Property Code: </label> 
            <input type="text" name="property_code" /> 
            <label>Phase: </label> 
            <input type="text" name="phase" /> 
            <label>&ensp; Get Long Description?:</label> 
            <input type="checkbox" name="long_text"> 
            <br><input type="submit" value="Display"/></p>

        </form>

    <?php
    if(  isset( $_REQUEST[ "phase" ] )) {
        $phase =  $_REQUEST[ "phase" ];
    }

    $getLongText = (filter_has_var(INPUT_POST,'long_text')) ? "true" : "false";

    if(  isset( $_REQUEST[ "property_code" ] ) ){
        $property_code = $_REQUEST["property_code"];
        $command = 'python jsonRetrieval.py ' . $property_code .' '. $getLongText . ' ' . $phase;  
        $output = shell_exec($command);
        print "<pre><p>" . $output ." </p></pre>";
    }
    
    ?>
        </div>
    </div>

</body>
</html>