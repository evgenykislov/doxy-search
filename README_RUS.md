#doxy-search
Поисковый сервер для осуществления поиска по документации, сгенерированной doxygen.
Сервер позволяет осуществлять поиск в документации не только по ключевым словам, но и по описанию.
В отличие от решения doxysearch??? сервер позволяем осуществлять поиск по части строки.
Также сервер поддерживает работу с несколькими документациями.
Для работы не требуется доступ к интернету и др. облачным решениям.

Сервер предназначен для работы на локальном компьютере, там же где находится сгенерированная документация.

Сервер doxy-search использует для своей работы фреймворк Django, работающий на python.

Далее описана установка и использование сервера.


* **Предустановленное ПО**  
Требуется установленный python версии 3, в котором установлен пакет Django. Python и Django являются бесплатно распространяемым ПО. Описание его установки для вашей версии операционной системы проще всего найти в интернете.

* **Установка**  
  В папке загруженного doxy-search (в ней находится файл manage.py) выполняем следующие команды:  
  1. **Инициализация базы данных**  
  python3 manage.py makemigrations  
  python3 manage.py migrate  --run-syncdb  
  1. **Запустить doxy-search**  
  python3 manage.py runserver

* Добавление документации  
Необходимо будет изменить настройки в Doxyfile и сделать две генерации документации:  
  - В doxywizard открываем Doxyfile и во вкладке Expert в топике HTML выставляем следующие поля:  
    - SEARCHENGINE - Yes
    - SERVER_BASED_SEARCH - Yes
    - EXTERNAL_SEARCH - Yes
    - SEARCHENGINE_URL - empty string
    - SEARCHDATA_FILE - searchdata.xml (it's default value)
  - генерируем документацию
  - находим файл searchdata.xml (обычно расположен в родительской папке относительно сгенерированной документации) и запоминаем его путь
  - создаём проект в doxy-search
    - Открываем в браузере страницу: http://127.0.0.1:8000/localsrv/admin  
    - Нажимаем добавить документацию
    - Вводим желаемое имя документации и путь к файлу searchdata.xml. Также можете указать 'слаг' (не обязательно).
    - Жмём Save and Exit
  - На главной странице для созданной документации копируем поисковую ссылку.
  - В doxywizard открываем Doxyfile и во вкладке Expert в топике HTML выставляем следующие поля:  
    - SEARCHENGINE_URL - указываем ссылку (см. предыдущий шаг)
  - генерируем документацию
  - На главной странице для созданной документации нажимаем кнопку обновить (после второй генерации)

* Использование поиска
- Открываем в браузере документацию (index.html)
- В поле поиска набираем желаемую строку, жмём кнопку искать или enter.

* Обновление документации
Если документация обновилась, то необходимо также обновить и базу поиска.
Для этого заходим на главную страницу: http://127.0.0.1:8000/localsrv/admin/
И для требуемой документации жмём Обновить.


Кислов Евгений, 2021-2022.