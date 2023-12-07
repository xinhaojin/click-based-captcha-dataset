import random
import os

def split_data(data, ratios):
    """
    Split the data array into three parts according to given ratios.
    Args:
        data: the array to split.
        ratios: a tuple containing the ratios of the split, e.g. (0.7, 0.15, 0.15).
    Returns:
        A tuple of three arrays: train, val, and test.
    """
    # Get the number of items in each part
    train_size = int(len(data) * ratios[0])
    val_size = int(len(data) * ratios[1])
    test_size = len(data) - train_size - val_size

    # Randomly shuffle the data
    random.shuffle(data)

    # Split the data into three parts
    train = data[:train_size]
    val = data[train_size:train_size + val_size]
    test = data[train_size + val_size:]

    return train, val, test
#3100网易汉字+1200极验汉字+2000网易图标
arr1 = list(range(1, 3101))
arr2 = list(range(10001, 11201))
arr3 = list(range(20001, 22001))

train_lists=[]
val_lists=[]
test_lists=[]

train_list,val_list,test_list=split_data(arr1,(0.7,0.15,0.15))
train_lists.extend(train_list)
val_lists.extend(val_list)
test_lists.extend(test_list)

train_list,val_list,test_list=split_data(arr2,(0.7,0.15,0.15))
train_lists.extend(train_list)
val_lists.extend(val_list)
test_lists.extend(test_list)

train_list,val_list,test_list=split_data(arr3,(0.7,0.15,0.15))
train_lists.extend(train_list)
val_lists.extend(val_list)
test_lists.extend(test_list)

if not os.path.exists('ImageSets'):
    os.mkdir('ImageSets')
    os.mkdir('ImageSets/Main')
train=open('ImageSets/Main/train.txt','w')
val=open('ImageSets/Main/val.txt','w')
test=open('ImageSets/Main/test.txt','w')
for i in train_lists:
    train.write(str(i).zfill(5)+'\n')
for i in val_lists:
    val.write(str(i).zfill(5)+'\n')
for i in test_lists:
    test.write(str(i).zfill(5)+'\n')
train.close()
val.close()
test.close()
