# DAVIS BUSTEED -- LING 360

# Instructions:
# Write a Python program that uses regular expressions and the list data structure 
# to identify and count all of the nominalizations in a short text. Use the website 
# below or other resources to familiarize yourself with nominalizations. As input 
# to your program, you can simply paste a short text (300 or so words) into your .py file. 
# Write a short report in which you give the initial precision and recall accuracy 
# measurements of your program. Then, modify your program (probably just the regular expression) 
# and give the final precision and recall measurements of your program. Turn into the CMS a zipped 
# file (with extension .zip) with your .py file as well as your report in a .docx (Microsoft Word) file.
# http://www.dailywritingtips.com/nominalized-verbs/

# import the regex library
import re

# the text to search thru (toggle word wrap to easily view text)
text = '''
  After 2112, Rush went to the United Kingdom to record A Farewell to Kings (1977) and Hemispheres (1978) at Rockfield Studios in Wales. These albums saw the band members expanding the progressive elements in their music. "As our tastes got more obscure," lead singer Geddy Lee said in an interview, "we discovered more progressive rock-based bands like Yes, Van der Graaf Generator and King Crimson, and we were very inspired by those bands and their employees. They made us want to make our music more interesting and more complex and we tried to blend that with our own personalities to see what we could come up with that was indisputably us." Increased synthesizer use, lengthy songs, and highly dynamic playing featuring complex time signature changes became a staple of Rush's compositions. To achieve a broader, more progressive sound, Lifeson began to use classical and twelve-string guitars, and Lee added bass-pedal synthesizers and Minimoog. Likewise, Peart's percussion became diversified in the form of triangles, glockenspiel, wood blocks, cowbells, timpani, gong, and chimes. Beyond instrument additions, the band kept in stride with the progressive rock trends by continuing to compose long, conceptual songs with science fiction and fantasy overtones. As the new decade approached, Rush gradually began to dispose of its older styles of music in favour of shorter and sometimes softer arrangements. The lyrics up to this point were heavily influenced by classical poetry, fantasy literature, science fiction, and the writings of writer Ayn Rand, as exhibited most prominently by their 1975 song "Anthem" from Fly By Night and a specifically acknowledged derivation in 2112 (1976). Permanent Waves (1980) shifted Rush's style of music with the introduction of reggae and new wave elements. Although a hard rock style was still evident, more synthesizers were introduced. Moreover, because of the limited airplay Rush's previous extended-length songs received, Permanent Waves included shorter, more radio-friendly songs such as "The Spirit of Radio" and "Freewill", two songs that helped Permanent Waves become Rush's first US Top 5 album. Meanwhile, drummer Neil Peart's lyrics shifted toward an expository tone with subject matter that dwelled less on fantastical or allegorical story-telling and more heavily on topics that explored humanistic, social, and emotional elements. 
  '''

# initial list of regexes for testing
# regex = [
#   r'\b\w+[eo]r\b',
#   r'\b\w+ion\b', 
#   r'\b\w+ment\b', 
#   r'\b\w+e{2}\b', 
#   r'\b(use|change)\b', 
#   r'\b\w+ing\b'
# ]

# adjusted regexes after intial testing
regex = [
  r'\b\w+[eo]rs?\b',
  r'\b\w+ions?\b',
  r'\b\w+(?<!ele)ments?\b',
  r'\b\w{2,}e{2}s?\b',
  r'(?<!to)\W(uses?|changes?)\b',
  r'\b\w{2,}ings?\b',
]

# create an empty list to add results to
results = []

# lopp thru the list of regexes 
# 'r' will refer to a single regex string
for r in regex:

  # for each regex string, do a case-insensitive search of the text
  # because re.findall() returns a list, we will loop thru its results, where 'res' will refer to each individual result.
  # if no match is made, an empty list will be returned, and no traversal will be performed.
  for res in re.findall(r, text, re.I):
    
    # add the individual results to the list of results
    results.append(res)


# print the number of results we found, as well as the list of results
print(f'\nFound {len(results)} nominalizations.\n')
print(f'Results: {results}\n')