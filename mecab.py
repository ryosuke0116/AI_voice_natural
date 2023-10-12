import MeCab
import csv
a = MeCab.Tagger("-Owakati")
print(a.parse("pythonが大好きです").split())
tagger = MeCab.Tagger()
print(tagger.parse("pythonが大好きです").split())

with open("memo.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(a.parse("pythonが大好きです").split())