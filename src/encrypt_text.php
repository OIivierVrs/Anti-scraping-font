<?PHP
$GLOBALS['env'] = parse_ini_file('./.env');

function decrypt_mapping($encrypted_data_b64, $iv_b64, $key) {

    // Decode base64-encoded data and IV
    $encrypted_data = base64_decode($encrypted_data_b64);
    $iv = base64_decode($iv_b64);
    
    // Decrypt the data
    $decrypted_data = openssl_decrypt($encrypted_data, 'aes-128-cbc', $key, OPENSSL_RAW_DATA, $iv);
    
    // Remove PKCS7 padding
    $decrypted_data = rtrim($decrypted_data, "\x07");
    
    // Convert decrypted data (JSON) back to array
    $mapping = json_decode($decrypted_data, true);
    
    return $mapping;
}

function decrypt_file($file_path, $key) {

    // Read encrypted data and IV from the file
    $lines = file($file_path, FILE_IGNORE_NEW_LINES);
    $encrypted_data_b64 = $lines[0];
    $iv_b64 = $lines[1];
    
    // Decrypt the mapping using the IV and key
    $mapping = decrypt_mapping($encrypted_data_b64, $iv_b64, $key);
    
    return $mapping;
}

function init_encrypted_fonts($arr_fonts, $encryption_level = 1){
    $html = "<style>";
    foreach($arr_fonts as $font){
        
        # We get all the ttf files that match the font name
        $files = glob($GLOBALS['env']['FONTS_FOLDER']."encrypted/$font*.ttf");

        # On boucle sur les $files tant qu'on atteint pas le niveau de cryptage souhaité
        $i = 0;
        while($i <= $encryption_level){
            $html .= "@font-face {font-family: '".$font."_".$i."_Encrypted'; src: url('fonts/encrypted/".$font."_".$i."_Encrypted.ttf') format('truetype');} .".$font."_".$i."_Encrypted {font-family: '".$font."_".$i."_Encrypted' !important;}";
            $i++;
        }
    }
    $html .= "</style>";
    return $html;
}

function encrypt_text($texte, $font, $encryption_level = 1){

    if($texte == ""){
        return "";
    }

    # We get all the ttf files that match the font name
    $files = glob($GLOBALS['env']['FONTS_FOLDER']."encrypted/$font*.ttf");

    # On boucle sur les $files tant qu'on atteint pas le niveau de cryptage souhaité
    $i = 1;
    $arr_fonts_to_load = [];
    while($i <= $encryption_level){

        $i_file = $i-1;

        $font_to_load = $font."_".$i_file."_Encrypted";

        $arr_fonts_to_load[$font_to_load] = "";

        // Load key in bin file
        $encrypted_file_path = $GLOBALS['env']['FONTS_FOLDER']."encrypted/". $font_to_load.".bin";

        # Convert $key to bytes
        $key = $GLOBALS['env']['ENCRYPT_KEY'];
        
        // Decrypt the mapping key
        $decrypted_data = decrypt_file($encrypted_file_path, $key);
        
        // Convert decrypted data to array (assuming JSON format)
        $mapping = $decrypted_data;

        $arr_fonts_to_load[$font_to_load] = $mapping;

        $i++;
    }

    
    // Initialize an array to store the correspondences
    $correspondences = [];
    
    $final_texte = "";
    // Iterate over each letter in the word
    for ($i = 0; $i < strlen($texte); $i++) {
        $letter = $texte[$i];

        # We randomly get the mapping and the key in the $arr_fonts_to_load array
        $font = array_rand($arr_fonts_to_load);
        $mapping = $arr_fonts_to_load[$font];

        # We check if the file font and it's corresponsing key exists
        $encrypted_font_path = $GLOBALS['env']['FONTS_FOLDER']."encrypted/". $font.".ttf";
        $encrypted_keyfile_path = $GLOBALS['env']['FONTS_FOLDER']."encrypted/". $font.".bin";

        if(!file_exists($encrypted_font_path) || !file_exists($encrypted_keyfile_path)){
            $final_texte .= $letter;
            continue;
        }
    
        # Find the key for the letter
        $key = array_search($letter, $mapping);
    
        if($key === false) {
            $key = $letter;
        }

        $final_texte .= "<span class='".$font."'>".$key."</span>";
    }

    return $final_texte;
}


?>