import sys

# 1. Create a function called return_num_vowels that accepts an 
# input string and returns a dictionary where the keys are the vowels
# a, e, i, o, u, and the values are the count of the vowels.

# write function here
def return_num_vowels(string):
    string = string.lower()
    dictionary = dict({'a': string.count('a'),'e': string.count('a'),'e': string.count('e'),'i': string.count('i'),'o': string.count('o'), 'u': string.count('u')})
    return dictionary


# 2. Create a function called return_num_characters that counts the number english alpha
# characters in a input string (less spaces, punctuation, numbers, and all other characters not a-z) 
# and returns the count. Hint: review the python built-in functions to find functions that could help.

# write function here
def return_num_characters(string):
    letters = 0
    for i in string:
        if i.isalpha():
            if  i.isascii() is True:
                letters += 1
    return letters

# 3. Create a function called bar_plot that draws a bar plot taking as input a list of numbers.
# and printing out bars. This function should ignore negative values and floating point values.
#Example:
#bar_plot([1,2,10])
#+
#++
#++++++++++

# write function here
def bar_plot(numbers):
    for i in numbers:
        if i > 0:
            print('+'*i)

def case_vowel_count(string_arg):
    string_arg = ' '.join(string_arg)
    vowel_count = return_num_vowels(string_arg)
    sys.stdout.write(f"a {vowel_count['a']}\n")
    sys.stdout.write(f"e {vowel_count['e']}\n")
    sys.stdout.write(f"i {vowel_count['i']}\n")
    sys.stdout.write(f"o {vowel_count['o']}\n")
    sys.stdout.write(f"u {vowel_count['u']}\n")
                     

def case_character_count(string_arg):
    string_arg = ' '.join(string_arg)
    character_count = return_num_characters(string_arg)
    sys.stdout.write(str(character_count))
                     
def case_bar_plot(list_arg):
    list_arg = map(int, list_arg[0].split(' '))
    bar_plot(list_arg)
                     
                     
if __name__ == '__main__':
    test_func_name = sys.stdin.readline().strip()
    test_func = globals()[test_func_name]
    arg = sys.stdin.readlines()
    test_func(arg)
