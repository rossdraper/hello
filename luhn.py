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
    check_digit = luhn_checksum(card_number + "0")
    return 0 if check_digit == 0 else 10 - check_digit

def generate_visa_card_number():
    base_number = [4] + [random.randint(0, 9) for _ in range(14)]  # 15 digits starting with 4
    check_digit = calculate_luhn_check_digit("".join(map(str, base_number)))
    return "".join(map(str, base_number)) + str(check_digit)

# Generate 4 Visa card numbers
visa_card_numbers = [generate_visa_card_number() for _ in range(4)]

# Print the generated Visa card numbers
for card_number in visa_card_numbers:
    print(card_number)

