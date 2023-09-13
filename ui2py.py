"""
ui文件转py文件
blog: https://www.cnblogs.com/linyfeng/p/8207149.html
"""
import os
import os.path

# UI文件所在的路径
DIR_ROOT = './'

"""
from pathlib import Path
获得当前文件路径
Path(__file__).resolve()
.parents获取上一级目录
Path(__file__).resolve().parents[2]

后缀名 截断
os.path.splitext(filename)
"/" 截断
os.path.split(filename)
"""

# 保存目录下的所有ui文件
def listUiFile():
    dir_list = []
    files = os.listdir(DIR_ROOT)
    for filename in files:
        if os.path.splitext(filename)[1] == '.ui':
            dir_list.append(filename)
    return dir_list


# 后缀为ui的文件改成后缀为py的文件
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


# 调用系统命令把ui转换成py
def runMain():
    dir_list = listUiFile()
    for uifile in dir_list:
        pyfile = transPyFile(uifile)
        cmd = 'pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyfile, uifile=uifile)
        os.system(cmd)
        print("{uifile} -> {pyfile}转换成功".format(uifile=uifile, pyfile=pyfile))


if __name__ == "__main__":
    runMain()
