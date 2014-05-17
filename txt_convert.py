import os
# translate txt content of ['1', '2'] into [1,2]
f=open('E:/qkj/split/south-west/exp_ids.txt')
id=map(lambda x:int(x.strip()[1:-1]),f.readlines()[0][1:-1].split(','))
f.close()
#print(id)
f=open('E:/qkj/split/south-west/exp_ids.txt','w')
f.writelines(str(id))
f.close()