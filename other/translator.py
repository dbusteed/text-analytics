from googletrans import Translator

t = Translator()

while True:
  wors = input('\n?: ')

  print('\n'+t.translate(wors).text)

  if wors == 'q':
    break