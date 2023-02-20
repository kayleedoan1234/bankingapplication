# Ngoc Doan CIS345 Mon Wed 12:00-1:15 PE3
import os
import random
import json

file_handle = open('customers.json')
accounts = json.load(file_handle)
file_handle.close()

# Allow 3 invalid pin entries
tries = 1
pin_tries = 1
max_tries = 3
pin_found = False

while True:
    try:
        selection = input('''
Welcome to Cactus Bank!
*********************************
* Enter 1 to add a new customer *
* Enter 2 to delete a customer  *
* Enter 3 to make transaction   *
*********************************
Make your selection: ''')
        if int(selection) not in range(1,4):
            raise TypeError
        break
    except(ValueError, TypeError):
        print('Selection should be 1,2, or 3. Try again....')

username = input('Please enter a username: ')

if selection == 1:
    #Add new customer
    if username in accounts:
        print(f'{username} already exists. Exiting the system.')
        quit()
    else:
        accounts[username]={}
        ans1 = int(input('Enter 1 to create a pin yourself or 2 and the system will create a pin for you: '))
        if ans1 == 1:
            while pin_tries <= max_tries:
                pin = int(input('Select a number between 1 and 9999 as your pin: '))
                print(pin)
                if 0 < pin < 10000:
                    accounts[username]['Pin'] = pin
                    pin_found = True
                    break
                else:
                    print('Invalid pin entered.')
                    pin_tries += 1
                    if pin_tries > max_tries:
                        print('Please try later ....')
        elif ans1 == 2:
            pin = random.randint(1, 9999)
            print("Your pin is: ", pin)
            accounts[username]['Pin'] = pin
            pin_found = True
        else:
            print('Invalid option! Thank you for visiting Catcus Bank.  Come back soon.')
        name = input('Please enter your name: ')
        accounts[username]['Name'] = name

        #ask for checking amount
        try:
            checking = float(input('Enter the amount you will deposit to the checking account: '))
            if checking < 0:
                raise TypeError('A negative number was entered. The current balance will be 0.0')
        except ValueError:
            print('Invalid number enter. The current balance will be 0.0')
            checking = 0.0
        except TypeError as e:
            print(e)
            checking = 0.0
        accounts[username]['C']= checking

        #ask for saving
        try:
            saving = float(input('Enter the amount you will deposit to the saving account: '))
            if saving < 0:
                raise TypeError('A negative number was entered. The current balance will be 0.0')
        except ValueError:
            print('Invalid number enter. The current balance will be 0.0')
            saving = 0.0
        except TypeError as e:
            print(e)
            saving = 0.0
        accounts[username]['S'] = saving
        print('''Your account has been created
                Please visit the system again to make transactions''')
        input('Please Enter to continue...')

elif selection == 2:
    #Delete a customer
    if username in accounts:
        accounts.pop(username)
        print(f'{username} has been deleted')
    else:
        print('Username not found! Exiting the system')
        quit()
else:
    #Make transaction
    if username not in accounts:
        print('Error: username is not in the system.' )
    else:
        print('Cactus Bank- Making Transaction')
        print()
        selection = input('Enter pin or x to exit application: ').casefold()

        # determine exit, pin not found, or correct pin found
        if selection == 'x':
            quit()

        elif int(selection) != accounts[username]['Pin']:
            os.system('clear')
            print(f'Invalid pin. Attempt {tries} of {max_tries}. Please Try again')
            if tries == max_tries:
                print('Locked out!  Exiting program')
            # increment tries
            tries += 1

        else:
            tries = 1 #reset tries
            pin = selection
            # clear screen
            os.system('clear')

            #New screen
            for t in range(1, 5):
                print(f"Welcome {accounts[username]['Name']}")
                #ask for checking or saving
                while True:
                    try:
                        selection = input('Checking or Saving (Enter C or S): ').upper()
                        if selection != 'C' and selection !='S':
                            raise ValueError('Incorrect Selection. You must enter C or S.')
                    except ValueError as ex:
                        print(ex)
                    else:
                        os.system('clear')
                        print(f'Opening {selection} Account ...\n')
                        break

                print('Transaction instructions:')
                print(' - Withdrawal enter a negative dollar amount: -20.00.')
                print(' - Deposit enter a positive dollar amount: 10.50')

                print(f"Balance: ${accounts[username][selection]: ,.2f}")
                amount = 0.00
                try:
                    amount = float(input(f'Enter transaction amount: '))
                except Exception:
                    print('Bad Amount - No Transaction.')
                    amount = 0.0

                if (amount + accounts[username][selection]) >= 0:
                    accounts[username][selection] = accounts[username][selection] + amount
                    print(f"Transaction complete. New balance is {accounts[username][selection]: ,.2f}")
                else:
                    print('Insufficient Funds. Transaction Cancelled.')

                ans = input('Press n to make another transaction or x to exit application: ').casefold()
                if ans == 'x':
                    break


with open('customers.json','w') as fp:
    json.dump(accounts,fp)

#Print json file
print('''
Saving data...

Data Saved...
Exiting''')
for k,v in accounts.items():
    print(f'\n{k:>10}', end ='')
    for key in v:
        print(f'{v[key]:>20}',end='')
print()





