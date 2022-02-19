# Скрипт предназначен для запуска в случае обновления фронт-энда.

from os import listdir
from os.path import isdir, exists
from shutil import copy as copy_file, copytree, rmtree

path_to_front_end = input("Введите абсолютный путь к папке dist из Vue.js проекта: ")
path_to_back_end = input("Введите абсолютный путь к папке flask из проекта: ")

if path_to_front_end[-1] != "/":
    path_to_front_end = path_to_front_end + "/"
if path_to_back_end[-1] != "/":
    path_to_back_end = path_to_back_end + "/"


# Проверка на наличие самих директорий.
if not exists(path_to_front_end):
    print("Путь к ФРОНТУ не существует.")
    exit(-1)
if not exists(path_to_back_end):
    print("Путь к БЭКУ не существует.")
    exit(-1)
if not isdir(path_to_front_end):
    print("ФРОНТ должен быть директорией, а не файлом.")
    exit(-1)
if not isdir(path_to_back_end):
    print("БЭК должен быть директорией, а не файлом.")


# Проверка на корректность директорий по наименованию и наличию обязательных параметров.
if "dist/" != path_to_front_end[-5:]:
    print("ПРЕДУПРЕЖДЕНИЕ: указанный путь не заканчивается на dist.\n"
          "Если эта директория была переименована -- игнорируйте.\n"
          "Если этой директории не было в проектных файлах -- изучите npm run generate.")
if "static" not in listdir(path_to_back_end):
    print("ПРЕДУПРЕЖДЕНИЕ: указанный путь не имеет в себе папки static.\n"
          "Если эта директория была удалена намеренно -- игнорируйте.\n"
          "Если этой директории не было в проектных файлах -- проверьте, является "
          "ли указанная директория нужной.")
if "templates" not in listdir(path_to_back_end):
    print("ПРЕДУПРЕЖДЕНИЕ: указанный путь не имеет в себе папки templates.\n"
          "Если эта директория была удалена намеренно -- игнорируйте.\n"
          "Если этой директории не было в проектных файлах -- проверьте, является "
          "ли указанная директория нужной.")


may_we_continue = input("Продолжаем?(y/n) ")

if may_we_continue != "y":
    exit(0)

files_to_ignore = [
    "favicon.ico", "icon.png",
    "README.md", ".nojekyll",
    "200.html"
]
templates_to_rename = {
    # Старое название файла: Новое название файла.
    "index.html": "registration.html"
}
templates_path = path_to_back_end + "templates/"
static_path = path_to_back_end + "static/"

for file in listdir(path_to_front_end):
    if file in files_to_ignore:
        continue

    file_path = path_to_front_end + file
    if isdir(file_path):
        if file == "_nuxt":
            new_path = static_path + file
            if exists(new_path):
                rmtree(new_path)
            copytree(src=file_path, dst=new_path, symlinks=False)
            print("'_nuxt' copied.")
        else:
            if "index.html" not in listdir(file_path):
                print(f"WARNING({file}): Не найден index.html")
                continue
            file_path += "/index.html"
            new_path = templates_path + file + ".html"
            copy_file(file_path, new_path, follow_symlinks=False)
            print(f"'{file}' copied.")
    else:
        if file in templates_to_rename:
            new_path = templates_path + templates_to_rename[file]
            copy_file(file_path, new_path)
            print(f"'{file} ({templates_to_rename[file]} new)' copied.")
        else:
            print(f"'{file}' not copied.")

refactor_html_files = True if input("Сделать ли псевдо-удобный рефактор кода?(y/n) ") == "y" else False
if not refactor_html_files:
    exit(0)

for file in listdir(templates_path):
    full_path = templates_path + file
    with open(full_path, mode="r", encoding="utf-8") as file_object:
        file_text = file_object.read().replace("\n", "").replace(">", ">\n").replace("</", "\n</").replace("\n\n", "\n")

        file_text = file_text.replace('src="/_nuxt', 'src="/static/_nuxt')
        file_text = file_text.replace('href="/_nuxt', 'href="/static/_nuxt')

    with open(full_path, mode="w", encoding="utf-8") as file_object:
        file_object.write(file_text)

    print(f"'{file}' refactored.")
