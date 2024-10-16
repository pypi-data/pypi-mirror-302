from utilities import aws_helper
import tableauserverclient as TSC
import pandas as pd
import xmltodict

SERVER_URL='https://tableau.tools.pomelo.la'
SERVER_API_VERSION='3.15'
SITE_NAME='Pomelo'

def login_server():
    SECRET_TABLEAU = aws_helper.get_secrets(
        "arn:aws:secretsmanager:us-east-1:644197204120:secret:data/bi/tableau_credentials-1PfxO7",
        "us-east-1")
    user = SECRET_TABLEAU.get('tableau_credential_user')
    password = SECRET_TABLEAU.get('tableau_credential_pass')
    server = TSC.Server(SERVER_URL)
    server.version = '3.15'
    tableau_auth = TSC.TableauAuth(user, password)
    return server.auth.sign_in(tableau_auth),server

def get_metadata_graphql(query,server):
    result = server.metadata.query(query)
    if result.get("data"):
        print("### Results:")
    return result

def get_metadata_postgre(query):
    SECRET_POSTGRE = aws_helper.get_secrets(
        "arn:aws:secretsmanager:us-east-1:644197204120:secret:data/bi/metadata_tableau-u9AXUp",
        "us-east-1")
    URL='postgresql://{username}:{password}@{host}:{port}/{dbname}'.format(username=SECRET_POSTGRE.get('username'),password=SECRET_POSTGRE.get('password'),
                                                                           host=SECRET_POSTGRE.get('host'),port=SECRET_POSTGRE.get('port'),dbname=SECRET_POSTGRE.get('dbname'))
    ##GENERAMOS DATAFRAME A PARTIR DE LA QUERY
    return pd.read_sql(query,URL)


def refresh_tableau_extract(datasource_id,login,server):
    """
    Generate a full refresh of an extract in Tableau Server.
    :param datasource_id: id of datasource that we want to update, login: Tableau server session, server: server varaible of Tableu to make operations
    """
    with login:
        print('connection made')
        print(server.version)
        print(server.site_id)
        #Get datasource resource by id
        resource = server.datasources.get_by_id(datasource_id)
        print(resource)
        #Generate job of refresh extract of datasource
        job = server.datasources.refresh(resource)
        print(job)
        print(f"Update job posted (ID: {job.id})")
        print("Waiting for JOB...")
        # `wait_for_job` will throw if the job isn't executed successfully
        server.jobs.wait_for_job(job)
        print("JOB Refresh extract finished succesfully")

def refresh_incremental_extract(task_id,login,server):
    """
    Simulate a incremental refresh of an extract in Tableau Server. This function execute a task that have a schedule program linked
    :param datasource_id: id of datasource that we want to update, login: Tableau server session, server: server varaible of Tableu to make operations
    """
    with login:
        task = server.tasks.get_by_id(task_id)
        print("Execute task ")
        print(task)
        update_xml=server.tasks.run(task)
        print(update_xml)
        #print(f"Update job posted (ID: {job.id})")
        print("Waiting for JOB...")
        job_id = xmltodict.parse(update_xml)['tsResponse']['job']['@id']
        print(f"Refresh extract job {job_id} created")
        # `wait_for_job` will throw if the job isn't executed successfully
        job=server.jobs.get_by_id(job_id)
        server.jobs.wait_for_job(job)
        print("JOB Refresh extract finished succesfully")

def update_credential_datasource(datasource_id,login,server,user_target,pass_target):
    """
    Update cretendials of datasource
    :param datasource_id: id of datasource that we want to update, login: Tableau server session, server: server varaible of Tableu to make operations, secret: arn secret in aws to get value
    """

    with login:
        endpoint = {"workbook": server.workbooks, "datasource": server.datasources}.get("datasource")
        update_function = endpoint.update_connection
        datasource = server.datasources.get_by_id(datasource_id)
        server.datasources.populate_connections(datasource)
        connection = datasource.connections[0]
        connections = list(filter(lambda x: x.id == connection.id, datasource.connections))
        assert len(connections) == 1
        connection = connections[0]
        connection.username = user_target
        connection.password = pass_target
        connection.embed_password = True
        print(update_function(datasource, connection).__dict__)

def create_user(server, login, username, email, full_name, site_role='Viewer'):
    """
    Create a new user
    :param username: Username -- client_id
    :param email: Email for the new user -- not for clients embedded
    :param full_name: Full name -- client name
    :param site_role: Role [Creator, Explorer, Viewer...]
    """
    with login:
        new_user = TSC.User(username, email, full_name, site_role)
        server.users.add(new_user)
        print(f"usuario '{full_name}' creado.")
        # print(f"Error creating user '{full_name}': {e}")

def delete_user(server, login, username):
    """
       Delete an existing user
       :param username: Username -- client_id o mail de persona
       """
    with login:
        user = server.users.get_by_name(username)
        server.users.remove(user)
        print(f"Removed user {username}'")
        #print(f"Error removing user '{client_id}': {e}")

def add_user_to_group(server, login, username, group_name):
    """
    Add a user to a group
    :param username: Username -- client_id or mail
    :param group_name: Name of the group
    """
    with login:
        user = server.users.get_by_name(username)
        group = server.groups.get_by_name(group_name)
        if user and group:
            server.groups.add_user(group, user)
            print("Usuario agregado")
        else:
            print("Fallo algo")