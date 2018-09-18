import jieba

MAX_TOKENS = 600
def basic_tokenizer(senten):
  """Very basic tokenizer: split the sentence into a list of tokens."""
  words = []
  sentence = []
  while len(senten) > MAX_TOKENS:
    sentence1 = jieba.cut(senten[:MAX_TOKENS])
    senten = senten[MAX_TOKENS:]
    sentence.extend(sentence1)

  sentence1 = jieba.cut(senten)
  sentence.extend(sentence1)
  for i in range(len(sentence)):
    if isinstance(sentence[i], str):
        word = str.encode(sentence[i])
    else:
        word = sentence[i]
    words.append(word.decode("utf-8"))
  return words


if __name__=='__main__':
	stri = '我们喜欢'
	stri_en = stri.encode('utf-8')
	j_stri=jieba.cut(stri)
	j_stri_en=jieba.cut(stri_en)
	for i in j_stri:
		print(i)

	for i in j_stri_en:
		print(i)