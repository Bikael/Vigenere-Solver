import string
import math
from rich import print


# Frequencies of each letter in the english alphabet in order
expected_frequencies = [
    0.084966, 0.020720, 0.045388, 0.033844, 0.111607, 0.018121, 0.024705, 0.030034, 
    0.075448, 0.001965, 0.011016, 0.054893, 0.030129, 0.066544, 0.071635, 0.031671, 
    0.001962, 0.075809, 0.057351, 0.069509, 0.036308, 0.010074, 0.012899, 0.002902, 
    0.017779, 0.002722]


def index_of_coincidence(group):
    total = 0
    N = len(group)

    occurrences = dict.fromkeys(string.ascii_lowercase, 0)
    
    # counts occurrences
    for letter in group:
        occurrences[str(letter)] += 1
    
    # formula for index of coincidence
    for key in occurrences:
        n = occurrences[key]
        total += (n/N) * ((n-1)/(N-1))
        
    return total

def group_maker(cipher_text, key_length):
    count = 0
    groups = []
    
    # list of lists with key_length number of nested lists
    for _ in range(key_length):
        groups.append([])

    # Divides the cipher_text into key_length number of groups
    for letter in cipher_text:
        if count == key_length:
            count = 0
        groups[count].append(letter)
        count +=1

    return groups

def finding_shift(group):

    # Dictionary of all lower case letters as keys
    occurrences = dict.fromkeys(string.ascii_lowercase, 0)
    actual_frequencies = {}
    sums = []
    count = 0 
    total = 0


    for letter in group:
        occurrences[letter] += 1  
    for key in occurrences:
        actual_frequencies[key] = occurrences[key]/ len(group)


    for _ in range(len(expected_frequencies)):
        for key in actual_frequencies:
            total += (actual_frequencies[key] * expected_frequencies[count])
            count += 1
        expected_frequencies.insert(0, expected_frequencies.pop())
        sums.append(total)
        total = 0
        count = 0

    shift_value = (sums.index(max(sums)))
    
    return shift_value

def average_ICs(cipher_text, key_length, groups):

    total = 0
    average_IC = 0
    num_groups = key_length
    for group in groups:
        total += index_of_coincidence(group)
    average_IC = total/num_groups
    print (f"num_groups: {num_groups} average_IC: {average_IC}")
    return average_IC
       
def numbers_to_word(numbers):
    # Convert a list of numbers into a word, where 0 = 'a', 1 = 'b', etc.
    word = ''.join(chr(num + ord('a')) for num in numbers)
    return word

def decrypt(cipher_text, shifts):
    deciphered_list = []
    count = 0
    
    for letter in cipher_text:
        curr_key_shift = shifts[count % len(shifts)]
        if (ord(letter) - curr_key_shift) < 97:
            remainder = (96 - (ord(letter) - curr_key_shift))
            deciphered_list.append(chr(ord('z') - remainder))
        else:
            deciphered_list.append(chr(ord(letter) - curr_key_shift))
        count += 1

    deciphered_text = ''.join(deciphered_list)
    return deciphered_text

def encrypt(plain_text, key):
    enciphered_text = []
    count = 0 

    for letter in plain_text:
        shift = ord(key[count]) - ord('a')
        e_letter = ord(letter) + shift
        if e_letter > ord('z'):
            e_letter = chr(e_letter % ord('z') + 96)
            enciphered_text.append(e_letter)
        else:
            enciphered_text.append(chr(e_letter))
        count += 1
        if count == len(key) :
            count = 0
    
    return ''.join(enciphered_text)

def main():

    cipher_texts = ["aufegrmchehvoohoeymgrtuxhcxtjipkksjevgnuuxdkwcqzetidvlecrioeluergwhqgkghaphpwdzniddctjmsdsxgviptatxieylcviuvenycvenvxocgcgttvliu","gicavbrvhlvfwfoaeqdsnpdepfpegstlfngirtvoeqcssmhrvpnpliifjelzusptelufdhpbpisaonylvehrhiyofrrftsmtmnnlaisayaszubtvebzuctuctymttygdbcjegnytviifronsftsknltmyugczcmdogacqunboocmieykfemehvuhpieshrtzbiefmywmuohvahqmdjjozxjnzcjzzuhvtddbirrytsmcozdtzbiettofveaafrlvgoeyacluhequrpuhruelwgshfdpvmystokmoszklpaqrbutpboipxorwojrntkebsaqtlxmenuaybtitjtpdfnsqrzbieexorwosukssqhhyadzufdaqspzpsrjirpbbbxelanaynptohysqrppfaqjidlbrxirpmorhdbpzzsxknhittukcvmoohihqwshvotzxmalvhpobmrqfgwhoaeigqmsrtvtkfpbnieqdsnpdatbyvvwptmaafwlbfrctoznfnbwgsnprukmewtuexigmjnqgftvjtrnylbtenfeabisbhuabpagjofabnqhepbxigjnzqmlrhfpkusaqtepbtugegmswrptdejmzknrwgcbwrdmiifdudgtcugdftfwbwlovptnnlzejtugwlauhryajpfwnubpkbufgbttmibpsznzentslopwugnepfvbioyaiaqhicaucecwwmeohvoqbiefnurojsurrtufvnnspitosxoraqhrtelvehnfllqopnpttvhaafhpiwiaioybiecnaymusikrrqosuqrpaxhrptsmgieutcizsbhtsmcrvihegpuaivzotoyuuypbdfjoymbceqsdbiezvhlbnoepiyojtjcslajfgjeqwscruoqmwoywttwoaquixxmytkvpvvpbptsmntugrpiodgjeypbdgwrymeafkdpqodvugfauaafwcqutrptsmnoshadioutnylveuahocbvnnvexqttnmeepfyagv","ksjsuapgbttalfcjngbgrupoizeluconifrjepmvfdooybhxbccbiufibojoszuluconrfnkqwnynrfmvexbmrifivtuapniennedfvdgecvieqpvdoczpgncnihznotcjqzeaflaruccbocxcmonrppcaanhainpteixvvpdcwlgqpbxphwlgchwytjfktavagbovopbongvmbbsjumksdvadwaqzcjiatazqzxjliskllvvbyqpwkcvlzecdal"]
    
    max_key_length = int(input("Choose a max key length (must be shorter than the ciphertext): "))
    arg = int(input("Which cipher-text would you like to use (0,1,2): "))
    
    shifts = []
    # process the ciphertext
    cipher_texts[arg] = cipher_texts[arg].replace(" ", "").lower()

    for key_length in range(1, max_key_length):

        # divide the ciphertext into groups of the key_length
        groups = group_maker(cipher_texts[arg], key_length)
    

        # list the average index coincidences to see the pattern
        avg_IC = average_ICs(cipher_texts[arg], key_length, groups)
        
        if math.floor(avg_IC * 100)/100.0 >= 0.05:
            for group in groups:
                shifts.append(finding_shift(group))

            key = numbers_to_word(shifts)

            print(key)

            print(decrypt(cipher_texts[arg],shifts))
            
            correct = input("Was this correct (y/n): ")
            if correct.lower() == "y":
                break
            else: 
                print("Continuing")

if __name__ == '__main__' :
    main()

