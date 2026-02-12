This script creates a volume, an  export policy and an export rules using the REST API. A thick volume is created. The NFS protocol is used for export rules. The "Snapshot copies" folder is hidden from users. Snapshot reserve is set to 0%. Storage efficiency is disabled (deduplication, cross-volume deduplication, compression).

Tested on:
- ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10

Run the script from a Linux bash shell:

python3 create_volume.py <cluster_ip> <login> <password> <svm_name> <aggregate> <volume_name> <size_gb> <client_ips>

Where the parameters from the template above are:
- cluster_ip - IP address of the cluster
- login - admin login with volume creation permission
- password - admin password
- svm_name - name of the existing svm (Storage Virtual Machine)
- aggregate - name of the existing aggregate
- volume_name - name of the volume to be created
- size_gb - specify the desired volume size in GB (integer value)
- client_ips - list of client IP addresses for export rules, separated by spaces

All parameters must be separated by a single space (no commas). Parameters may contain special characters that must be escaped in bash (@ # & $ ! " ' [ ] { } * ( ) < > | ). Quotes '' or "" are used for escaping. F.e. if the password is the string like Disk000@Somethinghere you must escape the password with quotes "Disk000@Somethinghere" or 'Disk000@Somethinghere' because of the @ symbol when passing it to the command line.

An example:

python3 create_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_10_SAS_1 dc0_d000_test_nfs_01 10 10.100.10.01 10.100.10.02

***********************************************************************************************************************************


Этот скрипт создает volume, export policy и export rules, используя REST API. Создается thick volume, для export rules используется протокол NFS, папка “Snapshot copies” скрывается от пользователей, Snapshot reserve - 0%, Storage efficiency отключено (deduplication, cross-volume deduplication, compression).

Скрипт протестирован на:
- ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10 

При запуске скрипта необходимо вводить данные через консоль. Скрипт вызывается через консоль bash Linux. Шаблон вызова:

python3 create_volume.py <cluster_ip> <login> <password> <svm_name> <aggregate> <volume_name> <size_gb> <client_ips>

где:
- cluster_ip - IP массива
- login - логин администратора, у которого есть права на создание volume
- password - пароль администратора
- svm_name - имя существующей svm (Storage Virtual Machine)
- aggregate - имя существующего агрегата
- volume_name - имя volume, который необходимо создать
- size_gb - указать необходимый размер создаваемого volume в ГБ, указывается целым числом
- client_ips - список клиентских IP-адресов для создания export rules, указывается через пробел

Все параметры передаются через 1 пробел без запятых. В параметрах могут встречаться символы, которые необходимо экранировать, передавая через bash (@ # & $ ! " ' [ ] { } * ( ) < > | ). Для экранирования используются кавычки '' или "". То есть если пароль является строкой Disk000@Somethinghere, то из-за символа @ необходимо экранировать пароль кавычками "Disk000@Somethinghere" или 'Disk000@Somethinghere' при передаче в командную строку:

Пример запуска скрипта:

python3 create_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_10_SAS_1 dc0_d000_test_nfs_01 10 10.100.10.01 10.100.10.02
