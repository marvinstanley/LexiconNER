import re

filenames = ['train', 'test', 'valid']
prev_empty = False

#FLAG
LIMIT_DATASET = FALSE

#Limit Data Size
train_size = 300000
valid_size = 100000
test_size = 100000

for filename in filenames:

  with open('data/conll2003/ori_{}.txt'.format(filename), 'r', encoding='utf-8') as f, \
      open('data/conll2003/{}.PER.txt'.format(filename), 'w', encoding='utf-8') as fp, \
      open('data/conll2003/{}.LOC.txt'.format(filename), 'w', encoding='utf-8') as fl, \
      open('data/conll2003/{}.ORG.txt'.format(filename), 'w', encoding='utf-8') as fo, \
      open('data/conll2003/{}.txt'.format(filename), 'w', encoding='utf-8') as fw:
    for i, line in enumerate(f):
      if LIMIT_DATASET:
        if filename == 'train' and i >= train_size:
          break
        elif filename == 'test' and i>= test_size:
          break
        elif filename == 'valid' and i>= valid_size:
          break

      if '\t' in line:
        prev_empty = False
        splits = line.split()
        splits[0] = re.sub('à', 'a', splits[0])

        # If somehow whitespaces are labeled as unmasked token
        if len(splits) < 2:
          continue

        if 'LOC' in splits[1]:
          unlabeled = [fw, fp, fo]
          labeled = [fl]
        elif 'ORG' in splits[1]:
          unlabeled = [fw, fp, fl]
          labeled = [fo]
        elif 'PER' in splits[1]:
          unlabeled = [fw, fl, fo]
          labeled = [fp]
        else:
          unlabeled = [fw, fp, fl, fo]
          labeled = []
        
        for lab in unlabeled:
          lab.write(' '.join(splits + [str(0)]) + '\n')

        for lab in labeled:
          lab.write(' '.join(splits + [str(1)]) + '\n')
      else:
        if not prev_empty:
          prev_empty = True
          fw.write('\n')
          fp.write('\n')
          fo.write('\n')
          fl.write('\n')

  print('{} files done!'.format(filename))
