

def ppp():
    print("sdfgh")

def hash(info_arr):

    operation_counter = 1
    hash_out = 0
    counter_1 = 1
    counter_2 = 1


    for item in info_arr:
        hash_value = 0
        last_char_hash = 1
        for char in item[0]:
            last_char_hash = (ord(char) % 5)
            hash_value += last_char_hash ** counter_2
            counter_2 += 2
            operation_counter += 1

        counter_2 = last_char_hash + 3
        hash_value *= counter_1

        for char in item[1]:
            last_char_hash = (ord(char) % 5)
            hash_value += last_char_hash ** counter_2
            counter_2 += 2
            operation_counter += 1

        counter_2 = last_char_hash + 3
        hash_value *= counter_1
        hash_value %= operation_counter ** 6
        hash_out += hash_value
        operation_counter = 1
        counter_1 += 1

    if hash_out % 4 == 0:
        pass

    elif hash_out % 4 == 1:
        hash_out = int(str(hash_out)[len(str(hash_out)) // 2:] + str(hash_out)[:len(str(hash_out)) // 2])

    elif hash_out % 4 == 2:
        hash_out = int(str(hash_out)[len(str(hash_out)) - len(str(hash_out)) // 3:] + str(hash_out)[len(str(hash_out)) // 3:len(str(hash_out)) - len(str(hash_out)) // 3] + str(hash_out)[:len(str(hash_out)) // 3])

    elif hash_out % 4 == 3:
        hash_out = int(str(hash_out)[len(str(hash_out)) - len(str(hash_out)) // 4:] + str(hash_out)[len(str(hash_out)) // 4:len(str(hash_out)) - len(str(hash_out)) // 4] + str(hash_out)[:len(str(hash_out)) // 4])

    return hash_out
