# acm-cli

## Как создать проект, чтобы он заработал

1. Создаём рабочую директорию и переходим в неё. Например, `mkdir test && cd test`.
2. Выводим полный путь до текущей директории. Это понадобится нам в будущем. Для этого вводим команду `pwd`. 
3. Выполняем команду `git clone https://github.com/vladloh/acm-cli`
4. Заходим в скачанную директорию (`cd acm-cli`)
5. Создаём там файл `config.py` следующего содержания. В качестве `folder_path` рекомендуется использовать результат 2 шага. 
```python
# login 
login = 'xxx'

# password
password = 'xxx'

# full path to folder, created at step 1. For example, '/Users/work/Documents/unic/dp_contests'. 
folder_path = 'xxx/xxx/xxx'
```
5. Создаём там файл `acm` следующего содержания и заменяем XXX на путь полученный в пункте 2:
```bash
#!/bin/bash

PATH_TO_ACCOUNT=XXX
python3 $PATH_TO_ACCOUNT/acm-cli/api.py $@
```
6. Делаем файл `acm` исполняемым: `chmod +x acm`
7. Устанавливаем зависимости: `pip3 install -r requirements.txt`
8. Выходим из папки на уровень наверх: `cd ..`
9. Создаём файл `template.cpp` -- это будет нашим шаблоном. 
## Использование утилиты в MacVim
10. Открываем или создаём файл `~/.vimrc`, добавляем в него такие строчки:
```
command! Gen !./acm-cli/acm gen
command! Submit !./../acm-cli/acm submit '%:p'
command! Status !./../acm-cli/acm status
command! Submissions !./../acm-cli/acm submissions

"Uncomment this for hotkey F12 for submit
"autocmd filetype cpp nnoremap <F12> :w <bar> Submit %:p <CR>
```
11. Вызываем в macvim команду `source ~/.vimrc`, чтобы активировать изменения

Теперь всё готово к использованию в MacVim.  
Чтобы вызвать очередную команду, нужно написать `Gen/Submit/Status/Submissions` в поле команд.   
Команда `Gen` должна запускаться из директории, куда мы сохраняем контесты.  
Команда `Submit` должна запускаться при открытом файле с решением задачи.   
Команда `Status/Submissions` вызывается внутри папки конкретного контеста.  


## Использование консольной утилиты (независимо от macvim) 
!!! Может быть неопределенное поведение !!!  
`acm gen` -- скачивает все имеющиеся контесты. вызывать нужно в папке, куда будут сохраняться контесты.   
`acm submit path` -- посылает задачу. path должен быть вида .../contest_folder/A.cpp. рекомендуется запускать из папки с задачей текущего контеста.   
`acm status` -- выводит статус всех задач текущего контеста. запускать нужно из папки с задачами текущего контеста.   
`acm submissions` -- выводит статус последних 10 посылок в контесте. запускать нужно из папки с задачами текущего контеста.   
