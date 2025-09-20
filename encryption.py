import random


def string_to_int(s):
    match s:
        case "simon": return 0
        case "eden": return 1
        case "guy": return 2
        case "shira": return 3
        case "yaheli": return 4
    return None

    #return int.from_bytes(s.encode(), 'big')

def int_to_string(n):
    #byte_length = (n.bit_length() + 7) // 8
    #return n.to_bytes(byte_length, 'big').decode()
    match n:
        case 0: return "simon"
        case 1: return "eden"
        case 2: return "guy"
        case 3: return "shira"
        case 4: return "yaheli"
    return None

def encrypt_vote(name, Group, public_key):
    r = random.randint(1, 100)
    m = string_to_int(name)
    return Group.pow(Group.get_generator(), r), Group.operation(Group.pow(public_key,r), m)

def decrypt_vote(Group, num, encrypted_vote, private_key):
    inverse = Group.inverse(Group.pow(num, private_key))
    return int_to_string(Group.operation(inverse, encrypted_vote))