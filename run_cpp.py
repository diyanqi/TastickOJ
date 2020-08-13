import time
import timeout_decorator
import os

@timeout_decorator.timeout(1, use_signals=False)
def run(pro_num,testid):
    rst=os.system('./caj/code.sh <io_data/'+str(pro_num)+'/'+str(testid)+'.in >caj/code.out')
    if(rst==35584):
        return -1
    return 1
