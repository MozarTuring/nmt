import NeuHub_API_JDDC as jddc
import jieba

MAX_TOKENS = 600

def jieba_split(senten):
  sentence = []
  while len(senten) > MAX_TOKENS:
    sentence1 = jieba.cut(senten[:MAX_TOKENS])
    senten = senten[MAX_TOKENS:]
    sentence.extend(sentence1)

  sentence1 = jieba.cut(senten)
  sentence.extend(sentence1)

  return sentence

def jd_split(senten):
  sentence = []
  while len(senten) > MAX_TOKENS:
    sentence1 = jddc.parse(senten[:MAX_TOKENS])
    senten = senten[MAX_TOKENS:]
    sentence.extend(sentence1)

  sentence1 = jddc.parse(senten)
  sentence.extend(sentence1)
  sentence.append('\n')

  return sentence


def word_split(read_fi, write_fi, fn_split):
  with open(read_fi, 'r', encoding='utf-8') as rf:
    with open(write_fi, 'w', encoding='utf-8') as wf:
      line = rf.readline()
      t = 0
      while line:
        t += 1
        if t % 100 == 0:
          print(t)
        if line == '\n':
          line = rf.readline()
          continue
        split_line = fn_split(line)
        for i in split_line:
          if i != '\n':
            wf.write(i + ' ')
          else:
            wf.write(i)

        line = rf.readline()


if __name__ == '__main__':
  path = '/home/team447/notespace/data/single/'
  file_r = 'chat'
  suffix = '.dec'
  read_f = path + file_r + suffix
  func_split = jieba_split
  if func_split == jieba_split:
    write_f = 'jieba_split/' + file_r + suffix
  elif func_split == jd_split:
    write_f = 'jd_split/' + file_r + suffix
  else:
    print('invalid split function \n')
    sys.exit()

  word_split(read_f, write_f, func_split)

