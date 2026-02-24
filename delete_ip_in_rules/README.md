This script deletes ONE IP address from an export rule in NetApp ONTAP using the REST API.

⚠️ Important:

If the export rule contains only one client IP address, the rule will be deleted together with that IP address.

If the export rule contains multiple client IP addresses, only the specified IP address will be removed, and the export rule will remain.

The script was tested on:

ONTAP AFF 9.14.1

Python 3.10

When running the script, input parameters must be provided via the console. The script is executed from a Linux bash shell.

Command template:
python3 delete_IP_in_rule.py <IP> <login> <password> <svm_name> <export_policy_name> <client_ip_delete>

Where:

IP — cluster IP address

login — administrator login

password — administrator password

svm_name — name of the SVM where the export policy resides

export_policy_name — name of the export policy associated with the IP address to be deleted

client_ip_delete — IP address to be removed

All parameters must be separated by a single space (no commas).

Parameters may contain special characters that must be escaped when passed through bash:

@ # & $ ! " ' [ ] { } * ( ) < > |

Use single ('') or double ("") quotes for escaping.
For example, if the password is Disk000@Somethinghere, the @ symbol requires escaping when passed on the command line:

"Disk000@Somethinghere"

or

'Disk000@Somethinghere'
Example:
python3 delete_IP_in_rule.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy 10.100.10.01

***********************************************************************************************************************************

Этот скрипт удаляет ОДИН IP в export rule NetApp ONTAP, используя REST API.

!!! Если export rule содержит только один IP-адрес клиента, правило удаляется вместе с удаленным IP-адресом.
Если export rule содержит несколько IP-адресов клиентов, удаляется только указанный IP-адрес, а export rule остается.

Скрипт протестирован на:
- ONTAP AFF 9.14.1
- Python 3.10 

При запуске скрипта необходимо вводить данные через консоль. Скрипт вызывается через консоль bash Linux. Шаблон вызова:

python3 delete_IP_in_rule.py <IP> <login> <password> <svm_name> <export_policy_name> <client_ip_delete>

где:
- IP - IP массива
- login - логин администратора
- password - пароль администратора
- svm_name - имя svm, на которой расположена export_policy
- export_policy_name – имя export policy, к которой относится удаляемый IP
- client_ip_delete – IP, который необходимо удалить

Все параметры передаются через 1 пробел без запятых. В параметрах могут встречаться символы, которые необходимо экранировать, передавая через bash (@ # & $ ! " ' [ ] { } * ( ) < > | ). Для экранирования используются кавычки '' или "". То есть если пароль является строкой Disk000@Somethinghere, то из-за символа @ необходимо экранировать пароль кавычками "Disk000@Somethinghere" или 'Disk000@Somethinghere' при передаче в командную строку.

Пример запуска скрипта:

`python3 delete_IP_in_rule.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy 10.100.10.01`



