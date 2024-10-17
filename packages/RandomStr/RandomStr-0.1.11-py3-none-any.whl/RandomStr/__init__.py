import time

def generate(length):
    # Define the characters to use in the random string (letters, digits, and special characters)
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789^7]|\\/2*@#"
    string = ""
    # Use the current time in microseconds to seed the randomness
    seed = int(time.time() * 1000000)
    
    # Generate a random string of the specified length
    for i in range(length):
        # Update the seed to produce a pseudo-random number using the loop index and current time
        seed = (seed * (i + 1) + int(time.time() * 1000)) % 1000
        # Get a pseudo-random index based on the updated seed
        index = seed % len(characters)
        # Append the selected character to the random string
        string += characters[index]
    
    # Print the generated random string
    print(string)