# ファイルをオープンする
test_data = open("frag1ToTestInfo.txt", "r")

# 行ごとにすべて読み込んでリストデータにする
lines = test_data.readlines()
# print(lines)
# 一行ずつ表示する
newLines = []
for line in lines:
    line = line.replace('\n','')
    newLines.append(line)
    # print(line)
print(newLines)

for l in newLines:
    if l.startswith('C') == True:
        print(l)

# ファイルをクローズする
test_data.close()