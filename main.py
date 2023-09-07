from PIL import Image
import os
import platform

def make_pdf_all(dir_path):
    if platform.system() == "Windows":
        join = str("/")
        dir_files = [dir_path + join + f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        return dir_files

    elif platform.system() == "Linux":
        join = str('\'')
        dir_files = [dir_path + join + f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        return dir_files #Если операционная система - Windows, то переменная join устанавливается равной /, иначе, если операционная система - Linux

def make_pdf_only_selected(selected_files, file_name, pdf_location):
    images_list = [] # код создает пустой список images_list, который будет содержать изображения, которые будут использованы для создания PDF файла.
    for f in selected_files:
        try:
            images_list.append((Image.open(f)).convert('RGB'))
        except IOError:
            pass #Внутри цикла, код пытается открыть каждый файл с помощью функции Image.open(f) из модуля PIL.
            # Если файл является изображением, то он добавляется в список images_list после преобразования в формат RGB с помощью метода convert('RGB'). Если файл не является изображением или возникает ошибка при его открытии, то код пропускает его с помощью оператора pass.

    os.chdir(pdf_location)
    images_list[0].save(file_name, save_all=True, append_images=images_list[1:]) #код сохраняет первое изображение из списка images_list в формате PDF с помощью метода save() из модуля PIL. Он также указывает параметр save_all=True, чтобы сохранить все изображения из списка images_list в один PDF файл. Параметр append_images=images_list[1:]
    # указывает, что все остальные изображения из списка должны быть добавлены к первому изображению.

if __name__ == '__main__':
    print("Это основной серверный модуль!")
