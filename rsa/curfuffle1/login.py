#!/usr/bin/exec-suid -- /usr/bin/python3
try: 
    with open('./company_password.txt', 'r') as f:
        password = f.read().strip()
except FileNotFoundError:
    print('Error fetching company_password')
    exit()

    
inp = input('Associate Password: ').strip()
if inp == password:
    print('\nWelcome Associate')
    try:
        with open('/flag', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print('Error reading flag.')
        exit()
else:
    print('Incorrect password or unkown employee.')
    exit()



