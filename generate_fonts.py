import random
import string
import json
import os
from fontTools.ttLib import TTFont
import fontTools.ttLib.tables._g_l_y_f as TTGlyphGlyf
from encrypt import encrypt_file
from word2number import w2n
from dotenv import main
main.load_dotenv()

arr_full_letter_number = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
max_encryption_level = 5
font_folder = os.getenv("FONTS_FOLDER")

def shuffle_coordinates(coordinates):
    # Convert tuple to list, shuffle, then convert back to tuple
    coordinates_list = list(coordinates)
    random.shuffle(coordinates_list)
    return tuple(coordinates_list)

def shuffle_cmap(font):
    cmap = font.getBestCmap()

    # Extract alphanumeric characters with length 1
    single_char_mapping = {}
    for char_code in cmap.keys():
        char = chr(char_code)
        if char in string.ascii_letters + string.digits and len(char) == 1:
            single_char_mapping[char] = cmap[char_code]

    # Shuffle single character values randomly in-place
    single_char_values = list(single_char_mapping.values())
    random.shuffle(single_char_values)

    # Create a dictionary to store shuffled mappings for single character keys
    shuffled_single_char_mapping = {char: shuffled_value for char, shuffled_value in zip(single_char_mapping.keys(), single_char_values)}

    # Update cmap with shuffled values for single character keys
    for char, shuffled_value in shuffled_single_char_mapping.items():
        cmap[ord(char)] = shuffled_value

    # Extract mappings for characters with more than one character
    multi_char_mapping = {char: cmap[char_code] for char_code, char in cmap.items() if len(char) > 1}

    '''
    glyf_table = font["glyf"]

    for glyph_name in glyf_table.glyphs:
        glyph_data = glyf_table.glyphs[glyph_name]
        if isinstance(glyph_data, TTGlyphGlyf.Glyph):
            # Handle glyphs with contours
            if glyph_data.isComposite():
                if hasattr(glyph_data, "components"):
                    for component in glyph_data.components:
                        component.coordinates = shuffle_coordinates(component.coordinates)
            else:
                if hasattr(glyph_data, "getCoordinates"):
                    if hasattr(glyph_data, "numberOfContours"):
                        glyph_data.coordinates = shuffle_coordinates(glyph_data.getCoordinates(glyf_table))
                        # Save the modified coordinates back to the glyph
                        glyph_data.recalcBounds(glyf_table)
                else:
                    # Handle older versions of fontTools
                    glyph_data.coordinates = shuffle_coordinates(glyph_data.coordinates)
                    # Save the modified coordinates back to the glyph
                    glyph_data.recalcBounds(glyf_table)

    font["glyf"] = glyf_table
    '''

    # Apply the modified cmap to the font object
    font['cmap'].tables[0].cmap = cmap

    return shuffled_single_char_mapping, multi_char_mapping


# We get all the fonts files in the fonts directory
fonts = [f for f in os.listdir(font_folder) if f.endswith('.ttf')]

for font_file in fonts:

    font_name = font_file.replace(".ttf", "")
        
    input_file = font_folder + font_name + '.ttf'

    # We itirate until we reach the max_encryption_level
    for i in range(max_encryption_level):

        output_file = font_folder + '/encrypted/' + font_name + '_' + str(i) + '_Encrypted' + '.ttf'
        mapping_file = font_folder + '/encrypted/' + font_name + '_' + str(i) + '_Encrypted' + '.json'

        # Load the font file
        font = TTFont(input_file)

        # Shuffle only the values in the character mapping (cmap) for alphanumeric characters with length 1
        single_char_mapping, multi_char_mapping = shuffle_cmap(font)

        # Combine the shuffled single character mapping with the original mappings for characters with more than one character
        final_mapping = {**single_char_mapping, **multi_char_mapping}

        for fm in final_mapping:
            value = final_mapping[fm]
            if value in arr_full_letter_number:
                final_mapping[fm] = w2n.word_to_num(value)

        # Save the mapping to a file
        with open(mapping_file, 'w') as f:
            json.dump(final_mapping, f)

        # Save the modified font to a new file
        font.save(output_file)

        encrypt_file(font_name, i)

        # Remove original json
        os.remove(mapping_file)