import os
import re
import configparser
import mysql.connector
from mysql.connector import Error

def get_type_from_db(name, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['dbname']
        )
        cursor = conn.cursor()
        query = f"SELECT type FROM llx_const WHERE name = '{name}';"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Error as e:
        print(f"erreur bdd : {e}")
        return None

def update_php_modules(directory, db_config):
    # Définition des motifs à rechercher
    pattern1 = re.compile(r'\$conf->global->(\w+)')
    pattern2 = re.compile(r'\$user->rights->(\w+)->(\w+)(?:->(\w+))?')
    pattern5 = re.compile(r'!empty\(\$conf->(\w+)->enabled\)')
    pattern3 = re.compile(r'\$conf->(\w+)->enabled')
    pattern4 = re.compile(r'(\$\w+)->fk_origin_line')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.php'):
                file_path = os.path.join(root, file)
                print(f"On va checker : {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                
                def replace_global(match):
                    const_name = match.group(1)
                    type_from_db = get_type_from_db(const_name, db_config)
                    if type_from_db == 'chaine':
                        return f"getDolGlobalString('{const_name}')"
                    elif type_from_db in ['yesno', 'int']:
                        return f"getDolGlobalInt('{const_name}')"
                    else:
                        return match.group(0)

                def replace_rights(match):
                    module = match.group(1)
                    right1 = match.group(2)
                    right2 = match.group(3)
                    if right2:
                        return f"$user->hasRight('{module}', '{right1}', '{right2}')"
                    else:
                        return f"$user->hasRight('{module}', '{right1}')"

                def replace_not_empty(match):
                    module = match.group(1)
                    return f"isModEnabled('{module}')"

                def replace_module_enabled(match):
                    module = match.group(1)
                    return f"isModEnabled('{module}')"

                def replace_fk_origin_line(match):
                    variable = match.group(1)
                    return f"{variable}->fk_elementdet ?? {variable}->fk_origin_line"

                contents = pattern1.sub(replace_global, contents)
                contents = pattern2.sub(replace_rights, contents)
                contents = pattern5.sub(replace_not_empty, contents)
                contents = pattern3.sub(replace_module_enabled, contents)
                contents = pattern4.sub(replace_fk_origin_line, contents)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contents)
                
                print(f"Trouvé ! : {file_path}")

config = configparser.ConfigParser()
config.read('config.ini')
db_config = config['DATABASE']
directory = config['PATH']['directory']

update_php_modules(directory, db_config)
