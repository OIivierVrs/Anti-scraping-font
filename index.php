
<?PHP 
session_start();
include_once("src/encrypt_text.php"); 
?>
<?PHP
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <title>Anti Scraping Example</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 128 128%22><text y=%221.2em%22 font-size=%2296%22>⚫️</text></svg>">
        <link href="css/styles.css" rel="stylesheet">
        <?PHP 
        $arr_encrypted_fonts = ["Roboto-Black", "Roboto-Medium"];
        echo init_encrypted_fonts($arr_encrypted_fonts, 5); 
        ?>
    </head>
    <body>
        <h1>Anti Scraping Example</h1>

        <p>Je souhaite cacher ce numéro : <?PHP echo encrypt_text("0601020304", "Roboto-Black"); ?></p>

        <p>Et cet adresse email j'y tiens encore plus : <?PHP echo encrypt_text("adresseemail@supersecrete.com", "Roboto-Medium", 5); ?></p>
    </body>
</html>

