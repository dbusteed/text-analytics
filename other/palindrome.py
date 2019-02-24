# palindrone fun

def palindrome(n):
  if n.lower() == n.lower()[::-1]:
    return True
  else:
    return False

word = input('\nword?: ')

print(palindrome(word))