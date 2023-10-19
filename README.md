![pipeline](https://github.com/Herbet-Meneses/Airflow_Kafka_Pipeline/assets/142064420/b98cb2ac-aae1-474f-9a70-6f49df24e029)

Ambiente de produção

Esse projeto foi desenvolvido com SN Labs em uma plataforma de IDE (Ambiente de Desenvolvimento Integrado) de código aberto executado em nuvem, que é um ambiente prático para laboratórios relacionados a projetos e fins acadêmicos, mas poderia ser rodado on-premise, para isso seria necessário fazer o deploy do Airflow, CLI, kafka/zookeeper, MySQL, de preferência rodando em contêiner Docker. Caso o projeto seja operado localmente pode haver algumas alteraçãoes em comandos e caminhos mas a síntese se mantém.




Cenário

Uma empresa de consultoria em análise de dados precisa analisar os dados de tráfego rodoviário de diferentes praças de pedágio. Cada rodovia é operada por um operador de pedágio diferente, com uma configuração de TI diferente que utiliza diferentes formatos de arquivo. É necessário coletar os dados disponíveis em diferentes formatos e consolidá-los em um único arquivo. Como os dados dos veículos são capturados instantaneamente é necessário criar um pipeline de dados que coleta os dados em streaming e os carrega em um banco de dados.




Objetivo

Construir um pipeline de dados executando as seguintes etapas:


Criar um DAG do Apache Airflow que irá:

● Carregar e descompactar os dados;

● Extrair dados de arquivos CSV/TSV/TXT;

● Transformar os dados;

● Carregar os dados transformados na área de preparação;


Operar servidor Kafka para:

● Criar tópico para gerenciar dados em streaming;

● Personalizar programa gerador para transmitir para tópico kafka;

● Baixar e personalizar um consumidor de dados em streaming;


A partir de um servidor de banco de dados MySQL:

● Criar uma tabela para armazenar os dados transformados;

● Personalizar o programa consumidor para escrever no banco de dados MySQL;



Hands-on:

Step 1: Criar diretório centralizado conferir livre acesso:

    sudo mkdir -p /home/project/airflow/dags/finalassignment/staging
    sudo chmod 777 /home/project/airflow/dags/finalassignment/staging
    cd /home/project/airflow/dags/finalassignment/staging

Step 2: Descarregar dataset no diretório:

    wget -P /home/project/airflow/dags/finalassignment/staging "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-        SkillsNetwork/labs/Final%20Assignment/tolldata.tgz"

Step 3: Iniciar Airflow:

    start_airflow

Step 4: Criar DAG:

    DAG-ETL_toll_data.py

Step 5: Submeter DAG:

    cp DAG-ETL_toll_data $AIRFLOW_HOME/dags

Step 6: Rodar DAG:

    airflow dags unpause DAG-ETL_toll_data

Step 7: Monitorar DAG:

![print dag running](https://github.com/Herbet-Meneses/Airflow_Kafka_Pipeline/assets/142064420/27177e8d-a511-48d3-bbab-9eefec13d844)

Step 8: Baixar Kafka:

    wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz

Step 9: Extrair Kafka:

    tar -xzf kafka_2.12-2.8.0.tgz

Step 10: Iniciar MySQL:

    start_mysql
    mysql --host=127.0.0.1 --port=3306 --user=root --password=MTY4NTUtZmhtZW5l

Step 11: Criar banco de dados 'tolldata' e tabela 'livetolldata':

    create database tolldata;
    use tolldata;
    create table livetolldata(Row_id int, Timestamp datetime, Anonymized_Vehicle_number int, Vehicle_type char(15), Number_of_axles int,         
    Tollplaza_id smallint, Tollplaza_code varchar(20), Type_of_Payment_code char(3), Vehicle_Code varchar(10));

Step 12: Desconectar MySQL:

    exit

Step 13: Instalar Módulo kafka-python:

    python3 -m pip install kafka-python

Step 14: Instalar Módulo mysql-connector-python:

    python3 -m pip install mysql-connector-python==8.0.31

Step 15: Iniciar Zookpeear:

    cd kafka_2.12-2.8.0
    bin/zookeeper-server-start.sh config/zookeeper.properties

Step 16: Iniciar Kafka:

    cd kafka_2.12-2.8.0
    bin/kafka-server-start.sh config/server.properties

Step 17: Criar tópico Kafka:

    cd kafka_2.12-2.8.0
    bin/kafka-topics.sh --create --topic toll --bootstrap-server localhost:9092

Step 18: Criar Produtor Kafka:

    #Código python que lê os dados transformados pelo airflow em arquivo CSV e envia para o tópico Kafka através de mensagens.
    produtor.py

Step 19: Criar Consumidor e gravador de dados:

    #Código python para consumir as mensagens enviadas através do tópico kafka, transforma dados e carrega os dados em banco de dados.
    consumer.py
![INSERT](https://github.com/Herbet-Meneses/Airflow_Kafka_Pipeline/assets/142064420/01da9b26-6538-4080-95ae-798bb302c6a0)

Step 20: Consultar banco de dados:

    select * from livetolldata limit 10;
![Screenshot 2023-10-19 135746](https://github.com/Herbet-Meneses/Airflow_Kafka_Pipeline/assets/142064420/b5059361-e891-4e6e-9161-ab8910ad7a5c)

