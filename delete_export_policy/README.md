Этот скрипт удаляет существующую export policy в NetApp ONTAP, используя python библиотеку netapp_ontap (ONTAP REST API). Библиотеку необходимо установить командой pip install netapp-ontap. 

!!! Перед удалением данной export policy необходимо сначала либо переназначить на другую export policy, либо удалить все относящиеся к ней volumes, qtrees и export rules.

Скрипт протестирован на:
- ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10 

При запуске скрипта необходимо вводить данные через консоль. Скрипт вызывается через консоль bash Linux. Шаблон вызова:

python3 delete_exp_policy.py <IP> <login> <password> <svm_name> <export_policy_name>

где:
- IP - IP массива
- login - логин администратора
- password - пароль администратора
- svm_name - имя svm, на которой расположена export_policy
- export_policy_name – имя export policy, которую необходимо удалить


Все параметры передаются через 1 пробел без запятых. В параметрах могут встречаться символы, которые необходимо экранировать, передавая через bash (@ # & $ ! " ' [ ] { } * ( ) < > | ). Для экранирования используются кавычки '' или "". То есть если пароль является строкой Disk000@Somethinghere, то из-за символа @ необходимо экранировать пароль кавычками "Disk000@Somethinghere" или 'Disk000@Somethinghere' при передаче в командную строку.

Пример запуска скрипта:

`python3 delete_exp_policy.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy`

