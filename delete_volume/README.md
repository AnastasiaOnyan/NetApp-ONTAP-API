Этот скрипт удаляет существующий volume в NetApp ONTAP, используя python библиотеку netapp_ontap (ONTAP REST API). Библиотеку необходимо установить командой pip install netapp-ontap. 

Скрипт протестирован на:
- ONTAP 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10 

При запуске скрипта необходимо вводить данные через консоль. Скрипт вызывается через консоль bash Linux. Шаблон вызова:

python3 delete_volume.py <IP> <login> <password> <svm_name> <volume_name>

где:
- IP - IP массива, на котором расположен volume
- login - логин администратора, имеющего права для изменения размера volume
- password - пароль администратора
- svm_name - имя svm, на которой расположен volume
- volume_name - имя volume, который необходимо удалить

Все параметры передаются через 1 пробел без запятых. В параметрах могут встречаться символы, которые необходимо экранировать, передавая через bash (@ # & $ ! " ' [ ] { } * ( ) < > | ). Для экранирования используются кавычки '' или "". То есть если пароль является строкой Disk000@Somethinghere, то из-за символа @ необходимо экранировать пароль кавычками "Disk000@Somethinghere" или 'Disk000@Somethinghere' при передаче в командную строку.

Пример запуска скрипта:

`python3 delete_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01`

***************************************************************************************************************************

This script deletes an existing volume in NetApp ONTAP using the `netapp_ontap` Python library (ONTAP REST API). The library may be installed using the command `pip install netapp-ontap`.

The script was tested on:

* **ONTAP 9.14.1**
* **netapp_ontap Python client 9.17.1.0**
* **Python 3.10**

When running the script, data must be entered via command line. The script is executed via Linux Bash. The invocation template:

```python3 delete_volume.py <IP> <login> <password> <svm_name> <volume_name>```

where:

* **IP** — IP address of the array on which the volume is located
* **login** — administrator login with permissions to modify the volume size
* **password** — administrator password
* **svm_name** — name of the SVM on which the volume is located
* **volume_name** — name of the volume that needs to be deleted

All parameters are passed separated by 1 space, without commas. The parameters may contain characters that need to be escaped when passing them through Bash (`@ # & $ ! " ' [ ] { } * ( ) < > |`). Quotes `''` or `""` are used for escaping. That is, if the password is the string `Disk000@Somethinghere`, then because of the `@` character, the password must be escaped with quotes `"Disk000@Somethinghere"` or `'Disk000@Somethinghere'` when passing it to the command line.

Example of running the script:

```python3 delete_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01```
