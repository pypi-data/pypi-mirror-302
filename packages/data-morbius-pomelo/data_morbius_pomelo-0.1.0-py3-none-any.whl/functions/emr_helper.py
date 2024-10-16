#GENERAL VARIABLES
from airflow.models import Variable
#from datetime import datetime,timezone
from airflow.exceptions import AirflowException, AirflowFailException
from botocore.exceptions import ClientError
import time
import logging
from ast import literal_eval
import json
import datetime


#temp_credentials=TemporaryCredentials("dag_id", region='us-east-1')
#emr_client=temp_credentials.get_client('emr')
failed_states = {"FAILED", "CANCELLED", "INTERRUPTED", "CANCEL_PENDING"}
non_terminal_states = {"PENDING", "RUNNING"}
completed_states = {"COMPLETED"}

########################################
######  *** CLUSTER FUNCTIONS *** ######
########################################

def create_emr(emr_client, config_map, steps, cluster_name=None,**kwargs):
    if cluster_name:
        cluster_name = cluster_name
    else:
        cluster_name = kwargs['params']['emr_name']
    if (type(steps) == str):
            steps = literal_eval(steps) #Método para interpretar el string como una List<Dict>
    cluster_id = create_cluster(emr_client,config_map.JOB_FLOW_OVERRIDES, cluster_name, steps)
    return cluster_id

def create_empty_emr(emr_client, config_map, emr_name=None,**kwargs):
    steps = []
    cluster_id = create_cluster(emr_client,config_map.JOB_FLOW_OVERRIDES,emr_name, steps)
    return cluster_id

def create_cluster(emr_client,job_flow_overrides,cluster_name, steps):
    config = job_flow_overrides
    response = emr_client.run_job_flow(
        Name=cluster_name,
        LogUri=config.get('LogUri'),
        ReleaseLabel=config.get('ReleaseLabel'),
        Instances=config.get('Instances'),
        Steps=steps,
        BootstrapActions=config.get('BootstrapActions', []),
        StepConcurrencyLevel=config.get('StepConcurrencyLevel'),
        Applications=config.get('Applications'),
        Configurations=config.get('Configurations', []),
        VisibleToAllUsers=config.get('VisibleToAllUsers'),
        JobFlowRole=config.get('JobFlowRole'),
        ServiceRole=config.get('ServiceRole'),
        SecurityConfiguration=config.get('SecurityConfiguration'),
        Tags=config.get('Tags')
    )
    return response['JobFlowId']

def get_cluster_status(emr_client, clusterStates=['RUNNING'] , emr_name=None , **kwargs):
    if emr_name:
        emr_name = emr_name
    else:
        emr_name = kwargs['params']['emr_name']
    clusters = emr_client.list_clusters(ClusterStates=clusterStates)
    for i in clusters['Clusters']:
        if i['Name'] == emr_name:
            return i['Id']
    raise AirflowException(f'No EMR cluster running with name {emr_name}')

########################################
######  *** STEPS FUNCTIONS *** ######
########################################

def add_steps_specific_cluster(emr_client, cluster_id, steps, **kwargs):
    if (type(steps) == str):
        steps = literal_eval(steps)

    print (f'clusted_id param: {cluster_id}')
    if not cluster_id:
        raise AirflowException(f"No cluster found for name: {cluster_id}")

    logging.info(f"Adding steps to {cluster_id}")

    response = emr_client.add_job_flow_steps(JobFlowId=cluster_id, Steps=steps)

    if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        raise AirflowException("Adding steps failed: %s" % response)
    else:
        logging.info("Steps %s added to JobFlow", response["StepIds"])
        return response["StepIds"]

def create_step_execution(name_step="Job-Executor", cores=1, instance=1, memory = "2G", memory_overhead_executor="1G",memory_overhead_driver="1G", parallelism=10,dynamic_allocation_enabled="false", streaming_dynamic_allocation="true", streaming_dynamic_allocation_min_executors="1",streaming_dynamic_allocation_max_executors="2",py_files="s3://use1-infra-infrastructure-infradatabi-repo-sync-s3/dist/utilities-0.1-py3-none-any.whl", jars="""s3://use1-tools-infrastructure-datalake-s3/python/jars/AthenaJDBC42_2.0.25.1001.jar""",script_file="s3://use1-prd-infrastructure-datalake-s3/code/emr/holamundo.py",parameters_script_file="",app_name="App-Job-Executor"):
    steps=[]
    item= {
        "Name": name_step,
        "ActionOnFailure": "CONTINUE",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                    "spark-submit",
                "--deploy-mode" ,"cluster",
                "--conf", f"spark.executor.cores={cores}",
                "--conf", f"spark.executor.instances={instance}",
                "--conf", f"spark.executor.memory={memory}",
                "--conf", f"spark.executor.memoryOverhead={memory_overhead_executor}",
                "--conf", f"spark.driver.memoryOverhead={memory_overhead_driver}",
                "--conf", f"spark.default.parallelism={parallelism}",
                "--conf", f"spark.dynamicAllocation.enabled={dynamic_allocation_enabled}",
                "--conf", f"spark.streaming.dynamicAllocation.enabled={streaming_dynamic_allocation}",
                "--conf", f"spark.streaming.dynamicAllocation.minExecutors={streaming_dynamic_allocation_min_executors}",
                "--conf", f"spark.streaming.dynamicAllocation.maxExecutors={streaming_dynamic_allocation_max_executors}",
                "--master", "yarn",
                "--conf", "spark.yarn.submit.waitAppCompletion=true",
                "--py-files", f"{py_files}",
                "--jars", f"{jars}",
                f"{script_file}"
            ] + parameters_script_file.split(),
        }
    }
    steps.append(item)
    return steps

def get_step_status(emr_client, emr_name,step_raw_name,cluster_id,  **kwargs):
    step_raw_name = step_raw_name
    emr_raw_name = emr_name
    steps = emr_client.list_steps(ClusterId=cluster_id)
    for i in steps['Steps']:
        if i['Name'] == step_raw_name and i['Status']['State'] == 'RUNNING':
            return i['Id']
    raise AirflowException(f'No Step running with name ${emr_raw_name}')


def wait_for_steps_completions(emr_client,cluster_id, step_ids=[], **kwargs):
    response = emr_client.list_steps(ClusterId=cluster_id)
    if (type(step_ids) == str):
        step_ids = literal_eval(step_ids)

    if len(step_ids)== 0:
        [step_ids.append(i['Id']) for i in response['Steps']]

    failed_steps_list = []
    check_interval = 60

    for step_id in step_ids:
        running = True
        sec = 0

        while running:
            logging.info(f"Waiting step: {step_id}")
            sec += check_interval

            try:
                response = emr_client.describe_step(ClusterId=cluster_id, StepId=step_id)
                status = response["Step"]["Status"]["State"]
                logging.info(
                    f"Job still running for {sec} seconds... current status is {status}"
                )
            except KeyError:
                raise AirflowException("Could not get status of the EMR job")
            except ClientError:
                raise AirflowException("AWS request failed, check logs for more info")

            if status in non_terminal_states:
                running = True
                time.sleep(check_interval)
            if status in failed_states:
                failed_steps_list.append(step_id)
                running = False
            if status in completed_states:
                running = False

        logging.info(f"EMR {step_id} completed")

    if len(failed_steps_list):
        failed_steps = ",".join(failed_steps_list)
        raise AirflowException(f"Failed steps: {failed_steps}, check emr")



###############################################
######  *** EMR STREAMING MONITORING *** ######
###############################################

def get_running_streaming_clusters(emr_client, environment):
#    # Create a boto3 session to access the AWS EMR service
#    session = boto3.Session(region_name='us-east-1')
#    client = session.client('emr')
    
    # Call the list_clusters method to get a list of all the running clusters
    running_states = ['STARTING','BOOTSTRAPPING','RUNNING']
    response = emr_client.list_clusters(ClusterStates=running_states)
    
    # Extract the list of running clusters from the response
    running_clusters = response['Clusters']

    running_streaming_clusters = {'Clusters':[]}
    for cluster in running_clusters:
        if cluster.get('Name').startswith(f'use1-{environment}-streaming'):
            running_streaming_clusters['Clusters'].append(cluster)
    # Return the list of running streaming clusters
    return running_streaming_clusters


def read_from_s3(s3_client, environment):
    BUCKET_PREFIX = f'use1-{environment}-infrastructure-datalake-s3'
    PATH_TO_EMR_FILE = 'files/emr_streaming/'
   #Create a boto3 session to access the AWS S3 service
   #session = boto3.Session(region_name='us-east-1')
   #s3 = session.client('s3')

    #get the list of all files in the S3 bucket
    response = s3_client.list_objects(Bucket=BUCKET_PREFIX, Prefix=PATH_TO_EMR_FILE)
    
    #extract the files
    files = response.get('Contents', [])
    
    if len(files) == 0:
        #create an empty file in the directory if there are no files
        empty_file = f"{PATH_TO_EMR_FILE}/empty.json"
        s3_client.put_object(Bucket=BUCKET_PREFIX, Key=empty_file, Body="")
        
        #return the path of the empty file
        return empty_file
    
    #returns the path of the most recent file in the path
    files.sort(key=lambda x: x['LastModified'], reverse=True)
    if len(files) > 0:
        return files[0]['Key']
    else:
        return None


def write_to_s3(s3_client, environment, cluster_list):
    BUCKET_PREFIX = f'use1-{environment}-infrastructure-datalake-s3'
    PATH_TO_EMR_FILE = 'files/emr_streaming/'
#    # Create a boto3 session to access the AWS S3 service
#    session = boto3.Session(region_name='us-east-1')
#    s3 = session.client('s3')
    
    # Generate a filename based on the current date and time
    now = datetime.datetime.now()
    filename = f'running-clusters-{now.strftime("%Y%m%d-%H%M%S")}.json'
    
    # Write the cluster list to the file
    s3_client.put_object(Bucket=BUCKET_PREFIX, Key=f'{PATH_TO_EMR_FILE}{filename}', Body=json.dumps(cluster_list, indent=4, sort_keys=True, default=str))
    
def clone_emr_cluster(emr_client, environment, cluster_id):
#    emr = boto3.client("emr", 'us-east-1')

    # Get the configuration of the terminated cluster
    terminated_cluster = emr_client.describe_cluster(ClusterId=cluster_id)
    
    terminated_steps = emr_client.list_steps(ClusterId=cluster_id)
    for step in terminated_steps["Steps"]:
        step.pop("Id")
        step.pop("Status")
        step["Config"].pop("Properties")
        step["HadoopJarStep"] = step.pop("Config")

    # Get the EC2 instance attributes
    ec2_instance_attributes = terminated_cluster["Cluster"]["Ec2InstanceAttributes"]
    # Get the list of instance groups
    instance_group_list = emr_client.list_instance_groups(ClusterId=cluster_id)
    instance_group_list.pop('ResponseMetadata')
    for instance in instance_group_list.get('InstanceGroups'):
        instance.pop('Id','')
        instance.pop('Status','')
        instance.pop('LastSuccessfullyAppliedConfigurations','')
        instance.pop('LastSuccessfullyAppliedConfigurationsVersion','')
        instance.pop('RunningInstanceCount','')
        instance.pop('ConfigurationsVersion','')
        instance.pop('EbsBlockDevices','') 
        instance.pop('ShrinkPolicy','')        
        instance['GroupType'] = instance.pop('InstanceGroupType')
        instance['InstanceCount'] = instance.pop('RequestedInstanceCount')
        instance['InstanceRole'] = instance.pop('GroupType')
        if 'EbsOptimized' in instance:
            instance['EbsConfiguration'] = {'EbsOptimized': instance['EbsOptimized']}
            del  instance['EbsOptimized']
    instance_group_list["Ec2SubnetId"] = ec2_instance_attributes['Ec2SubnetId']

    bootstrap_actions = emr_client.list_bootstrap_actions(ClusterId=cluster_id)
    bootstrap_actions.pop('ResponseMetadata')
    for action in  bootstrap_actions['BootstrapActions']:
        action['ScriptBootstrapAction']= { 'Path' : action.pop('ScriptPath'), 
                                           'Args' : action.pop('Args')  }
 
    terminated_cluster_name = terminated_cluster["Cluster"]["Name"]
    
    if not terminated_cluster_name.startswith(f'use1-{environment}-streaming'):
        terminated_cluster_name = terminated_cluster_name.replace(f'use1-{environment}',f'use1-{environment}-streaming')

        
    if terminated_cluster["Cluster"]["Status"]["State"] == 'WAITING':
        print(f"{cluster_id} cluster is in WAITING State. Terminating...")
        # Terminate the cluster
        try:
            response = emr_client.set_termination_protection(
                JobFlowIds=[cluster_id],
                TerminationProtected=False
            )
            logging.info(f"Set Termination Protection False on Cluster_id {cluster_id}")
        except InternalServerError:
            raise AirflowException("Could not set termination protection")
        try:
            logging.info(f"Terminating Cluster_id {cluster_id} ... ")
            emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
        except InternalServerError:
            raise AirflowException(f"Could not terminate cluster_id {cluster_id}")

    for app in terminated_cluster["Cluster"]["Applications"]:
        app.pop('Version')

    print("Creating new cluster")
    # Use the same configuration to start a new cluster
    new_cluster = emr_client.run_job_flow(
        Name=terminated_cluster_name,
        LogUri=terminated_cluster["Cluster"]["LogUri"],
        ReleaseLabel=terminated_cluster["Cluster"]["ReleaseLabel"],
        Instances=instance_group_list,
        Applications=terminated_cluster["Cluster"]["Applications"],
        Configurations=terminated_cluster["Cluster"]["Configurations"],
        ServiceRole=terminated_cluster["Cluster"]["ServiceRole"],
        JobFlowRole=terminated_cluster["Cluster"]["Ec2InstanceAttributes"]["IamInstanceProfile"],
        Steps = terminated_steps["Steps"],
        VisibleToAllUsers=terminated_cluster["Cluster"]["VisibleToAllUsers"],
        Tags=terminated_cluster["Cluster"]["Tags"],
        SecurityConfiguration='default',
        BootstrapActions = bootstrap_actions['BootstrapActions']
    )
    print(f"Finish creating new cluster. new_cluster_id:{new_cluster['JobFlowId']}")

    # Return the ID of the new cluster
    return new_cluster["JobFlowId"]


def monitor_emr_streaming(emr_client, s3_client, environment):
    BUCKET_PREFIX = f'use1-{environment}-infrastructure-datalake-s3'
    PATH_TO_EMR_FILE = 'files/emr_streaming/'

    print("Read the most recent file from s3...")
    # Read the most recent file in the S3 bucket
    filename = read_from_s3(s3_client, environment)

    # Get the list of running clusters
    print("Obtaining EMR Running Clusters...")
    running_clusters = get_running_streaming_clusters(emr_client, environment)

    # If there's an existing file in the S3 bucket, check the status of each cluster in the file
    if filename:
        # Read the contents of the file
        print("Obtaining file content before checking if the clusters are running")
        file_content = s3_client.get_object(Bucket=BUCKET_PREFIX, Key=f'{filename}')["Body"].read().decode("utf-8")

        if file_content:
            saved_clusters = json.loads(file_content).get('Clusters')
            # resto del código
        else:
            print("A file was not found in the directory")
            saved_clusters = []

        found = False
        cluster_id_aux = []
        for saved_cluster in saved_clusters:
            saved_cluster_id = saved_cluster.get('Id')
            saved_cluster_name = saved_cluster.get('Name')
            for running_cluster in running_clusters.get('Clusters'):
                running_cluster_id = running_cluster.get('Id')
                running_cluster_status = running_cluster.get('Status').get('State')
                if saved_cluster_id == running_cluster_id:
                    print(f'{saved_cluster_id} se encuentra arriba y esta running')
                    found = True
                    break
            if found:
                found = False
                continue

            print(f'{saved_cluster_id} no se encuentra arriba. Debemos clonarlo')
            new_cluster_id = clone_emr_cluster(emr_client, environment, saved_cluster_id)
            cluster_id_aux.append((new_cluster_id, saved_cluster_id, saved_cluster_name))

        print("Finaliza chequeo de clusters")
        print("Lista de nuevos clusters")
        print(cluster_id_aux)

        print("Obtaining EMR Running Clusters...")
        running_clusters = get_running_streaming_clusters(emr_client, environment)

        for cluster in running_clusters.get('Clusters'):
            for aux in cluster_id_aux:
                # Nos fijamos si el id del running cluster se corresponde con el alguno de los ID viejos
                if cluster.get('Id') == aux[0]:
                    cluster['oldId'] = aux[1]

    print('Writing running_clusters to s3')
    write_to_s3(s3_client, environment, running_clusters)
