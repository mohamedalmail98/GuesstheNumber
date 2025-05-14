import random

print("🎲 I'm thinking of a number between 1 and 100.")
number = random.randint(1, 100)
max_guesses = 4

for attempt in range(1, max_guesses + 1):
    guess = input(f"Attempt {attempt}/{max_guesses} - Your guess: ")
    
    if not guess.isdigit():
        print("⚠️ Please enter a valid number.")
        continue

    guess = int(guess)

    if guess < number:
        print("Too low ⬇️")
    elif guess > number:
        print("Too high ⬆️")
    else:
        print("🎉 Correct! You guessed the number!")
        break
else:
    print(f"❌ Out of guesses! The number was {number}.")