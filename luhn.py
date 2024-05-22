import random

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def calculate_luhn_check_digit(card_number):
    test_number = card_number + "0"
    check_digit = luhn_checksum(test_number)
    return 0 if check_digit == 0 else 10 - check_digit

def generate_card_number(length=16, issuer="visa"):
    issuer_prefixes = {
        "visa": ["4"],
        "mastercard": ["51", "52", "53", "54", "55"],
        "amex": ["34", "37"],
        "discover": ["6011", "65"] + [str(i) for i in range(622126, 622926)] + [str(i) for i in range(644, 650)],
        "diners": ["36", "38"] + [str(i) for i in range(300, 306)],
        "jcb": [str(i) for i in range(3528, 3590)],
        "solo": ["6334", "6767"],
        "switch": ["4903", "4905", "4911", "4936", "564182", "633110"] + [str(i) for i in range(6333, 6760)],
        "maestro": ["5018", "5020", "5038", "5893", "6304", "6759", "6761"]
    }
    
    if issuer not in issuer_prefixes:
        raise ValueError("Unsupported issuer. Supported issuers: visa, mastercard, amex, discover, diners, jcb, solo, switch, maestro.")
    
    valid_lengths = {
        "visa": [13, 16],
        "mastercard": [16],
        "amex": [15],
        "discover": [16],
        "diners": [14],
        "jcb": [16],
        "solo": [16, 18, 19],
        "switch": [16, 18, 19],
        "maestro": list(range(12, 20))
    }
    
    if length not in valid_lengths[issuer]:
        raise ValueError(f"{issuer.capitalize()} card numbers must be {valid_lengths[issuer]} digits long.")
    
    prefix = random.choice(issuer_prefixes[issuer])
    base_number = [int(d) for d in prefix] + [random.randint(0, 9) for _ in range(length - len(prefix) - 1)]
    base_number_str = "".join(map(str, base_number))
    check_digit = calculate_luhn_check_digit(base_number_str)
    return base_number_str + str(check_digit)

# List of all issuers and their valid lengths
issuers_and_lengths = {
    "visa": [13, 16], # 19 is uncommon
    "mastercard": [16],
    "amex": [15],
    "discover": [16], # shows invalid
    "diners": [14],
    "jcb": [16],
    "solo": [16, 18, 19], # 19 uncommon
    "switch": [16, 18, 19], # all invalid
    "maestro": list(range(12, 20)) # only 16 works
}

# Generate card numbers for all combinations of issuers and lengths
card_numbers = []
for issuer, lengths in issuers_and_lengths.items():
    for length in lengths:
        card_number = generate_card_number(length=length, issuer=issuer)
        card_numbers.append((issuer.capitalize(), length, card_number))

# Print the generated card numbers with comments
for issuer, length, card_number in card_numbers:
    print(f"# Issuer: {issuer}, Length: {length}")
    print(card_number)
    print()
