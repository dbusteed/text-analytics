def check_anagram(s1, s2):
  if sorted(list(s1.lower().replace(' ',''))) == sorted(list(s2.lower().replace(' ',''))):
    return True
  else:
    return False


s1 = input('First string?: ')
s2 = input('Second string?: ')

print(check_anagram(s1, s2))
