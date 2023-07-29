import ops


bot_on = True

adress_book = ops.AddressBook()
stop_words = ["good bye", "close", "exit"]
main_file = "address_book.bin"

def input_error(func):
    def inner(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except UnboundLocalError:
            return 'Enter command'
        except TypeError:
            return 'Enter name and phone separated by a space!'
        except KeyError:
            return 'This name not found!'
        except IndexError:
            return 'This name found! Enter another name.'
        except ValueError:
            return 'Error. Wrong value.'
        except AttributeError:
            return 'Error... Wrong command.'
    return inner


def start():
    
    print("\nAddress book bot started!\nHow can I help you?\nTo see awailable comands type 'help'\n")
    adress_book.load_from_file(main_file)


def show_page(page_number): # Підкажіть як релізувати принт конкретної сторінки?
    
    return adress_book.show_page(page_number)


def helper(*args):
    res = ''
    for key in comands.keys():
        res += f"-{key}\n"
    return  f"\n | Available bot functions:|\n{res}"


def error(*args):
    return "Unknown command. Use function 'help' to show available commands..."


@input_error
def add(name, phone, birthday = ''):

    rec = ops.Record(ops.Name(name), ops.Phone(phone), ops.Birthday(birthday))
    adress_book.addRecord(rec)
    # phone_num = [phone.value for phone in adress_book[rec.name.value].phones]
    return f"\nNew contact '{rec.name.value}' added in dict.\nTo show contacts use 'show all'...\n"
        

@input_error
def change_phone(name, old_phone, new_phone):
    
    rec = adress_book[name]
    rec.change_phone(ops.Phone(old_phone), ops.Phone(new_phone))
    return rec.__str__()
    
   
@input_error
def add_phone(name, phone):
    
    rec = adress_book[name]
    rec.add_phone(ops.Phone(phone))
    print('\nContact updated with new phone')
    return rec.__str__()


@input_error
def delete_phone(name, phone):
    
    rec = adress_book[name]
    rec.del_phone(ops.Phone(phone))
    if phone.isdigit():
        return f"{rec.name.value} : {[ phone.value for phone in rec.phones]}\n"
    else:
        return "Number is not numerical!"


@input_error
def add_birthday(name, birthday):
    
    rec = adress_book[name]
    bd = ops.Birthday(birthday)
    rec.add_birthday(bd)
    return rec.__str__()


@input_error
def days_to_birthday(name):
    
    rec = adress_book[name]
    return rec.days_to_birthday()


@input_error
def phone(name):

    rec = adress_book[name]
    return rec.__str__()


@input_error
def find(*args)-> str:
    
    return adress_book.find(*args)


@input_error
def show_all(*args):

    return adress_book.print_book()


comands =  {'hello':start,
            'start': start,
            'add phone': add_phone,
            'add new': add,
            'add birthday': add_birthday,
            'change':change_phone,
            'phone':phone,
            'show all':show_all,
            'help':helper,
            'find': find,
            'page': show_page,
            'delete phone': delete_phone,
            'days to bd': days_to_birthday,
            }


def parser(text):
    for key in comands.keys():          #скрипт знаходить ключ у введеному в консоль повідомленні і підставляє значення у відповідну функцію
            # comand = user_input.lower()
            # user_command = user_input.split()      
        if text.lower().startswith(key):
            func = comands.get(key)
            args = text[len(key):].strip().split()
            return func, args
    return None, None
  

def main():             #Вирішую робити через таку структуру щоб програма одразу оцінювала те що вводиться з консолі, як на мене такий варіант є логічним так як можна в будьякий момент додати нові ключі в команди і записати під кожен ключ нову окрему функцію. Також усі варіанти окрім ключів-функцій одразу відсіюються. А при правильному введені функції скрипт повертає одразу значення з потрібної функції.

    start()
    while True:

        user_input = input(">>> ")
        
        if user_input in stop_words: # Замінив на список
            print("Good bye!")
            break
        func, args = parser(user_input)
        if func:
            result = func(*args)
        else:
            result = error(user_input) 
        print(result) 
            

if __name__ == "__main__":
    main()