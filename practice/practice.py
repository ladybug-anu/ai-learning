# def greet_user(name):
#     return f"Hello {name}, welcome to AI engineering"

# name = input('Enter your name: ')
# print(greet_user(name))

# def calculate_savings(income, expenses):
#     return income - expenses

# try:
#     income = int(input('Enter your income: '))
#     expenses = int(input('Enter your expenses: '))
#     print(calculate_savings(income, expenses))
# except ValueError:
#     print('Please enter a valid number')

def chunk_text(text, size, overlap):
    chunk_list = []
    for i in range(0, len(text), size - overlap):
        chunk_list.append(text[i:i+size])
    return chunk_list

t = input('enter')
s = int(input('size'))
overlap = int(input('Enter overlap'))
print(chunk_text(t, s, overlap))

