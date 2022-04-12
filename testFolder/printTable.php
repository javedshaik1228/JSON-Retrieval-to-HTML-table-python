<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Countries data</title>
</head>

<style>
    table, th, td {
    border:2px solid black;
    border-collapse: collapse;
    table-align: center;
    margin-left: auto; 
    margin-right: auto;
    }
</style>

<body>

    <form method="get" >
        <label>Country:</label> 
        <input type="text" name="country" /> 
        <br/><input type="submit" value="Submit"/></p>
    </form>

    <?php

    if(  isset( $_REQUEST[ "country" ] ) ){
        $country = $_REQUEST["country"];
        $command = 'C:\Users\shaikj\AppData\Local\Programs\Python\Python310\python.exe jsonRetrieval.py 2>&1' . $country;  
        $output = shell_exec($command);
        print "<pre><p>" . $output ." </p></pre>";
    }
    ?>

</body>
</html>