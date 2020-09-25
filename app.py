from flask import Flask,request,Response
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings,TurnContext,ConversationState,MemoryStorage,UserState
from botbuilder.schema import Activity
import asyncio
from botdialog import BotDialog
from botbuilder.azure import CosmosDbPartitionedStorage, CosmosDbPartitionedConfig

app = Flask(__name__)
loop = asyncio.get_event_loop()

botsettings = BotFrameworkAdapterSettings("","")
botadapter = BotFrameworkAdapter(botsettings)

memstore = MemoryStorage()
CONMEMORY = ConversationState(memstore)
userstate = UserState(memstore)


key = "jxbaXcJPMuaqnInF22EumWepd79R38nyfkrNXzHJB7EaGB2XkiUkaAOYU1r4GrbCiDNeAAaYJFoDA1okvesP3Q=="
cosmos_config = CosmosDbPartitionedConfig(
        cosmos_db_endpoint="https://joecosmostest.documents.azure.com:443",
        auth_key=key,
        database_id="userprofile",
        container_id="userinfo",
        compatibility_mode = False
    )
cosdbStore = CosmosDbPartitionedStorage(cosmos_config)

botdialog = BotDialog(CONMEMORY,userstate, cosdbStore)

@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await botdialog.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)


if __name__ == '__main__':
    app.run('localhost',3978)
