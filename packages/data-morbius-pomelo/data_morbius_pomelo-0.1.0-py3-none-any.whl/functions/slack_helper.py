from slack import WebClient
from slack.errors import SlackApiError
#from slack_sdk.errors import SlackApiError

# Permite adjuntar un archivo a un canal de Salck mediante una App con Token (La app debe estar agregada en el canal)
def notification_slack_attachment(slack_token, slack_channel, message, emoji, name_attachment,file_extension, df_data, header_row):
    # Authenticate to the Slack API via the generated token
    client = WebClient(slack_token)
    # Send csv file
    client.files_upload(
        channels=slack_channel,
        initial_comment="{} - {}".format(emoji, message),
        filename="{}.{}".format(name_attachment,file_extension),
        content=df_data.toPandas().to_csv(index=False, float_format='{:f}'.format, header=header_row))

# Permite enviar un mensaje a un canal de Salck mediante una App con Token (La app debe estar agregada en el canal)
def notification_slack_message(slack_token, slack_channel, message, emoji):
    # Authenticate to the Slack API via the generated token
    client = WebClient(slack_token)
    # Send a simple message
    response = client.chat_postMessage(channel=slack_channel,
                                       text="{} - {}".format(emoji,message))


# Permite adjuntar un archivo a un canal de Salck mediante una App con Token (La app debe estar agregada en el canal)
def notification_slack_attachment_pd(slack_token, slack_channel, message, emoji, name_attachment,file_extension, df_data):
    # Authenticate to the Slack API via the generated token
    client = WebClient(slack_token)
    # Send csv file
    client.files_upload(
        channels=slack_channel,
        initial_comment="{} - {}".format(emoji, message),
        filename="{}.{}".format(name_attachment,file_extension),
        content=df_data.to_csv(index=False, float_format='{:f}'.format))