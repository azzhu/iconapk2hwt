# coding utf-8
'''
create by bigzhu
qq:228812066
2018.2.24
'''

import os
import shutil
import zipfile
import tarfile

# param
ind = []


def read_ind():
    global ind
    with open('ind.txt', 'r') as f:
        lines = f.readlines()
        le = len(lines)
        for i in range(le):
            line = lines[i]
            rows = line.split('\n')[0].split(',')
            if len(rows) == 3:
                ind.append(rows[0] + ',' + rows[1] + '.png,' + rows[2] + '.png')


def delDir(delDir):
    delList = os.listdir(delDir)

    for f in delList:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
            # print(filePath + " was removed!")
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
        # print("Directory: " + filePath + " was removed!")


def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


def make_targz(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


if __name__ == '__main__':
    # 准备数据，解压
    z = zipfile.ZipFile('theme.hwt', 'r')
    z.extractall(path='theme/')
    z.close()
    print('theme.hwt exted.')
    z2 = zipfile.ZipFile('theme/icons', 'r')
    z2.extractall(path='icons/')
    z2.close()
    print('icon exted.')
    fnlist = os.listdir('icons')
    for f in fnlist:
        if 'icon_' not in f:
            os.remove('icons/' + f)
    print('del somepng.')
    z3 = zipfile.ZipFile('icon.apk', 'r')
    z3.extractall(path='.apk/')
    z3.close()
    print('apk exted.')

    src_s = '.apk/res/drawable-nodpi-v4/'
    dst_s = 'icons/'

    read_ind()
    # print(ind)

    srcfs = []
    for fn in os.listdir(src_s):
        srcfs.append(fn)

    e0, e1, e2 = 0, 0, 0
    notmatchlist = []

    tol = len(ind)
    for i in range(tol):
        match = False
        vs = ind[i].split(',')
        appname, srcf, dstf = vs[0], vs[1], vs[2]
        if srcf in srcfs:
            oldfn = src_s + srcf
            newfn = dst_s + dstf
            shutil.copyfile(oldfn, newfn)
            e0 += 1
            match = True
        elif 'huawei_' in srcf:
            srcf_ = srcf.split('_')[1]
            if srcf_ in srcfs:
                oldfn = src_s + srcf_
                newfn = dst_s + dstf
                shutil.copyfile(oldfn, newfn)
                e1 += 1
                match = True
        else:
            for j in range(len(srcfs)):
                if srcf in srcfs[j]:
                    oldfn = src_s + srcfs[j]
                    newfn = dst_s + dstf
                    shutil.copyfile(oldfn, newfn)
                    e2 += 1
                    match = True
                    break
        if match == False:
            notmatchlist.append(appname)

    # 压缩
    make_zip('icons/', 'theme/icons')
    make_zip('theme/', 'theme_new.hwt')
    delDir('.apk/')
    delDir('icons/')
    delDir('theme/')
    os.rmdir('.apk/')
    os.rmdir('icons/')
    os.rmdir('theme/')

    print('\nfinished!')
    print("total:{}\ne0:{}\ne1:{}\ne2:{}\nnot match:{}".format(len(ind), e0, e1, e2, len(ind) - e0 - e1 - e2))
    if len(notmatchlist) > 0:
        print('not match list:')
        print(notmatchlist)
