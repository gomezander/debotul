from __future__ import print_function

import time
import random


import sys
import time

dibujo = [r'''                , ,, ,                              
                | || |    ,/  _____  \.             
                \_||_/    ||_/     \_||             
                  ||       \_| . . |_/              
                  ||         |  L  |                
                 ,||         |`==='|                
                 |>|      ___`>  -<'___             
                 |>|\    /             \            
                 \>| \  /  ,    .    .  |           
                  ||  \/  /| .  |  . |  |           
                  ||\  ` / | ___|___ |  |     (     
               (( || `--'  | _______ |  |     ))  ( 
             (  )\|| (  )\ | - --- - | -| (  ( \  ))
             (\/  || ))/ ( | -- - -- |  | )) )  \(( 
              ( ()||((( ())|         |  |( (( () )
    ''', 
    r'''
                                ,     /~/'   ,--,
                               _/`, ,/'/'   /'/~
                             .'___|/ /____/'/'   __/|
                             /~  __        `\ /~~, /'
                      _,-,__/'  ,       \   /'/~/ /'
                    .~      `   \_/  / ,     "~_/'  ,-'~~~~~---,_
                    `,               `~    `~~~|   /'    ~~\__   `~\_
            |~~~/     `~---,__        _,      /'  | /~~\  _/' ~~\    `~,
            |/\`\          /'     _,-~/      /'  .' __ `/'       `~\    \ 
   |~~~/       `\`\        `-\/\/~   /'    .'    |    `| \/    |    `\_  |
   |/\`\         `,`\              /'      |_  ,' /~\ /' |' |  `\     \~\|
      `\`\    _/~~_/~'            /'      /' ~~/     /   `\ `\,  | \   |
~/      `\`\/~ _/~                ~/~~~~\/'    `\__/' \/\  `\_/\ `\~~\ |
\`\    _/~'    \               /~~'                `~~~\`~~~'   `~~'  `'__
 `\`\/~ _/~\    `\           /' _/                      `\        _,-'~~ |
   `\_/~    `\    `\       _|--'                          |      `\     |'
              `\    `\   /'          _/'                  |       /' /\|'
                /\/~~\-/'        _,-'                     |     /' /'  `
                |_`\~~~/`\     /~                          \/~~' /'
                   |`\~ \ `\   `\                           `| /'
    ''',
    r'''
                              .-"/   .-"/
                             /  (.-./  (
                            /           \      .^.
                           |  -=- -=-    |    (_|_)
                            \   /       /      // 
                             \  .=.    /       \\
                        ___.__`..;._.-'---...  //
                  __.--"        `;'     __   `-.  
        -===-.--""      __.,              ""-.  ".
          '=_    __.---"   | `__    __'   / .'  .'
          `'-""""           \             .'  .'
                             |  __ __    /   |
"Saca el DNI!",              |  __ __   //`'`'
                             |         ' | //
                             |    .      |//
                            .'`., , ,,,.`'.
                           .'`',.',`.` ,.'.`
                            ',',,,,.'...',,'
                            '..,',`'.`,`,.',
                           ,''.,'.,;',.'.`.'
                           '.`.',`,;',',;,.;
                            ',`'.`';',',`',.
                             |     |     |
                             (     (     | Soc catalana
    '''
]

banner = (r"""
        ▓█████▄  ██▓ ▄▄▄       ▄▄▄▄    ██▓     ▒█████  
        ▒██▀ ██▌▓██▒▒████▄    ▓█████▄ ▓██▒    ▒██▒  ██▒
        ░██   █▌▒██▒▒██  ▀█▄  ▒██▒ ▄██▒██░    ▒██░  ██▒
        ░▓█▄   ▌░██░░██▄▄▄▄██ ▒██░█▀  ▒██░    ▒██   ██░
        ░▒████▓ ░██░ ▓█   ▓██▒░▓█  ▀█▓░██████▒░ ████▓▒░
        ▒▒▓  ▒ ░▓   ▒▒   ▓▒█░░▒▓███▀▒░ ▒░▓  ░░ ▒░▒░▒░ 
        ░ ▒  ▒  ▒ ░  ▒   ▒▒ ░▒░▒   ░ ░ ░ ▒  ░  ░ ▒ ▒░ 
        ░ ░  ░  ▒ ░  ░   ▒    ░    ░   ░ ░   ░ ░ ░ ▒  
        ░     ░        ░  ░ ░          ░  ░    ░ ░  
        ░                          ░                """)

class colors:
    CRED2 = "\33[91m"
    CBLUE2 = "\33[94m"
    ENDC = "\033[0m"


def show_menu():

    for col in banner:
        print(colors.CRED2 + col, end="")
        sys.stdout.flush()
        time.sleep(0.0010)

    x = ("""
                    Authors:  xm0d, agarma, at0mic, ander
                    """)
    for col in x:
        print(colors.CBLUE2 + col, end="")
        sys.stdout.flush()
        time.sleep(0.0040)

    y = "\n\t\t          😈 El diablo! 😈\n"
    for col in y:
        print(colors.CRED2 + col, end="")
        sys.stdout.flush()
        time.sleep(0.0040)

    z = "\n"
    for col in z:
        print(colors.ENDC + col, end="")
        sys.stdout.flush()
        time.sleep(0.4)

    """
    Muestra un menú interactivo para que el usuario elija el tipo de scan.
    """
    for col in random.choice(dibujo):
        print(colors.CRED2 + col, end="")
        sys.stdout.flush()
        #time.sleep(0.0025)
    time.sleep(1)
    print("\n" + colors.ENDC + col)
    print("Seleccione el tipo de reconocimiento que desea realizar:\n")
    print(" 1. Internal Recon")
    print(" 2. External Recon")
    print(" 3. HTTP")
    print(" 4. Custom")
    print(" 5. Exit")

    # Solicitar al usuario que seleccione un perfil
    choice = input("\nIngrese el número correspondiente a su elección: ")

    profiles = {
        '1': 'Internal Recon',
        '2': 'External Recon',
        '3': 'HTTP',
        '4': 'Custom',
        '5': 'Exit'
    }

    # Validar la opción y retornar el perfil seleccionado
    return profiles.get(choice, None)