import os
import sys
from platform import system
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QStyleFactory, QDesktopWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
import main

# Корневое расположение приложения ↓
if system() == "Windows":
    appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"
elif system() == "Linux":
    appFolder = os.path.dirname(os.path.realpath(sys.argv[0])) + "//"
    #код проверяет операционную систему, на которой он выполняется, с помощью system().


class App(QMainWindow):
    def __init__(self):
        """Constructor."""
        super(App, self).__init__()
        uic.loadUi(appFolder + "ImaP.ui", self)  # Load the UI(User Interface) file. #Загружается пользовательский интерфейс из файла "ImaP.ui" с помощью uic.loadUi()
        self.makeWindowCenter() #центрирует окно приложения на экране
        self.run_system()  # основная рабочая функция этого файла графического интерфейса

        self.statusBar().showMessage("Конвертируйте файлы изображений в PDF (переносимый формат документов).).") #Устанавливается сообщение в строку состояния (statusBar()), которое отображается в нижней части окна
        self.setWindowTitle("Приложение Image To PDF Converter для рабочего стола")


    def makeWindowCenter(self):
        """For launching windows in center."""
        qtRectangle = self.frameGeometry() #создается прямоугольник (прямоугольник окна) с геометрией текущего виджета (окна).
        centerPoint = QDesktopWidget().availableGeometry().center() #определяется центр экрана с помощью QDesktopWidget, который предоставляет информацию о рабочем столе.
        qtRectangle.moveCenter(centerPoint) #центральная точка прямоугольника qtRectangle устанавливается в значение centerPoint, что фактически центрирует прямоугольник относительно центра экрана
        self.move(qtRectangle.topLeft()) #окно перемещается так, чтобы верхний левый угол прямоугольника qtRectangle совпадал с верхним левым углом окна

    def run_system(self):

        self.pushButton.clicked.connect(self.add_folder_button_on_click) #устанавливает связь между событием "клик на кнопку pushButton" и методом add_folder_button_on_click
        self.pushButton_add.clicked.connect(self.add_images_button_on_click) #
        self.pushButton_remove.clicked.connect(self.remove_button_on_click)
        self.pushButton_up.clicked.connect(self.up_button_on_click)
        self.pushButton_down.clicked.connect(self.down_button_on_click)
        self.pushButton_make_pdf.clicked.connect(self.make_pdf_button_on_click)
        self.pushButton_clear.clicked.connect(self.clear_button_on_click) #Когда пользователь нажимает на соответствующие кнопки, вызываются соответствующие методы для выполнения определенных действий, которые определенны в коде.

    def add_folder_button_on_click(self): # определяет действия, которые должны выполняться при нажатии на кнопку "Добавить папку".


        dir_path = QFileDialog.getExistingDirectory(self, 'Open File') #открывается диалоговое окно для выбора папки, и выбранная папка сохраняется в переменную dir_path

        if dir_path != "":
            dir_files = main.make_pdf_all(dir_path) # Если dir_path не пустая строка (т.е. пользователь выбрал папку), то вызывается функция main.make_pdf_all,
            # которая принимает путь к папке и создает PDF-файлыиз содержимого этой папки. Результат работы make_pdf_all сохраняется в переменную dir_files.

            for i in dir_files:
                next_row = self.listWidget.count()
                self.listWidget.insertItem(next_row, i) #цикл, в котором каждый элемент i из списка dir_files
                # добавляется в виджет listWidget, который представляет собой список элементов.
        else:
            return

    def add_images_button_on_click(self): #определяет действия, которые должны выполняться при нажатии на кнопку "Добавить изображение".
        file_name = QFileDialog.getOpenFileName(self, "Open File") #открывается диалоговое окно для выбора файла, и выбранный файл сохраняется в переменную file_name.
        next_row = self.listWidget.count()
        if file_name[0] != "":
            self.listWidget.insertItem(next_row, file_name[0]) # Если file_name[0] не пустая строка (т.е. пользователь выбрал файл),
            # то выбранный файл добавляется в виджет listWidget с помощью метода insertItem.

    def remove_button_on_click(self): #определяет действия, которые должны выполняться при нажатии на кнопку "Удалить файл изображения".
        current_row = self.listWidget.currentRow()
        item = self.listWidget.item(current_row)
        if item is None: #Если элемент равен None (т.е. ничего не выбрано), то ничего не происходит и функция завершается.
            pass
 #В противном случае, выводится диалоговое окно с вопросом о подтверждении удаления выбранного файла из списка.
        else:
            get_reply = QMessageBox.question(self, "Удалить файл изображения», «Хотите удалить" + str(item.text())
                                             + " из списка?", QMessageBox.Yes | QMessageBox.No)
            if get_reply == QMessageBox.Yes: #Если пользователь ответил "Да", то элемент списка удаляется с помощью метода takeItem(current_row)
                # и освобождается память с помощью оператора del.
                element = self.listWidget.takeItem(current_row)
                del element
            else:
                pass  #Если пользователь ответил "Нет", то ничего не происходит и функция завершается.

    def up_button_on_click(self):
        current_row = self.listWidget.currentRow() #Сначала получается текущая выбранная строка в виджете listWidget с помощью метода currentRow().
        if current_row >= 1: #проверяется, что текущая строка больше или равна 1 (т.е. не является первой строкой).
            # Если это условие не выполняется, то ничего не происходит и функция завершается.
            item = self.listWidget.takeItem(current_row)
            self.listWidget.insertItem(current_row - 1, item) #Затем элемент списка вставляется на позицию выше (текущая строка - 1) с
            # помощью метода insertItem(current_row - 1, item).
            self.listWidget.setCurrentItem(item) #Наконец, устанавливается текущий элемент списка вставленным элементом с помощью метода setCurrentItem(item).
            # то обновляет виджет listWidget так, чтобы вставленный элемент стал текущим.

    def down_button_on_click(self): #определяет действия, которые должны выполняться при нажатии на кнопку "Переместить файл изображения вниз".
        current_row = self.listWidget.currentRow()
        if current_row < self.listWidget.count() - 1: #проверяется, что текущая строка меньше, чем количество элементов в виджете минус 1 (т.е. не является последней строкой).
            # Если это условие не выполняется, то ничего не происходит и функция завершается.
            item = self.listWidget.takeItem(current_row)
            self.listWidget.insertItem(current_row + 1, item) #Затем элемент списка вставляется на позицию ниже
            self.listWidget.setCurrentItem(item) #Наконец, устанавливается текущий элемент списка вставленным элементом с помощью метода

    def clear_button_on_click(self): #определяет действия, которые должны выполняться при нажатии на кнопку "Очистить список".
        reply = QMessageBox.question(self, "Очистить список", "Вы хотите очистить все выбранные параметры?",
                                     QMessageBox.Yes | QMessageBox.No) #создается диалоговое окно с вопросом пользователю о желании очистить все выбранные параметры
        if reply == QMessageBox.Yes:
            self.listWidget.clear() #если пользователь нажимает кнопку "Да", то вызывается метод clear() для виджета listWidget. Метод clear() удаляет все элементы из виджета и очищает его.

    def make_pdf_button_on_click(self): #определяет действия, которые должны выполняться при нажатии на кнопку "Создать PDF"
        if self.listWidget.count() == 0: #Сначала проверяется, есть ли элементы в виджете listWidget.
            # Если виджет пуст, то выводится диалоговое окно QMessageBox с предупреждением о том, что список пуст, и пользователю предлагается добавить файлы в список.

            reply = QMessageBox.information(self, "Предупреждение!", "Поле со списком пусто! Сначала добавьте файлы в список.",
                                            QMessageBox.Ok)

        else:
            items_list = []
            for i in range(self.listWidget.count()): #перебираются все элементы виджета, и текст каждого элемента добавляется в список items_list с приведением его к строковому типу.
                items_list.append(str(self.listWidget.item(i).text()))

            pdf_name, ok = QInputDialog.getText(self, "PDF-имя", "Дайте имя вашему PDF-файлу", QLineEdit.Normal)
            if pdf_name == "":
                QMessageBox.information(self, "Тревога", "Пожалуйста, дайте вашему PDF-файлу имя.", QMessageBox.Ok)
                return #Если виджет пуст, то выводится диалоговое окно QMessageBox с предупреждением о том, что список пуст, и пользователю предлагается добавить файлы в список.
            if ok and pdf_name is not None:
                reply = QMessageBox.information(self, "Расположение PDF-файла", "Давайте выберем пункт назначения"
                                                                      "Чтобы сохранить PDF-файл!", QMessageBox.Ok)

                if reply == QMessageBox.Ok:

                    pdf_location = QFileDialog.getExistingDirectory(self, 'Открыть файл')
                    pdf_name += ".pdf"
                    if pdf_location == "":
                        return
                    main.make_pdf_only_selected(items_list, pdf_name, pdf_location) #Затем, к имени файла добавляется расширение .pdf, и если пользователь выбрал папку для сохранения, то вызывается функция make_pdf_only_selected из модуля main,
                    # которая создает PDF-файл на основе выбранных элементов и сохраняет его в выбранной папке с указанным именем.

                    last_reply = QMessageBox.information(self, "Сделанный!", "Ура! Ваш PDF-файл готов! "
                                                                        "Перейдите в выбранное вами место, чтобы найти"
                                                                        "PDF.", QMessageBox.Ok) #После успешного создания PDF-файла, выводится диалоговое окно
                    if last_reply == QMessageBox.Ok:
                        pass #Если пользователь подтверждает, то выполняются дополнительные действия (код не предоставлен).
                else:
                    return


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Слияние"))

    darkPalette = QtGui.QPalette()
    darkColor = QColor(45, 45, 45)
    disabledColor = QColor(127, 127, 127)
    darkPalette.setColor(QPalette.Window, darkColor)
    darkPalette.setColor(QPalette.WindowText, Qt.white)
    darkPalette.setColor(QPalette.Base, QColor(40, 40, 40))
    darkPalette.setColor(QPalette.AlternateBase, darkColor)
    darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QPalette.Text, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, disabledColor)
    darkPalette.setColor(QPalette.Button, darkColor)
    darkPalette.setColor(QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, disabledColor)
    darkPalette.setColor(QPalette.BrightText, Qt.red)
    darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.HighlightedText, Qt.black)
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, disabledColor) #этот код инициализирует и запускает приложение, показывая главное окно и обрабатывая события до его закрытия.

    app.setPalette(darkPalette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    run_main = App()  # Instantiate The App() class
    run_main.show()
    sys.exit(app.exec_())
