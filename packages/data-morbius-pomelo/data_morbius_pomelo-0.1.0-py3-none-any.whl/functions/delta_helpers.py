#GENERAL VARIABLES
from airflow.models import Variable
from datetime import datetime,timezone
from airflow.exceptions import AirflowException, AirflowFailException
import logging

########################################
######  *** CLUSTER FUNCTIONS *** ######
########################################
def get_steps(s3_client, process_date, config_map, **kwargs):
    s3_raw_path = kwargs['params']['s3_raw_path']
    full_load = kwargs['params']['full_load']

    database_dict = generate_database_dict(s3_raw_path, s3_client, **kwargs)
    steps = []
    
    while database_dict:
        database = database_dict.popitem()
        cluster_identifier = database[1].get('cluster_identifier')
        print(f"Running EMR Step tables in: {cluster_identifier}")
        while database[1].get('tables'):
            tables = database[1].get('tables').pop()
            spark_app_name = tables.get("spark_app_name")
            s3_table_prefix = tables.get("s3_table_prefix")
            s3_delta_table_prefix = tables.get("s3_delta_table_prefix")
            table_name = tables.get("table_name")

            print(f"Found the following information: {tables}")
            print("Will send the following information:")
            print(f"spark_app_name: {spark_app_name}")
            print(f"s3_stream_path: {s3_table_prefix}")
            print(f"s3_delta_path: {s3_delta_table_prefix}")
            print(f"cluster_identifier: {cluster_identifier}")
            print(f'table_name: {table_name}')
            item = {
                    "Name": f"Table {table_name}.",
                    "ActionOnFailure": "CONTINUE",
                    "HadoopJarStep": {
                        "Jar": "command-runner.jar",
                        "Args": [
                            "spark-submit","--deploy-mode", "cluster", "--conf", "spark.executor.cores=1", "--conf", "spark.executor.instances=1", "--conf", "spark.executor.memory=2G", "--conf", "spark.executor.memoryOverhead=1G", "--conf", "spark.driver.memoryOverhead=1G", "--conf", "spark.driver.cores=1", "--conf", "spark.driver.memory=2G", "--conf", "spark.default.parallelism=10", "--conf", "spark.dynamicAllocation.enabled=false", "--conf", "spark.streaming.dynamicAllocation.enabled=true", "--conf", "spark.streaming.dynamicAllocation.minExecutors=1", "--conf", "spark.streaming.dynamicAllocation.maxExecutors=2", "--master", "yarn", "--conf", "spark.yarn.submit.waitAppCompletion=true"
                            ,"--py-files" ,f"s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-core_2.12-2.0.0.jar,s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-storage-2.0.0.jar"
                            ,"--jars" , f"s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-core_2.12-2.0.0.jar,s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-storage-2.0.0.jar"
                            ,f"s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/code/emr/delta_table_merge.py",
                            "--spark_app_name", spark_app_name,
                            "--s3_stream_path", s3_table_prefix,
                            "--s3_delta_path", s3_delta_table_prefix,
                            "--environment", config_map.LOWER_ENV,
                            "--cluster_identifier", cluster_identifier,
                            "--table_name", table_name,
                            ]
                        }
                    }
            if not full_load:
                item.update({"Name": f"{process_date}. Table {table_name}."})
                item['HadoopJarStep']['Args'].append('--process_date')
                item['HadoopJarStep']['Args'].append(process_date)

            steps.append(item)
    return steps


def get_steps_optimized(s3_client, process_date, config_map, **kwargs):
    s3_raw_path = kwargs['params']['s3_raw_path']
    full_load = kwargs['params']['full_load']

    database_dict = generate_database_dict(s3_raw_path, s3_client, **kwargs)
    steps = []

    while database_dict:
        database = database_dict.popitem()
        cluster_identifier = database[1].get('cluster_identifier')
        print(f"Running EMR Step tables in: {cluster_identifier}")
        while database[1].get('tables'):
            tables = database[1].get('tables').pop()
            spark_app_name = tables.get("spark_app_name")
            s3_table_prefix = tables.get("s3_table_prefix")
            s3_delta_table_prefix = tables.get("s3_delta_table_prefix")
            table_name = tables.get("table_name")

            print(f"Found the following information: {tables}")
            print("Will send the following information:")
            print(f"spark_app_name: {spark_app_name}")
            print(f"s3_stream_path: {s3_table_prefix}")
            print(f"s3_delta_path: {s3_delta_table_prefix}")
            print(f"cluster_identifier: {cluster_identifier}")
            print(f'table_name: {table_name}')
            item = {
                "Name": f"Table {table_name}.",
                "ActionOnFailure": "CONTINUE",
                "HadoopJarStep": {
                    "Jar": "command-runner.jar",
                    "Args": [
                        "spark-submit",
                        "--deploy-mode", "cluster",
                        "--master", "yarn",
                        "--executor-memory", "26g",
                        "--driver-memory", "10g",
                        "--num-executors", "11",
                        "--executor-cores", "3",
                        "--conf", "spark.sql.files.maxPartitionBytes=128m",
                        "--conf", "spark.databricks.delta.optimizeWrite.enabled=true",
                        "--conf", "spark.sql.shuffle.partitions=200",
                        "--conf", "spark.yarn.submit.waitAppCompletion=true",
                        "--py-files", f"s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-core_2.12-2.0.0.jar,s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-storage-2.0.0.jar"
                        ,"--jars", f"s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-core_2.12-2.0.0.jar,s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/emr/jar/delta-storage-2.0.0.jar"
                        ,f"s3://use1-{config_map.LOWER_ENV}-infrastructure-datalake-s3/code/emr/delta_table_merge.py",
                        "--spark_app_name", spark_app_name,
                        "--s3_stream_path", s3_table_prefix,
                        "--s3_delta_path", s3_delta_table_prefix,
                        "--environment", config_map.LOWER_ENV,
                        "--cluster_identifier", cluster_identifier,
                        "--table_name", table_name,
                    ]
                }
            }
            if not full_load:
                item.update({"Name": f"{process_date}. Table {table_name}."})
                item['HadoopJarStep']['Args'].append('--process_date')
                item['HadoopJarStep']['Args'].append(process_date)

            steps.append(item)
    return steps

def clone_step_streaming_status():
    print("TBD task que clone el step caido del straming")

########################################
######  *** DELTA HELPER FUNCTIONS *** ######
########################################

def generate_database_dict(s3_raw_path, s3_client, **kwargs):
    raw_prefix = kwargs['params']['raw_prefix']

    database_dict = {
        f"{raw_prefix}accounts-api/": {
            "cluster_identifier": "use1-prd-core-accounts-api-accounts-api-db-rds-cluster"
        },
        f"{raw_prefix}accounts-query-api/": {
            "cluster_identifier": "use1-prd-core-accounts-query-api-rds-cluster"
        },
        f"{raw_prefix}dashboard-feature-toggle-db/": {
            "cluster_identifier": "use1-prd-dashboard-feature-toggle-db-rds-cluster"
        },
        f"{raw_prefix}developer-site-devx-account/": {
            "cluster_identifier": "use1-prd-developer-site-devx-account-db-rds-cluster"
        },
        f"{raw_prefix}fraud-fraud-store-db/": {
            "cluster_identifier": "use1-prd-fraud-fraud-store-db-rds-cluster"
        },
        f"{raw_prefix}identity-identity-geo-inf-db/": {
            "cluster_identifier": "use1-prd-identity-identity-geo-inf-db-rds-cluster"
        },
        f"{raw_prefix}issuing-clients-service-db/": {
            "cluster_identifier": "use1-prd-issuing-clients-service-db-rds-cluster"
        },
        f"{raw_prefix}issuing-shipping-service/": {
            "cluster_identifier": "use1-prd-issuing-shipping-service-db-rds-cluster"
        },
        f"{raw_prefix}issuing-users-service/": {
            "cluster_identifier": "use1-prd-issuing-users-service-db-rds-cluster"
        },
        f"{raw_prefix}network-cash-network-api-cashdb/": {
            "cluster_identifier": "use1-prd-network-cash-network-api-cashdb-rds-cluster"
        },
        f"{raw_prefix}network-cash-network-br-api-cash/": {
            "cluster_identifier": "use1-prd-network-cash-network-br-api-cash-rds-cluster"
        },
        f"{raw_prefix}payment-processor-tax-api-db/": {
            "cluster_identifier": "use1-prd-payment-processor-tax-api-db-rds-cluster"
        },
        f"{raw_prefix}payment-processor-transaction-adjustment/": {
            "cluster_identifier": "use1-prd-payment-processor-transaction-adjustment-rds-cluster"
        },
        f"{raw_prefix}issuing-cards-service/":{
            "cluster_identifier": "use1-cde-issuing-cards-service-db-rds-cluster"
        },
        f"{raw_prefix}fraud-fraud-chargebacks-core-cbk-db/":{
            "cluster_identifier": "use1-prd-fraud-fraud-chargebacks-core-cbk-db-rds-cluster"
        }

    }

    #Si s3_raw_path esta seteado solo nos quedamos con la info de esa instancia
    if s3_raw_path:
        database_dict = {f'{raw_prefix}{s3_raw_path}':database_dict.get(f'{raw_prefix}{s3_raw_path}')}
        modified_database_dict = obtain_s3_table_list(database_dict, s3_client, **kwargs)
        return modified_database_dict

def obtain_s3_table_list(database_dict, s3_client, **kwargs):
    client = s3_client 
    bucket = kwargs['params']['bucket']
    raw_prefix = kwargs['params']['raw_prefix']
    delta_prefix = kwargs['params']['delta_prefix']
    for database in database_dict:
        print(f"Loading tables for database: {database}")
        database_result = client.list_objects(
            Bucket=bucket, Prefix=database, Delimiter='/')

        database_dict[database]['tables'] = []
        for table in database_result.get('CommonPrefixes'):
            print(f"Found table: {table}")
            if not table.get('Prefix').endswith('_checkpoints/'):
                s3_table_prefix = table.get('Prefix')
                table_name = get_table_name(s3_table_prefix)
                spark_app_name = get_spark_app_name(
                    table_name, database_dict[database].get('cluster_identifier'))
                s3_delta_table_prefix = s3_table_prefix.replace(
                    raw_prefix, delta_prefix)
                database_dict[database]['tables'].append(
                    {
                        "s3_table_prefix":  "s3://" + bucket + '/' + s3_table_prefix,
                        "table_name": table_name,
                        "spark_app_name": spark_app_name,
                        "s3_delta_table_prefix": "s3://" + bucket + '/' + s3_delta_table_prefix
                    })

    return database_dict


#Candidatas a pasar a empaquetar en los helpers

def get_table_name(s3_table_prefix):
    # Ejemplo:
    #   s3_table_prefix.rsplit = streaming-raw-data/issuing-users-service/users/
    #   s3_table_prefix.rsplit('/')
    #        ['streaming-raw-data', 'issuing-users-service', 'users', '']
    #   Nos queremos quedar con 2, por eso aca hacemos [-2]
    return s3_table_prefix.rsplit('/')[-2]


def get_spark_app_name(table_name, cluster_identifier):
    spark_app_name = f'app-{remove_suffix(cluster_identifier,"-rds-cluster")}-{table_name}'
    return spark_app_name

## De Python 3.9 o 3.8 en adelante existe str.removepreffix(preffix). Pero en python 3.7 no, por lo que tenemos este helper para remover prefixes
def remove_preffix(text, preffix):
    if text.startswith(preffix):
        return text[len(preffix):]
    return text  # or whatever
## De Python 3.9 o 3.8 en adelante existe str.removesuffix(suffix). Pero en python 3.7 no, por lo que tenemos este helper para remover sufijo
def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix):]
    return text  # or whatever
