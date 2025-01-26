

import sys
from os import path
import configparser


# +++++++++++++++++++++++++++
# Return selected file data/content
# +++++++++++++++++++++++++++
def read_file(file_name):
   
    # Add app path to the file name
    root_path = path.dirname(path.abspath(sys.argv[0]))

    file_path_name = root_path + file_name
    file = path.join(path.dirname(__file__), file_path_name)
    
    file_content = configparser.ConfigParser()
    file_content.read(file, encoding="utf8")

    # Get the value and replace the literal \n with actual newline
    # Process all sections and their key-value pairs
    for section in file_content.sections():
        for key in file_content[section]:
            file_content[section][key] = file_content[section][key].replace('\\n', '\n')

    return file_content