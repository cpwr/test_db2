import sys
sys.setrecursionlimit(1001)  # don't try this at home


def handle_numbers1(num1: int, num2: int, num3: int) -> int:
    return len(list(filter(lambda x: x % num3 == 0, range(num1, num2 + 1))))


def handle_numbers2(num1, num2, num3):
    return sum(1 for _ in range(num1, num2 + 1) if _ % num3 == 0)


def handle_numbers3(num1, num2, num3):
    return len([x for x in range(num1, num2 + 1) if x % num3 == 0])


def handle_numbers4(num1, num2, num3):
    count = 0
    while num1 <= num2 + 1:
        if num1 % num3 == 0:
            count += 1
        num1 += 1
    return count


def handle_numbers5(num1, num2, num3, acc=0):
    if num1 % num3 == 0:
        acc += 1
    if num1 == num2:
        return acc
    return handle_numbers5(num1 + 1, num2, num3, acc)


# if the string is needed as a desired result
def handle_numbers6(num1, num2, num3):
    numbers_gen = (x for x in range(num1, num2 + 1) if x % num3 == 0)
    return (
        f"{sum(1 for _ in numbers_gen)}, because"
        f" {', '.join(map(lambda x: str(x), numbers_gen))}"
        f" are divisible by {num3}"
    )
