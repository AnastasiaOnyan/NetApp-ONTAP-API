This script deletes an existing export policy in NetApp ONTAP using the netapp_ontap Python library (ONTAP REST API). The library must be installed using the command:

pip install netapp-ontap

!!! Before deleting the export policy you must either reassign to another export policy or delete all volumes, qtrees, and export rules that associated with it.

The script was tested on:
- ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10

When running the script, input parameters must be provided as command line arguments. The script is executed from a Linux bash shell. 

A command template:

python3 delete_exp_policy.py <IP> <login> <password> <svm_name> <export_policy_name>

Where:
- IP — cluster IP address
- login — admin login
- password — admin password
- svm_name — name of the SVM where the export policy resides
- export_policy_name — name of the export policy to be deleted
- 
All parameters must be separated by a single space (no commas).

Parameters may contain some special characters that must be escaped when used in bash (@ # & $ ! " ' [ ] { } * ( ) < > |). Use single ('') or double ("") quotes for escaping.
For example, if the password is Disk000@Somethinghere, the @ symbol requires escaping when passed on the command line: "Disk000@Somethinghere".

How to run this script in bash (an example):

python3 delete_exp_policy.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy

***********************************************************************************************************************************

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

python3 delete_exp_policy.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy


