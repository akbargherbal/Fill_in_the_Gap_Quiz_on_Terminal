from random import randint
from time import sleep
from collections import defaultdict

import pandas as pd
from itertools import chain
from collections import Counter
import os
import subprocess
from colorama import Fore, Back, Style

import subprocess

import subprocess
from time import sleep
from datetime import datetime
def time_now():
    '''Get Current Time'''
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S.%f")[:-4]
    print("Current Time =", current_time)
    return now


url_progress = 'https://raw.githubusercontent.com/akbargherbal/Fill_in_the_Gap_Quiz_on_Terminal/master/porgress_quizzes.csv'
url_revision = 'https://raw.githubusercontent.com/akbargherbal/Fill_in_the_Gap_Quiz_on_Terminal/master/REVISE_QUIZ.csv'
start = time_now()
cmd_line = f"""
curl -o porgress_quizzes.csv {url_progress} --ssl-no-revoke
curl -o REVISE_QUIZ.csv {url_revision} --ssl-no-revoke
""".strip().split('\n')


try:
    print('Fetching Data from Github ...')
    for cmd in cmd_line:
        subprocess.run(cmd, shell=True)
    
except Exception as e:
    print(e)
    print(f'Failed to update porgress_quizzes.csv or REVISE_QUIZ.csv from Github!')


from zipfile import ZipFile
os.system('cls' if os.name == 'nt' else 'clear')

zf = ZipFile('./QUIZ_ON_CMD.zip')

quiz_collections  = []
for i in zf.filelist:
    if i.filename.endswith('.csv') == False:
        quiz_collections.append(i.filename)

quiz_collections

csv_files  = []
for i in zf.filelist:
    if i.filename.endswith('.csv'):
        csv_files.append(i.filename)

def sort_function(list_01, extra='A_Bunch_of_Text_'):
    '''Sort by integers not string; i.e. 29 comes before 100!'''
    result = [i.replace(extra, '') for i in list_01] # REMOVE PREFIXES IF NECESSARY; LIKE FOLDER PATH.
    result = [''.join([i for i in j if i.isnumeric()]) for j in result] # What remains only valid file name
    
    result = list(zip(list_01, result)) # zip input and output
    
    result = [(j ,'0') if (set(i) == {'0'}) else (j, i.lstrip('0')) for (j, i) in result]
    
    try:
        result = sorted(result, key= lambda i: int(i[1]))
        return [i[0] for i in result]
    
    except Exception as e:
        print('ERROR: Sort Exception!')
        print(e)
    assert len(list_01) == len(result),f'Something went wrong; input size {len(list_01)} should equal output {len(result)} size!'

dict_collection_vs_file = defaultdict(list)
for quiz in quiz_collections:
    for csv_f in csv_files:
        if csv_f.startswith(quiz):
            dict_collection_vs_file[quiz].append(csv_f)
dict_collection_vs_file = dict(dict_collection_vs_file)            

dict_collection_vs_file = {k: sort_function(v, k) for k,v in dict_collection_vs_file.items()}

list_quiz_collection = list(dict_collection_vs_file)

list_quiz_collection

dict_dig_vs_collection = {idx:i for (idx, i) in enumerate(list_quiz_collection)}

print('Available Quiz Collections are as Follows:')
for (idx, q) in enumerate(list_quiz_collection):
    print(Fore.YELLOW, f'{idx} : {q.replace("/", "")}')
    print('----------------------------------------------------')

quiz_type = int(input(f"""
Enter the number of the of quiz you want to test yourself in:
Enter an a number between {0} and {len(list_quiz_collection)-1} INCLUSIVE.
"""))

print(Fore.CYAN, f"""
You'll be tested in the following collection:
{dict_dig_vs_collection[quiz_type].replace("/", "")}""")

set_completed_quizzes = pd.read_csv(f'./porgress_quizzes.csv', encoding='utf-8')
set_completed_quizzes = set(list(set_completed_quizzes['QUIZ_NAME']))

quiz_list = dict_collection_vs_file[dict_dig_vs_collection[quiz_type]]

quiz_list = [i for i in quiz_list if i not in set_completed_quizzes]


quiz = quiz_list[0]

df = pd.read_csv(zf.open(quiz), encoding='utf-8')
df = df.sample(frac=1).reset_index(drop=True)
print(Fore.LIGHTBLUE_EX, f'Number of Questions in this Quiz: {len(df)}')

df =  list(zip(df.QUESTION_TEXT, df.OPTION_1, df.OPTION_2, df.OPTION_3))
df_incorrect = pd.read_csv('REVISE_QUIZ.csv', encoding='utf-8')
df_inc = pd.DataFrame()

score = 0
progress = 0
number_of_questions = len(df)
incorrect = 0


sleep(3)
for (idx, q) in enumerate(df):
    os.system('cls' if os.name == 'nt' else 'clear')
    if idx != 0:
        print(f'''Current score is {100 * score} ---- {score} Correct Answer; {incorrect} Incorrect Answer
        ''')
        print(f'''{idx + 1} of {number_of_questions}; {number_of_questions - (idx + 1)} to go!
        ''')

    print(Fore.LIGHTYELLOW_EX, f'Question: {idx + 1}')
    print(Fore.LIGHTCYAN_EX, f"""
{q[0]}
""")
    answer = input("".strip()).lower()
    if answer in q[1:]:
        print(Fore.LIGHTGREEN_EX, f'''
Correct!
''')
        score += 1
    else:
        print(Fore.RED, f"""Incorrect! The word we're looking for is:
        """)
        for i in range(3):
            print(Fore.LIGHTYELLOW_EX, f"""
        {q[1].upper()}!""")
            sleep(1)
        incorrect += 1
        
        df_inc['QUESTION_TEXT'] = q[0]
        df_inc['OPTION_1'] = q[1]
        df_inc['OPTION_2'] = q[2]
        df_inc['OPTION_3'] = q[3]
        df_incorrect = df_incorrect.append(df_inc).reset_index(drop=True)

    print('-'*50)
    sleep(0.1)
print('Closing ZIP FILE!')
zf.close()
print('End of Quiz; Goodbye!')


finished = True
############
print('Trying to update Quiz Progress on Github repository ...')
end = time_now()
############

cmd = f"""
git add .
git commit -m "Git pushed from inside python script @ {end}"
git push origin master  
""".strip().split('\n')


if finished:
    quiz_time = [end]
    quiz_name = [quiz]
    correct_answers = [score]
    incorrect_answers = [incorrect]
    end = time_now()
    duration_minutes = (end - start).seconds / 60
    duration_minutes = round(duration_minutes, 2)
    duration_minutes = [duration_minutes]


    try:
        print('Trying to update Quiz Progress on Github...')
        df_read = pd.read_csv('porgress_quizzes.csv', encoding='utf-8') 
        df_pr = pd.DataFrame()
        df_pr['QUIZ_DATE_TIME'] = quiz_time
        df_pr['QUIZ_NAME'] = quiz_name
        df_pr['CORRECT_ANSWERS'] = correct_answers
        df_pr['INCORRECT_ANSWERS'] = incorrect_answers
        df_pr['DURATION_MINUTES'] = duration_minutes
        df_pr = pd.concat([df_read, df_pr], axis=0)
        df_pr.to_csv('porgress_quizzes.csv', encoding='utf-8', index=False)
        df_incorrect.to_csv('REVISE_QUIZ.csv', encoding='utf-8', index=False)

        print('Pushing to Github...')
        for command in cmd:
            print(command)
            subprocess.run(command)
            print('-------------------------')

    except Exception as e:
        print("Couldn't update quiz progress on Github!")
        print(e)