import re, os
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
    if re.findall('\((\d+)\)', file_name):
        num = re.findall('\((\d+)\)', file_name)
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

def file_zip_path(input_path, output_path, ignore=[]):
    outdir = os.path.dirname(output_path)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    f = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)

    filepathlists = []
    filenamelists = []
    _dfs_zip_file(input_path, filepathlists, filenamelists, ignore)

    for file in filepathlists:
        file = file.replace('\\', '/')
        input_path = input_path.replace('\\', '/')
        f.write(file, file.replace(input_path, ''))
    f.close()
    return output_path

def _dfs_zip_file(input_path, resultpath, resultfile, ignore=[]):
    files = os.listdir(input_path)

    for file in files:
        filepath = os.path.join(input_path, file)

        if os.path.isdir(filepath):
            _dfs_zip_file(filepath, resultpath, resultfile, ignore)
        else:
            count = 0
            for one in ignore:
                if one in file:
                    count += 1
            if count == len(ignore):
                resultpath.append(filepath)
                resultfile.append(file)

def _dfs_current_folder(input_path, resultpath, resultfile, ignore=[]):
    files = os.listdir(input_path)

    for file in files:
        filepath = os.path.join(input_path, file)
        if os.path.isdir(filepath):
            continue
        else:
            count = 0
            for one in ignore:
                if one in file:
                    count += 1
            if count == len(ignore):
                resultpath.append(filepath)
                resultfile.append(file)

def current_folder_file_copy(input_path, copy_to_path, ignore=[], rename=None):

    filepathlists = []
    filenamelists = []
    _dfs_current_folder(input_path, filepathlists, filenamelists, ignore)
    s = ''
    for file in filepathlists:
        dirs_f = os.path.dirname(file)
        dirs_t = dirs_f.replace(input_path, copy_to_path)
        os.makedirs(dirs_t, exist_ok=True)

        name = ntpath.basename(file)
        name_tmp = ntpath.basename(file)
        f = file_copy(dirs_f, name, name_tmp, dirs_t, rename)
        if s == '':
            s = s + f
        else:
            s = s + ',' + f
    return s

def file_and_folder_copy(input_path, copy_to_path, ignore=[], rename=None):

    filepathlists = []
    filenamelists = []
    _dfs_zip_file(input_path, filepathlists, filenamelists, ignore)
    s = ''
    for file in filepathlists:
        dirs_f = os.path.dirname(file)
        dirs_t = dirs_f.replace(input_path, copy_to_path)
        os.makedirs(dirs_t, exist_ok=True)

        name = ntpath.basename(file)
        name_tmp = ntpath.basename(file)
        f = file_copy(dirs_f, name, name_tmp, dirs_t, rename)
        if s == '':
            s = s + f
        else:
            s = s + ',' + f
    return s

if __name__ == '__main__':
    pass
