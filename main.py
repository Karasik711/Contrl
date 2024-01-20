import json
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QLabel, QListWidget, QPushButton, QLineEdit, QInputDialog, QMessageBox

app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
window.setWindowIcon(QtGui.QIcon('note.png'))

window.setMinimumSize(600, 500)

main_layout = QHBoxLayout()
col_left = QVBoxLayout()
text_note = QTextEdit()
col_left.addWidget(text_note)

col_right = QVBoxLayout()

layout1 = QVBoxLayout()

notes_list_label = QLabel('Список заметок:')
layout1.addWidget(notes_list_label)

notes_list = QListWidget()
layout1.addWidget(notes_list)

layout2 = QHBoxLayout()

create_note_button = QPushButton('Создать заметку')
layout2.addWidget(create_note_button)

delete_note_button = QPushButton('Удалить заметку')
layout2.addWidget(delete_note_button)

layout3 = QVBoxLayout()

save_note_button = QPushButton('Сохранить заметку')
layout3.addWidget(save_note_button)

tags_label = QLabel('Список тегов:')
layout3.addWidget(tags_label)

tags_list = QListWidget()
layout3.addWidget(tags_list)

tag_edit = QLineEdit()
tag_edit.setPlaceholderText('Введите тег...')
layout3.addWidget(tag_edit)

layout4 = QHBoxLayout()

add_tag_button = QPushButton('Добавить к заметке')
layout4.addWidget(add_tag_button)

remove_tag_button = QPushButton('Открепить от заметки')
layout4.addWidget(remove_tag_button)

layout5 = QHBoxLayout()
find_notes_by_tag = QPushButton('Искать заметки по тегу')
layout5.addWidget(find_notes_by_tag)

col_right.addLayout(layout1)
col_right.addLayout(layout2)
col_right.addLayout(layout3)
col_right.addLayout(layout4)
col_right.addLayout(layout5)

col_right.setSpacing(16)

main_layout.addLayout(col_left)
main_layout.addLayout(col_right)
window.setLayout(main_layout)


with open('notes.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

notes_list.addItems(data.keys())

def show_note():
    note_name = notes_list.currentItem().text()
    n_text = data[note_name]["текст"]
    n_tags = data[note_name]["теги"]

    text_note.setText(n_text)
    tags_list.clear()
    tags_list.addItems(n_tags)

notes_list.itemClicked.connect(show_note)

def create_note():
    note_name, result = QInputDialog.getText(window, \
        "Добавить заметку", "Название заметки:")
    if result and not note_name in data.keys() and note_name != '':
        data[note_name] = {
        "текст" : "",
        "теги" : []
    	}
        notes_list.addItem(note_name)


create_note_button.clicked.connect(create_note)

def save_all():
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)

def save_note():
    if notes_list.currentItem():
        note_name = notes_list.currentItem().text()
        data[note_name]['текст'] = text_note.toPlainText()
        save_all()

save_note_button.clicked.connect(save_note)

def delete_note():
    if notes_list.currentItem():
        note_name = notes_list.currentItem().text()
        
delete_note_button.clicked.connect(delete_note)

window.show()
app.exec_()
