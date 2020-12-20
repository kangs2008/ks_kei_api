import re, os
import glob
import shutil

import zipfile
import ntpath

def file_copy(file_path, file_name, file_tmp, copy_to_path, rename=None):

    tmpf = os.path.join(file_path, file_tmp)
    tmpf = tmpf.replace('\\', '/')

    if rename:
        path_list = file_name.split('.')
        file_name = path_list[0] + '_report.' + path_list[1]
        tmpt = os.path.join(copy_to_path, file_name)
    else:
        tmpt = os.path.join(copy_to_path, file_name)
        tmpt = tmpt.replace('\\', '/')

    if not os.path.exists(tmpt):
        shutil.copy(tmpf, tmpt)
        return file_name
    num = 1
    if re.findall('\((\d)\)', file_name):
        num = re.findall('\((\d)\)', file_name)
        new_num = int(num[0]) + 1
        file_name = file_name.replace(num[0], str(new_num))
        return file_copy(file_path, file_name, file_tmp, copy_to_path)
    path_list = file_name.split('.')

    if rename:
        if '_report' in path_list[0]:
            file_name = path_list[0] + f'({num}).' + path_list[1]
        else:
            file_name = path_list[0] + '_report' + f'({num}).' + path_list[1]
    else:
        file_name = path_list[0] + f'({num}).' + path_list[1]

    return file_copy(file_path, file_name, file_tmp, copy_to_path)


def file_unzip(file_name: str, dir_name):
    try:
        name = ntpath.basename(file_name)
        new = os.path.splitext(name)[0]
        dir_name = os.path.join(dir_name, new)
        file = zipfile.ZipFile(file_name)
        file.extractall(dir_name)
        file.close()
        # 递归修复编码
        # __rename(dir_name)
    except:
        print(f'{file_name} unzip fail')

def __rename(pwd: str, file_name=''):
    path = f'{pwd}/{file_name}'
    if os.path.isdir(path):
        for i in os.scandir(path):
            __rename(pwd, i.name)
    newname = file_name.encode('cp437').decode('gbk')
    os.rename(path, f'{pwd}/{newname}')

def file_del(filepath):
    del_list = os.listdir(filepath)

    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def _dfs_zip_file(input_path, result, ignore=[]):
    files = os.listdir(input_path)

    for file in files:
        filepath = os.path.join(input_path, file)

        # if file in ignore:
        #     continue
        if os.path.isdir(filepath):
            _dfs_zip_file(filepath, result, ignore)
        else:
            if ignore != []:
                if str(ignore[0]) not in file:
                    continue
            result.append(filepath)

def file_zip_path(input_path, output_path, ignore=[]):
    outdir = os.path.dirname(output_path)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    f = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)

    filelists = []
    _dfs_zip_file(input_path, filelists, ignore)

    for file in filelists:
        file = file.replace('\\', '/')
        input_path = input_path.replace('\\', '/')
        f.write(file, file.replace(input_path, ''))
    f.close()
    return output_path

def file_and_folder_copy(input_path, copy_to_path, ignore=[], rename=None):

    filelists = []
    _dfs_zip_file(input_path, filelists, ignore)
    # print(filelists)
    for file in filelists:
        dirs_f = os.path.dirname(file)
        dirs_t = dirs_f.replace(input_path, copy_to_path)
        os.makedirs(dirs_t, exist_ok=True)

        name = ntpath.basename(file)
        name_tmp = ntpath.basename(file)

        file_copy(dirs_f, name, name_tmp, dirs_t, rename)










if __name__ == '__main__':
    file_path = r'C:\Users\kangs\Desktop\yoyo\1'
    file_name = r'新建 DOC 文档.doc'
    copy_to_path = r'C:\Users\kangs\Desktop\yoyo\2'
    output_path = r'C:\Users\kangs\Desktop\yoyo\2\aa.zip'
    # file_del(copy_to_path)
    # file_copy(file_path, file_name, file_name, copy_to_path, rename='1')
    # file_zip_path(file_path, output_path, ignore=[])
    # pass
    # file_del(copy_to_path)
    file_and_folder_copy(file_path, copy_to_path, ignore=['t_'], rename='1')
