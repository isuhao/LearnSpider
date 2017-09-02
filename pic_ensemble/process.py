import os 
import shutil
with open('new_down.txt', 'rb') as f:
    content_list=f.readlines()
    
    new_con=list(set(content_list))
with open('newest.txt', 'wb') as f:
    f.writelines(new_con)


    # try:

    #     dir_list.remove('name.txt')
    #     for dir_ in dir_list:
    #         print dir_

    #         shutil.copyfile(os.path.join(dirpath, dir_), os.path.join(os.getcwd(), dir_))
    #     print '--------------------'
    # except:
    #     pass