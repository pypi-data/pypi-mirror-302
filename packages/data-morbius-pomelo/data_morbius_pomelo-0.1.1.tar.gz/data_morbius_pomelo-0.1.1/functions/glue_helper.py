#GENERAL VARIABLES
from airflow.models import Variable
from datetime import datetime,timezone
from airflow.exceptions import AirflowException, AirflowFailException
import botocore
import time
import logging
from ast import literal_eval
import logging
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

########################################
######  *** GLUE FUNCTIONS *** ######
########################################

def wait_glue_job(glue_client, glue_job_name, job_run_id, **kwargs):
    # print(f"VALIDATING GLUE JOB RUN {job_run_id}")
    logger.info(f'Validating Glue Job Run {job_run_id}')
    try:
        state = glue_client.get_job_run(JobName=glue_job_name, RunId=job_run_id)
        if state:
            status = state['JobRun']['JobRunState']
            while status not in ['SUCCEEDED']:
                logger.info('Waiting Job...')
                time.sleep(55)
                job_status = glue_client.get_job_run(JobName=glue_job_name, RunId=job_run_id)
                status = job_status['JobRun']['JobRunState']
                logger.info('Checking the status...')
                logger.info(f'Current status is {status}')
                # print("Checking the status...")
                # print("Current status is: ", status)
                if status in ['ERROR', 'TIMEOUT', 'FAILED', 'STOPPED', 'STOPPED', 'STOPPING']:
                    logger.info(f"The final status of the job is {status}")
                    raise AirflowFailException(f"Job status is {status}")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            logger.error('An error occurred while creating the Glue job. Check your input parameters.')
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            logger.error(f'An error occurred while creating the Glue job. The job {glue_job_name} was not found')
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            logger.error(
                'An error occurred while creating the Glue job. The connection could not be established successfully, timeout.')
        else:
            raise error


def run_customer_job(glue_client, glue_job_name, glue_job_arguments, process_date, **kwargs):
    glue_job_arguments = glue_job_arguments.replace("'", '''"''')
    glue_job_arguments = json.loads(glue_job_arguments)

    if "--process_date" in glue_job_arguments.keys():
        glue_job_arguments["--process_date"] = process_date
        logger.info('Setting process date as the glue job argument.')
    else:
        glue_job_arguments["--process_date"] = process_date
        logger.info('Adding "--process_date" as an argument to the glue job.')

    logger.info('Adding "--Owner" an argument to the glue job.')
    glue_job_arguments["--dag_run_id"] = str(kwargs['dag_run'])
    response = None
    try:
        logger.info('Starting glue Job')
        response = glue_client.start_job_run(
            JobName=glue_job_name ,
            Arguments=glue_job_arguments
        )
        logger.info(
            f"The execution of the job {glue_job_name} was triggered with the following job_run_id={response['JobRunId']}")

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInputException':
            logger.error('An error occurred while creating the Glue job. Check your input parameters.')
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            logger.error(f'An error occurred while creating the Glue job. The job {glue_job_name} was not found')
        if error.response['Error']['Code'] == 'ConcurrentRunsExceededException':
            logger.error('An error occurred while creating the Glue job. The job is currently running or ending.')
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            logger.error(
                'An error occurred while creating the Glue job. The connection could not be established successfully, timeout.')
        else:
            raise error

    return response["JobRunId"]


def get_glue_job(glue_client, glue_job_name, glue_job_arguments, **kwargs):
    print("Getting glue Job")
    response = glue_client.get_job(
        JobName=glue_job_name,
    )
    return response


def get_glue_job_runs(glue_client, glue_job_name, glue_job_arguments, **kwargs):
    print("Getting glue Job")
    response = glue_client.get_job_runs(
        JobName=glue_job_name
    )
    return response


def run_crawler_job(glue_client, crawler_job_name, **kwargs):
    logger.info(f'Starting Crawler job {crawler_job_name}')
    response = None
    try:
        response = glue_client.start_crawler(Name=crawler_job_name)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            logger.error(f'An error occurred while try run CrawlerJob. Name {crawler_job_name} was not found')
        if error.response['Error']['Code'] == 'CrawlerRunningException':
            logger.error('An error occurred while try run CrawlerJob. The job is currently running or ending.')
        if error.response['Error']['Code'] == 'OperationTimeoutException':
            logger.error('An error occurred while creating the Glue job. The connection could not be established successfully, timeout.')
        else:
            raise error
    return response