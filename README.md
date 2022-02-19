# acm-cli

## Как создать проект, чтобы он заработал

1. создаём рабочую директорию и переходим в неё
2. Выполняем команду `git clone https://github.com/vladloh/acm-cli`
3. Заходим в скачанную директорию (`cd acm-cli`)
4. Создаём там файл `config.py` следующего содержания:
```python
# login 
login = 'xxx'

# password
password = 'xxx'

# full path to folder, created at step 1. For example, '/Users/work/Documents/unic/dp_contests'. 
folder_path = 'xxx/xxx/xxx'
```
5. Создаём файл `acm` следующего содержания:
```bash
#!/bin/bash

PATH_TO_ACCOUNT=XXX
python3 $PATH_TO_ACCOUNT/acm-cli/api.py $@
```
6. Делаем файл `acm` исполняемым: `chmod +x acm`
