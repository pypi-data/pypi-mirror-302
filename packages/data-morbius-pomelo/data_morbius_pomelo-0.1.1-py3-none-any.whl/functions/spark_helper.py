import boto3
#from pyspark.sql import SparkSession
from utilities import aws_helper
#from pyspark.context import SparkContext

BUCKET_TOOLS = 'use1-tools-infrastructure-datalake-s3'

'''def get_context(app_name):
    print("Setting Spark Session")
    spark = SparkSession \
        .builder \
        .appName(app_name) \
        .getOrCreate()
    spark.sparkContext._jsc.hadoopConfiguration().set('fs.s3.canned.acl', 'BucketOwnerFullControl')

    # Properties para no generar archivos file$ en S3
    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    # Properties para que el overwrite no pise toda la tabla, sino las particiones a reemplazar
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "DYNAMIC")
    return spark'''

def to_csv(df, application_id, file_name, bucket_destination, path_destination,file_extension,sep,header_value):
    """
        Export Pyspark Dataframe to file with file_name in bucket s3
        :param
            df: dataframe,
            application_id:
            application_id,
            file_name: file_name,
            bucket_destination: bucket s3 ,
            path_destination: path destination will be end '/'
        :return file
    """

    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    if df.count() > 0:
        temp_bucket = BUCKET_TOOLS
        print(f'temp_bucket: {temp_bucket}')
        temp_prefix = f'bi/outbound/temp/{application_id}/'
        print(f'temp_prefix: {temp_prefix}')
        prefix_target = f'{path_destination}{file_name}.{file_extension}'
        print(f'prefix_target: {prefix_target}')
        df.coalesce(1).write.options(header=header_value,delimiter='{}'.format(sep if sep in [',',';','|'] else ';'),escape='\"').mode('overwrite').csv(f's3://{temp_bucket}/{temp_prefix}')

        object_s3 = s3_client.list_objects(Bucket=BUCKET_TOOLS,Prefix=temp_prefix,Delimiter='/')
        print(object_s3)
        temp_name_file = ''
        for object in object_s3.get('Contents'):
            if object.get('Key').endswith('.csv'):
                # object onboarding/part-00000-f676d0be-e9b7-4e98-a8a0-7022ccae86d5-c000.csv
                # temp_name_file=part-00000-f676d0be-e9b7-4e98-a8a0-7022ccae86d5-c000.csv
                temp_name_file = object.get('Key').split('/')[-1]
                print(f'Se detectó un file temporal en s3://{temp_bucket}/{temp_prefix}{temp_name_file}')
                print('Archivo copiandose a {}'.format(bucket_destination+'/'+prefix_target))
                print('Archivo copiandose de {}'.format(f'{temp_bucket}/{temp_prefix}{temp_name_file}'))
                if sep not in [',', ';', '|']:
                    file = aws_helper.get_file_s3(temp_bucket,f'{temp_prefix}{temp_name_file}')
                    file_replaced = file.replace(';', '').replace('♲',' ')
                    aws_helper.put_file_s3(temp_bucket, f'{temp_prefix}{temp_name_file}', file_replaced)
                TO_REPLACE = b'""'
                REPLACER = b''
                s3_obj = boto3.client('s3')
                s3_clientobj = s3_obj.get_object(Bucket=temp_bucket, Key=f'{temp_prefix}{temp_name_file}')
                s3_clientdata = s3_clientobj['Body'].read()
                file_replace = s3_clientdata.replace(TO_REPLACE, REPLACER)
                aws_helper.put_file_s3(bucket_destination, prefix_target, file_replace)
                print("Entramos en windows converter")
                aws_helper.convert_to_windows_format(bucket_destination,'{}'.format(prefix_target),'{}'.format(prefix_target))
                print('Archivo copiado')
                aws_helper.delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        if (temp_name_file == ''):
            print(f"No se encontró un archivo con la exntesión {file_extension} en el path s3://{temp_bucket}/{temp_prefix}{temp_name_file}")


    else:
        print("No se genero archivo por falta de informacion")

def to_csv_replacer_always(df, application_id, file_name, bucket_destination, path_destination,file_extension,sep,header_value):
    """
        Export Pyspark Dataframe to file with file_name in bucket s3
        :param
            df: dataframe,
            application_id:
            application_id,
            file_name: file_name,
            bucket_destination: bucket s3 ,
            path_destination: path destination will be end '/'
        :return file
    """

    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    if df.count() > 0:
        temp_bucket = BUCKET_TOOLS
        print(f'temp_bucket: {temp_bucket}')
        temp_prefix = f'bi/outbound/temp/{application_id}/'
        print(f'temp_prefix: {temp_prefix}')
        prefix_target = f'{path_destination}{file_name}.{file_extension}'
        print(f'prefix_target: {prefix_target}')
        df.coalesce(1).write.options(header=header_value,delimiter='{}'.format(sep if sep in [',',';','|'] else ';'),escape='\"').mode('overwrite').csv(f's3://{temp_bucket}/{temp_prefix}')

        object_s3 = s3_client.list_objects(Bucket=BUCKET_TOOLS,Prefix=temp_prefix,Delimiter='/')
        print(object_s3)
        temp_name_file = ''
        for object in object_s3.get('Contents'):
            if object.get('Key').endswith('.csv'):
                # object onboarding/part-00000-f676d0be-e9b7-4e98-a8a0-7022ccae86d5-c000.csv
                # temp_name_file=part-00000-f676d0be-e9b7-4e98-a8a0-7022ccae86d5-c000.csv
                temp_name_file = object.get('Key').split('/')[-1]
                print(f'Se detectó un file temporal en s3://{temp_bucket}/{temp_prefix}{temp_name_file}')
                print('Archivo copiandose a {}'.format(bucket_destination+'/'+prefix_target))
                print('Archivo copiandose de {}'.format(f'{temp_bucket}/{temp_prefix}{temp_name_file}'))
                file = aws_helper.get_file_s3(temp_bucket,f'{temp_prefix}{temp_name_file}')
                file_replaced = file.replace(';', '').replace('♲',' ')
                aws_helper.put_file_s3(temp_bucket, f'{temp_prefix}{temp_name_file}', file_replaced)
                TO_REPLACE = b'""'
                REPLACER = b''
                s3_obj = boto3.client('s3')
                s3_clientobj = s3_obj.get_object(Bucket=temp_bucket, Key=f'{temp_prefix}{temp_name_file}')
                s3_clientdata = s3_clientobj['Body'].read()
                file_replace = s3_clientdata.replace(TO_REPLACE, REPLACER)
                aws_helper.put_file_s3(bucket_destination, prefix_target, file_replace)
                print("Entramos en windows converter")
                aws_helper.convert_to_windows_format(bucket_destination,'{}'.format(prefix_target),'{}'.format(prefix_target))
                print('Archivo copiado')
                aws_helper.delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        if (temp_name_file == ''):
            print(f"No se encontró un archivo con la exntesión {file_extension} en el path s3://{temp_bucket}/{temp_prefix}{temp_name_file}")


    else:
        print("No se genero archivo por falta de informacion")