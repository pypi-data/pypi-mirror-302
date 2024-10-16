from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
import json
from botocore.errorfactory import ClientError
import pandas as pd
import time
import timeit
import logging
import botocore

log = logging.getLogger(__name__)

BUCKET_SFTP='use1-netprd-infrastructure-sftp-server-users-s3'

BUCKET_TOOLS='use1-tools-infrastructure-datalake-s3'

ARN_SECRET='arn:aws:secretsmanager:us-east-1:248666061168:secret:use1-infra-data-ofas-bi-job-2l5IHT'
def get_secrets(secret_url, region):
    secret_name = secret_url
    region_name = region
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def get_file_s3 (bucket, path):
    """
        Get file in bucket s3
        :param bucket: bucket s3 , path: path inside the bucket
        :return file
    """
    s3_obj =boto3.client('s3')
    s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=path.strip())
    s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
    return s3_clientdata

def get_file_s3_parquet (bucket, path):
    """
        Get file in bucket s3
        :param bucket: bucket s3 , path: path inside the bucket
        :return file
    """
    s3_obj =boto3.client('s3')
    s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=path.strip())
    s3_clientdata = s3_clientobj['Body'].read()
    return s3_clientdata

def put_file_s3 (bucket, path,file):
    """
        Insert file in bucket s3
        :param bucket: bucket s3 , path: path inside the bucket , file: file to insert
    """
    client = boto3.client('s3')
    client.put_object(Body=file, Bucket=bucket,Key=path,ACL='bucket-owner-full-control')

def convert_to_windows_format(bucket,path_origin ,path_destination):
    """
            Convert and put file in windows format
            :param bucket: bucket s3 , path_origin: path origin inside the bucket , path_destination: path destination
        """
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    s3_obj = boto3.client('s3')
    s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=path_origin)
    s3_clientdata = s3_clientobj['Body'].read()
    file_replaced = s3_clientdata.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)
    put_file_s3(bucket,path_destination,file_replaced)

def delete_file_s3 (bucket, path):
    """
        Delete file from bucket s3
        :param bucket: bucket s3 , path: file path
    """
    s3_obj = boto3.client('s3')
    s3_obj.delete_object(Bucket=bucket, Key=path)

def get_data_athena(spark,json_secret,query):
    """
        Get spark dataframe with data from Athena (tables and views)
        :param spark: spark session, json_secret: Athena credential, query: query to execute
    """
    SECRET_ATHENA = get_secrets(
        "arn:aws:secretsmanager:us-east-1:644197204120:secret:data_athena_iamuser-rwmgvN",
        "us-east-1")
    ##Setting driver jdbc Athena
    jdbc_driver = "com.simba.athena.jdbc42.Driver"
    ##Generate URL to connect athena by JDBC SIMBA
    jdbcUrl = "jdbc:awsathena://AWSRegion=us-east-1;UID={};PWD={};workgroup=dba_admin;schema=pomelo,".format(json_secret.get('access-id'), json_secret.get('access-secret'))
    df = spark.read.format("jdbc") \
        .option("query", query) \
        .option("url", jdbcUrl) \
        .option("driver", jdbc_driver) \
        .load()
    return df

def get_data_athena_ofas(spark,query):
    """
        Get spark dataframe with data from Athena (tables and views)
        :param spark: spark session, json_secret: Athena credential, query: query to execute
    """
    SECRET_ATHENA = get_secrets(
        "arn:aws:secretsmanager:us-east-1:248666061168:secret:use1-infra-data-ofas-bi-job-2l5IHT",
        "us-east-1")
    ##Setting driver jdbc Athena
    jdbc_driver = "com.simba.athena.jdbc42.Driver"
    ##Generate URL to connect athena by JDBC SIMBA
    jdbcUrl = "jdbc:awsathena://AWSRegion=us-east-1;UID={};PWD={};workgroup=dba_admin;schema=pomelo,".format(SECRET_ATHENA.get('athena_access_id'), SECRET_ATHENA.get('athena_access_key'))
    df = spark.read.format("jdbc") \
        .option("query", query) \
        .option("url", jdbcUrl) \
        .option("driver", jdbc_driver) \
        .load()
    return df

def get_data_replica_pg(spark,query,db):
    JDBC_DRIVER = "org.postgresql.Driver"
    if db!="jcard":
        if db=='jiraexporter':
            secret_json = get_secrets("arn:aws:secretsmanager:us-east-1:644197204120:secret:jira-exporter-tools-8AZjmT","us-east-1")
        else:
            secret_json = get_secrets("arn:aws:secretsmanager:us-east-1:644197204120:secret:kubernetes/infrastructure/dms-replica-db-credentials-7yymMb","us-east-1")
    else:
        secret_json = get_secrets("arn:aws:secretsmanager:us-east-1:644197204120:secret:kubernetes/data/use1-tools-data-jcard-replica-db-credentials-secret-kKTTem","us-east-1")


    jdbcUrl = "jdbc:postgresql://{}:{}/{}?user={}&password={}".format(secret_json.get("host"),
                                                                      secret_json.get("port"),
                                                                      db,
                                                                      secret_json.get("username"),
                                                                      secret_json.get("password"))
    df = spark.read.format("jdbc") \
        .option("url", jdbcUrl) \
        .option("query", query) \
        .option("driver", JDBC_DRIVER) \
        .load()

    return df

def get_data_replica_pg_ofas(spark,query,db):
    JDBC_DRIVER = "org.postgresql.Driver"
    SECRET_JSON = get_secrets("arn:aws:secretsmanager:us-east-1:248666061168:secret:use1-infra-data-ofas-bi-job-2l5IHT",
                              "us-east-1")
    host=''
    port=''
    username=''
    password=''

    if db!="jcard":
        if db=='jiraexporter':
            host=SECRET_JSON.get("jira_exporter_db_host")
            port=SECRET_JSON.get("jira_exporter_db_port")
            username=SECRET_JSON.get("jira_exporter_db_username")
            password=SECRET_JSON.get("jira_exporter_db_pass")
        else:
            host = SECRET_JSON.get("dms_replica_db_host")
            port = SECRET_JSON.get("dms_replica_db_port")
            username = SECRET_JSON.get("dms_replica_db_username")
            password = SECRET_JSON.get("dms_replica_db_password")
    else:
        host = SECRET_JSON.get("jcard_replica_db_host")
        port = SECRET_JSON.get("jcard_replica_db_port")
        username = SECRET_JSON.get("jcard_replica_db_username")
        password = SECRET_JSON.get("jcard_replica_db_password")


    jdbcUrl = "jdbc:postgresql://{}:{}/{}?user={}&password={}".format(host,
                                                                      port,
                                                                      db,
                                                                      username,
                                                                      password)
    df = spark.read.format("jdbc") \
        .option("url", jdbcUrl) \
        .option("query", query) \
        .option("driver", JDBC_DRIVER) \
        .load()

    return df

def insert_dataframe_into_sql_server(df, table, schema,json_secret,_database,mode):
    username = json_secret.get('username')
    password = json_secret.get('password')
    host = json_secret.get('host')
    port = json_secret.get('port')
    database = _database
    destination_table = table
    jdbcUrl = f"jdbc:sqlserver://{host}:1433;databaseName={database}"
    jdbcDriver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"

    df.write.format("jdbc") \
        .mode(mode) \
        .option("user", username) \
        .option("password", password) \
        .option("url", jdbcUrl) \
        .option("driver", jdbcDriver) \
        .option("dbtable", destination_table) \
        .option("createTableColumnTypes", schema) \
        .save()

def move_file_s3(bucket,origin,destination,coding):
    s3_obj = boto3.client('s3')
    try:
        s3_obj.head_object(Bucket=bucket, Key=origin)
        s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=origin)
        s3_clientdata = s3_clientobj['Body'].read().decode(coding)
        s3_obj.put_object(Body=s3_clientdata, Bucket=bucket,
                      Key=destination)
        #s3_obj.delete_object(Bucket=bucket, Key=origin)
    except ClientError:
        print("Archivo {} no encontrado".format(origin))
        pass

def delete_s3_folder(bucket,key_path):
    """
            Delete folder from bucket s3
            :param bucket: bucket s3 , key_path: folder path 'bi/outbound/temp/local-1663088553000/'
        """
    s3 = boto3.resource('s3')
    bucket_name = bucket
    folder = key_path
    bucket = s3.Bucket(bucket_name)
    deletedObj = bucket.objects.filter(Prefix=folder).delete()

def send_file_to_bucket_intern(dataframe,application_id,name_file,path_destination,sep):
    """
             Send file to SFTP for internal users
                :param dataframe: bucket s3 , application_id: application of spark to make path ('bi/outbound/temp/local-1663088553000/') , name_file: name of file ,path_destination: path destionation of file,
                sep: separator of files. If we dont want a separator we pass the param 'None'
    """

    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name_file=name_file), sep='{}'.format(sep if sep in [',',';','|'] else ';'), index=False, header=False)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}'.
                                      format(application_id=application_id, name_file=name_file))
        if sep in [',',';','|']:
            file_replaced = file
        else:
            file_replaced = file.replace(';', '')

        # Disponibilizacion en SFTP

        put_file_s3(BUCKET_SFTP,
                               'bi/outbound/{path_destination}/{name_file}'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced)
        convert_to_windows_format(BUCKET_SFTP,
                                             'bi/outbound/{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             'bi/outbound/{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")

def send_file_to_bucket_raas(dataframe,application_id,client_id,name_file,path_destination):
    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}.txt'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name=name_file), sep=';', index=False, header=False)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}.txt'.
                                      format(application_id=application_id, name=name_file))
        file_replaced = file.replace(';', '')

        # Disponibilizacion en SFTP

        put_file_s3(BUCKET_SFTP,
                               'bi/outbound/{path_destination}/{name_file}.txt'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced)
        convert_to_windows_format(BUCKET_SFTP,
                                             'bi/outbound/{path_destination}/{name_file}.txt'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             'bi/outbound/{path_destination}/{name_file}.txt'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")
        pass

def send_file_to_specific_bucket(specific_bucket,dataframe,application_id,name_file,path_destination,sep,header_value):
    """
             Send file to any bucket for internal users
                :param dataframe: bucket s3 , application_id: application of spark to make path ('bi/outbound/temp/local-1663088553000/') , name_file: name of file ,path_destination: path destionation of file,
                sep: separator of files. If we dont want a separator we pass the param 'None'
    """

    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name_file=name_file), sep='{}'.format(sep if sep in [',',';','|'] else ';'), index=False, header=header_value)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}'.
                                      format(application_id=application_id, name_file=name_file))
        if sep in [',',';','|']:
            file_replaced = file
        else:
            file_replaced = file.replace(';', '')

        # Disponibilizacion en specific bucket

        put_file_s3(specific_bucket,
                               '{path_destination}/{name_file}'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced)
        convert_to_windows_format(specific_bucket,
                                             '{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             '{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")

def send_file_to_specific_bucket_replace_quotes(specific_bucket,dataframe,application_id,name_file,path_destination,sep,header_value):
    """
             Send file to any bucket for internal users
                :param dataframe: bucket s3 , application_id: application of spark to make path ('bi/outbound/temp/local-1663088553000/') , name_file: name of file ,path_destination: path destionation of file,
                sep: separator of files. If we dont want a separator we pass the param 'None'
    """

    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name_file=name_file), sep='{}'.format(sep if sep in [',',';','|'] else ';'), index=False, header=header_value)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}'.
                                      format(application_id=application_id, name_file=name_file))
        if sep in [',',';','|']:
            file_replaced = file
        else:
            file_replaced = file.replace(';', '')

        file_replaced_quotes = file_replaced.replace('"', sep)

        # Disponibilizacion en specific bucket

        put_file_s3(specific_bucket,
                               '{path_destination}/{name_file}'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced_quotes)
        convert_to_windows_format(specific_bucket,
                                             '{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             '{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")


def start_a_crawler(crawler_name):
   session = boto3.session.Session()
   glue_client = session.client('glue')
   response = glue_client.start_crawler(Name=crawler_name)
   return response

def run_crawler(crawler: str, *, timeout_minutes: int = 120, retry_seconds: int = 5) -> None:
    """Run the specified AWS Glue crawler, waiting until completion."""
    # Ref: https://stackoverflow.com/a/66072347/
    timeout_seconds = timeout_minutes * 60
    client = boto3.client("glue")
    start_time = timeit.default_timer()
    abort_time = start_time + timeout_seconds

    def wait_until_ready() -> None:
        state_previous = None
        while True:
            response_get = client.get_crawler(Name=crawler)
            state = response_get["Crawler"]["State"]
            if state != state_previous:
                log.info(f"Crawler {crawler} is {state.lower()}.")
                state_previous = state
            if state == "READY":  # Other known states: RUNNING, STOPPING
                return
            if timeit.default_timer() > abort_time:
                raise TimeoutError(f"Failed to crawl {crawler}. The allocated time of {timeout_minutes:,} minutes has elapsed.")
            time.sleep(retry_seconds)

    wait_until_ready()
    response_start = client.start_crawler(Name=crawler)
    assert response_start["ResponseMetadata"]["HTTPStatusCode"] == 200
    log.info(f"Crawling {crawler}.")
    wait_until_ready()
    log.info(f"Crawled {crawler}.")


def get_metadata_postgre(query, secret, region):

    SECRET_AIRFLOW_POSTGRES = get_secrets(secret,region)
    URL='postgresql://{username}:{password}@{host}:{port}/{dbname}'.format(username=SECRET_AIRFLOW_POSTGRES.get('username'),password=SECRET_AIRFLOW_POSTGRES.get('password'),
                                                                           host=SECRET_AIRFLOW_POSTGRES.get('host'),port=SECRET_AIRFLOW_POSTGRES.get('port'),dbname=SECRET_AIRFLOW_POSTGRES.get('dbname'))
    ##GENERAMOS DATAFRAME A PARTIR DE LA QUERY
    return pd.read_sql(query,URL)

def get_metadata_postgre_ofas(query, username_key,password_key,host_key,port_key,dbname_key):

    SECRET = get_secrets(ARN_SECRET,'us-east-1')
    URL='postgresql://{username}:{password}@{host}:{port}/{dbname}'.format(username=SECRET.get('{}'.format(username_key)),password=SECRET.get('{}'.format(password_key)),
                                                                           host=SECRET.get('{}'.format(host_key)),port=SECRET.get('{}'.format(port_key)),dbname=SECRET.get('{}'.format(dbname_key)))
    ##GENERAMOS DATAFRAME A PARTIR DE LA QUERY
    return pd.read_sql(query,URL)

def file_exists(bucket, key):
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
        print(f"Key: '{key}' found!")
        return True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"File: '{key}' does not exist!")
        else:
            print("Something else went wrong")
            raise
        return False

def execute_alter_athena(query):
    session = boto3.Session()
    SECRET_ATHENA = get_secrets(
        "arn:aws:secretsmanager:us-east-1:248666061168:secret:use1-infra-data-ofas-bi-job-2l5IHT",
        "us-east-1")
    params = {
        'access_key': '{}'.format(SECRET_ATHENA.get('athena_access_id')),
        'secret_key': '{}'.format(SECRET_ATHENA.get('athena_access_key')),
        'region': 'us-east-1',
        'bucket': 'use1-tools-infrastructure-datalake-s3',
        'path': 'output',
        'query': '{}'.format(query)
    }
    client = session.client('athena',
                            aws_access_key_id=params['access_key'],
                            aws_secret_access_key=params['secret_key'],
                            region_name=params["region"])

    response = client.start_query_execution(
        QueryString=params["query"],
        ResultConfiguration={
            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path']
        }
    )
    execution_id = response['QueryExecutionId']
    state = 'RUNNING'
    max_execution = 5
    while (max_execution > 0 and state in ['RUNNING', 'QUEUED']):
        max_execution = max_execution - 1
        response = client.get_query_execution(QueryExecutionId=execution_id)

        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']
            if state == 'FAILED':
                print("Error en query metadata")
            elif state == 'SUCCEEDED':
                print("Query metadata ejecuta correctamente")
        time.sleep(1)
