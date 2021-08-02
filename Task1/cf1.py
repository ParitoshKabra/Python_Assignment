s = input()
s = s.lower()
sTemp = str(s)
vowels = "aeioyu"
for i in range (len(sTemp)):
    # print(s[i])
    if vowels.find(sTemp[i]) != -1:
        # print("yes")
        s = s.replace(sTemp[i], "")
# print(s)
characterr = '.'
sTemp = characterr.join(s)
print("."+sTemp)