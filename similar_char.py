import random

# 字符相似性字典
similar_characters = {'a': ['а'],
                      'c': ['с'],
                      'd': ['𝖽'],
                      'e': ['е'],
                      'g': ['ɡ'],
                      'h': ['հ'],
                      'i': ['і'],
                      'j': ['ј'],
                      'k': ['κ'],
                      'm': ['𝗆'],
                      'n': ['ᥒ'],
                      'o': ['ο'],
                      'p': ['р'],
                      'r': ['𝗋'],
                      's': ['ѕ'],
                      'x': ['х'],
                      'y': ['у'],
                      'A': ['Α'],
                      'B': ['В'],
                      'C': ['С'],
                      'E': ['Ε'],
                      'H': ['Η'],
                      'I': ['Ι'],
                      'J': ['Ј'],
                      'K': ['Κ'],
                      'M': ['М'],
                      'N': ['Ν'],
                      'O': ['Ο'],
                      'P': ['Ρ', 'Р'],
                      'T': ['Τ'],
                      'X': ['Х', 'Χ'],
                      'Y': ['Υ'],
                      'Z': ['Ζ', ]
                      }

for key in similar_characters:
    if key in similar_characters[key]:
        similar_characters[key].remove(key)
    similar_characters[key] = list(set(similar_characters[key]))
print(similar_characters)


def get_random_similar_character(input_char):
    if input_char.isalpha() and len(input_char) == 1:
        if input_char in similar_characters:
            similar_list = similar_characters[input_char]
            return random.choice(similar_list)
        else:
            return f"No similar characters found for '{input_char}'."
    else:
        return "Please enter a single alphabetical character (a-z or A-Z)."


# 示例用法
input_char = input("请输入一个字符 (a-z 或 A-Z)：")
similar_char = get_random_similar_character(input_char)
print(f"输入字符 '{input_char}' 的一个随机相似字符是 '{similar_char}'")

# filename = ""
# for key in similar_characters:
#     filename += similar_characters[key][0]
# with open('./%s.txt' % filename, 'a') as f:
#     f.write()
