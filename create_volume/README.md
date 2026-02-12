Этот скрипт создает volume, export policy и export rules, используя REST API. Создаются thick volumes, для export rules используется протокол NFS, папка “Snapshot copies” скрывается от пользователей, Snapshot reserve - 0%, Storage efficiency отключено (deduplication, cross-volume deduplication, compression).

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
- svm_name - имя существующей svm (Storgae Virtual Machine)
- aggregate - имя существующего агрегата
- volume_name - имя volume, который необходимо создать
- size_gb - указать необходимый размер создаваемого volume в ГБ, указывается целым числом
- client_ips - список клиентских IP-адресов для создания export rules, указывается через пробел

Все параметры передаются через 1 пробел без запятых. В параметрах могут встречаться символы, которые необходимо экранировать, передавая через bash (@ # & $ ! " ' [ ] { } * ( ) < > | ). Для экранирования используются кавычки '' или "". То есть если пароль является строкой Disk000@Somethinghere, то из-за символа @ необходимо экранировать пароль кавычками "Disk000@Somethinghere" или 'Disk000@Somethinghere' при передаче в командную строку:

Пример запуска скрипта:

python3 create_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_10_SAS_1 dc0_d000_test_nfs_01 10 10.100.10.01 10.100.10.02
