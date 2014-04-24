# def ReadEdgeId()
import os

def ReadEdgeId(path):
    f=open(path)
    content=f.readlines()
    f.close()
    # print(content)
    records=content[1:]
    print(records[0])
    edge_ORIGFID=map(lambda record:int(record.split(',')[-1]),records)
    print(len(edge_ORIGFID))

if __name__=='__main__':
    path='E:/tmp/edge.txt'
    ReadEdgeId(path)