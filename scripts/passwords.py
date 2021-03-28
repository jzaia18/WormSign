import random
import array


def generate_passwords(x):

    passwords = []
    for i in range(0, x):
        len = 12
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        lower_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                             'z']
        upper_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                             'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                             'Z']
        sym = ['@', '#', '$', '%', '*']

        listofchars = nums + upper_chars + lower_chars + sym

        rand_digit = random.choice(nums)
        rand_upper = random.choice(upper_chars)
        rand_lower = random.choice(lower_chars)
        rand_symbol = random.choice(sym)

        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

        for x in range(len - 4):
            temp_pass = temp_pass + random.choice(listofchars)
            temp_pass_list = array.array('u', temp_pass)
            random.shuffle(temp_pass_list)

        password = ""
        for x in temp_pass_list:
            password = password + x

        passwords.append(password)

    return passwords