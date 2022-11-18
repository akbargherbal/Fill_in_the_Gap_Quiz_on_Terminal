import logging
logging.basicConfig(filename='error.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

from time import sleep
from colorama import Fore, Back, Style

with open('./quiz_fill_in_blank.py', 'r', encoding='utf-8') as f:
    code = f.read()

huge_number = 1_000

for i in range (huge_number):
    try:
        if i > 0:
            print(Fore.GREEN, '''
Do you want to play again? Enter (yes/no )or (y/n):''')
            play_again = input('Enter your choice: ')
            if play_again.lower().strip()[0] != 'y':
                print(Fore.LIGHTRED_EX, 'Thank you for playing! Goodbye!')
                break
            exec(code)
        else:
            exec(code)
            
    except Exception as e:
        logging.exception(e)
        print(e)
        print('Try again!')