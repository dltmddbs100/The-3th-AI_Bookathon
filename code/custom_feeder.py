# data feeder method
def _sent_custom_append(self, text, length):
 sentences = split_text_into_sentences(text)
 sentences_tokenized = self.tokenizer.tokenize(sent) for sent in sentences if sent is not '']
 
 begin_index = 0
 
 selected_sents = sentences_tokenized[begin_index:]
 
 token_ids = self.tokenizer.convert_tokens_to_ids([token for sent in selected_sents for token in sent])
 while len(token_ids) < length:
  appending_text = random.choice(self.text_files).read_text(encoding='utf-8')
  token_ids += self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(appending_text))
  
 return token_ids[:length]