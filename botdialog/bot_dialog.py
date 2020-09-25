from botbuilder.core import TurnContext,ActivityHandler,ConversationState,MessageFactory, UserState, CardFactory
from botbuilder.dialogs import DialogSet,WaterfallDialog,WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt,NumberPrompt,PromptOptions
from botbuilder.schema import Activity, Attachment, ActivityTypes, AttachmentLayoutTypes, AnimationCard, ThumbnailCard, SuggestedActions, ChannelAccount, HeroCard, VideoCard, CardImage, CardAction, MediaUrl, ActionTypes
from botbuilder.azure import CosmosDbPartitionedStorage
from typing import List, Union
from datetime import datetime
import smtplib
import ssl
import json

from .data_model import UserProfile

class BotDialog(ActivityHandler):
    def __init__(self, conversation:ConversationState, userstate:UserState, cosdbStore:CosmosDbPartitionedStorage):
        self.con_statea = conversation
        self.userstate = userstate
        self.cosmodb = cosdbStore

        
        self.conprop = self.con_statea.create_property("constate")
        self.userprop = self.userstate.create_property("userstate")

        self.state_prop = self.con_statea.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)
        self.dialog_set.add(TextPrompt("text_prompt"))
        self.dialog_set.add(NumberPrompt("number_prompt"))
        self.dialog_set.add(WaterfallDialog("main_dialog",[self.Hello, self.MoodCarousel,self.NegativeMoodCarousel,self.Completed]))


    async def Hello(self,waterfall_step:WaterfallStepContext):
        return await waterfall_step.context.send_activity(
            f"Hi there! What is your name?"
        )


       

    async def MoodCarousel(self,waterfall_step:WaterfallStepContext):
        waterfall_step.values["username"] = waterfall_step._turn_context.activity.text

        reply = MessageFactory.list([])
        reply.attachment_layout = AttachmentLayoutTypes.carousel
        reply.attachments.append(self.create_hero_card1_1())
        reply.attachments.append(self.create_hero_card1_2())
        reply.attachments.append(self.create_hero_card1_3())
        reply.attachments.append(self.create_hero_card1_4())
        reply.attachments.append(self.create_hero_card1_5())
        reply.attachments.append(self.create_hero_card1_6())
        reply.attachments.append(self.create_hero_card1_7())
        reply.attachments.append(self.create_hero_card1_8())
        reply.attachments.append(self.create_hero_card1_9())
        reply.attachments.append(self.create_hero_card1_10())
        return await waterfall_step.context.send_activity(reply)
     




    async def NegativeMoodCarousel(self,waterfall_step:WaterfallStepContext):
        name = waterfall_step._turn_context.activity.text
        waterfall_step.values["first_click"] = name
        waterfall_step.values["first_clicktime"] = waterfall_step._turn_context.activity.timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")


        reply = MessageFactory.list([])
        reply.attachment_layout = AttachmentLayoutTypes.carousel

        if name == "feelings":
            reply.attachments.append(self.create_hero_card2_feelings_1())
            reply.attachments.append(self.create_hero_card2_feelings_2())
            reply.attachments.append(self.create_hero_card2_feelings_3())
            reply.attachments.append(self.create_hero_card2_feelings_4())
        elif name == "life":
            reply.attachments.append(self.create_hero_card2_life_1())
            reply.attachments.append(self.create_hero_card2_life_2())
            reply.attachments.append(self.create_hero_card2_life_3())
            reply.attachments.append(self.create_hero_card2_life_4())
        elif name == "job":
            reply.attachments.append(self.create_hero_card2_job_1())
            reply.attachments.append(self.create_hero_card2_job_2())
            reply.attachments.append(self.create_hero_card2_job_3())
            reply.attachments.append(self.create_hero_card2_job_4())
        elif name == "friends":
            reply.attachments.append(self.create_hero_card2_friends_1())
            reply.attachments.append(self.create_hero_card2_friends_2())
            reply.attachments.append(self.create_hero_card2_friends_3())
            reply.attachments.append(self.create_hero_card2_friends_4())
        elif name == "health":
            reply.attachments.append(self.create_hero_card2_health_1())
            reply.attachments.append(self.create_hero_card2_health_2())
            reply.attachments.append(self.create_hero_card2_health_3())
            reply.attachments.append(self.create_hero_card2_health_4())
        elif name == "family":
            reply.attachments.append(self.create_hero_card2_family_1())
            reply.attachments.append(self.create_hero_card2_family_2())
            reply.attachments.append(self.create_hero_card2_family_3())
            reply.attachments.append(self.create_hero_card2_family_4())
        elif name == "spouse":
            reply.attachments.append(self.create_hero_card2_spouse_1())
            reply.attachments.append(self.create_hero_card2_spouse_2())
            reply.attachments.append(self.create_hero_card2_spouse_3())
            reply.attachments.append(self.create_hero_card2_spouse_4())
        elif name == "love":
            reply.attachments.append(self.create_hero_card2_love_1())
            reply.attachments.append(self.create_hero_card2_love_2())
            reply.attachments.append(self.create_hero_card2_love_3())
            reply.attachments.append(self.create_hero_card2_love_4())
        elif name == "self":
            reply.attachments.append(self.create_hero_card2_self_1())
            reply.attachments.append(self.create_hero_card2_self_2())
            reply.attachments.append(self.create_hero_card2_self_3())
            reply.attachments.append(self.create_hero_card2_self_4())
        elif name == "home":
            reply.attachments.append(self.create_hero_card2_home_1())
            reply.attachments.append(self.create_hero_card2_home_2())
            reply.attachments.append(self.create_hero_card2_home_3())
            reply.attachments.append(self.create_hero_card2_home_4())

        return await waterfall_step.context.send_activity(reply)       

    

        
    async def Completed(self,waterfall_step:WaterfallStepContext):
        second_click_name = waterfall_step._turn_context.activity.text

        waterfall_step.values["second_click"] = second_click_name
        waterfall_step.values["second_clicktime"] = waterfall_step._turn_context.activity.timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")

        first_click = waterfall_step.values["first_click"]
        second_click = waterfall_step.values["second_click"]
        first_clicktime = waterfall_step.values["first_clicktime"]
        second_clicktime = waterfall_step.values["second_clicktime"]
        dif = datetime.strptime(second_clicktime, "%d-%b-%Y (%H:%M:%S.%f)") - datetime.strptime(first_clicktime, "%d-%b-%Y (%H:%M:%S.%f)")
        current_time = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        name = waterfall_step.values["username"]
        user = name + "_" + current_time

        # Store into CosmosDB
        storeitem = await self.cosmodb.read([user])
        if user not in storeitem:
            usermode = UserProfile()
        else:
            usermode = storeitem[user]
        usermode.name = waterfall_step.values["username"] 
        usermode.first = first_click
        usermode.second = second_click
        usermode.firsttime = first_clicktime
        usermode.secondtime = second_clicktime
        usermode.clickdiff = int(dif.total_seconds())
        collectionStore = {user: usermode}
        await self.cosmodb.write(collectionStore)

        if int(dif.total_seconds()) < 10:
            reply = MessageFactory.attachment(self.create_animation_card_breathe())
            return await waterfall_step.context.send_activity(reply)
        else: 
            reply = MessageFactory.attachment(self.create_animation_card_hanginthere())
            return await waterfall_step.context.send_activity(reply)
            return await waterfall_step.end_dialog()

      



    async def on_turn(self,turn_context:TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if(dialog_context.active_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog("main_dialog")
        
        await self.con_statea.save_changes(turn_context)
    
# Email if triggered
    def send_mail(self, turn_context:WaterfallStepContext):
        with smtplib.SMTP('smtp', 587) as server:
            #context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            #server.ehlo()
            server.starttls()
            #server.ehlo()
            server.login("", "")
            message = "Please reach out urgently to " + waterfall_step.values["username"]
            server.sendmail("", "", message)
        return




#############################
# Create Mood Carousel Cards
#############################

    def create_hero_card1_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/love-600w-127647092.jpg")],
      buttons=[CardAction(title="love", type=ActionTypes.im_back, value="love")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card1_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/young-plant-growing-sunlight-600w-609086588.jpg"
               )
      ],
      buttons=[CardAction(title="life", type=ActionTypes.im_back, value="life")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_3(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/business-career-placement-concept-successful-600w-1111032854.jpg"
               )
      ],
      buttons=[CardAction(title="job", type=ActionTypes.im_back, value="job")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_4(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/group-friends-standing-by-car-600w-275521547.jpg"
               )
      ],
      buttons=[CardAction(title="friends", type=ActionTypes.im_back, value="friends")])
      return CardFactory.hero_card(herocard2)
    
    def create_hero_card1_5(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-vector/medical-heart-cartoon-drawing-vector-600w-1726653772.jpg"
               )
      ],
      buttons=[CardAction(title="health", type=ActionTypes.im_back, value="health")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_6(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/young-family-children-having-fun-600w-592802372.jpg"
               )
      ],
      buttons=[CardAction(title="family", type=ActionTypes.im_back, value="family")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_7(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/close-photo-cheerful-excited-glad-600w-789414166.jpg"
               )
      ],
      buttons=[CardAction(title="spouse", type=ActionTypes.im_back, value="spouse")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_8(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-vector/emoticons-set-emoji-faces-emoticon-600w-1556226521.jpg"
               )
      ],
      buttons=[CardAction(title="feelings", type=ActionTypes.im_back, value="feelings")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_9(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/z/stock-photo-self-healing-heart-chakra-meditation-woman-sitting-in-a-lotus-position-with-right-hand-on-heart-1510165223.jpg"
               )
      ],
      buttons=[CardAction(title="self", type=ActionTypes.im_back, value="self")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card1_10(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-vector/home-icon-600w-656554627.jpg"
               )
      ],
      buttons=[CardAction(title="home", type=ActionTypes.im_back, value="home")])
      return CardFactory.hero_card(herocard2)


#############################################
# Create Feelings NegativeMoodCarousel Cards
#############################################
    def create_hero_card2_feelings_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/family-laying-flowers-on-grave-600w-1230694315.jpg")],
      buttons=[CardAction(title="grief", type=ActionTypes.im_back, value="grief")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_feelings_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://img.etimg.com/photo/msid-72036663,quality-100/toes-numb1_istock.jpg"
               )
      ],
      buttons=[CardAction(title="numb", type=ActionTypes.im_back, value="numb")])
      return CardFactory.hero_card(herocard2)


    def create_hero_card2_feelings_3(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/angry-man-driving-vehicle-600w-1039040590.jpg"
               )
      ],
      buttons=[CardAction(title="rage", type=ActionTypes.im_back, value="rage")])
      return CardFactory.hero_card(herocard2)


    def create_hero_card2_feelings_4(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/depressed-business-woman-600w-310940801.jpg"
               )
      ],
      buttons=[CardAction(title="overwhelmed", type=ActionTypes.im_back, value="overwhelmed")])
      return CardFactory.hero_card(herocard2)



#############################################
# Create Life NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_life_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/cute-man-screams-covering-his-600w-1171526140.jpg")],
      buttons=[CardAction(title="intolerable", type=ActionTypes.im_back, value="intolerable")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_life_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://i2-prod.coventrytelegraph.net/incoming/article15284490.ece/ALTERNATES/s1200b/3_Remains-of-person.jpg"
               )
      ],
      buttons=[CardAction(title="death", type=ActionTypes.im_back, value="death")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_life_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/z/stock-photo-self-healing-heart-chakra-meditation-woman-sitting-in-a-lotus-position-with-right-hand-on-heart-1510165223.jpg")],
      buttons=[CardAction(title="me", type=ActionTypes.im_back, value="me")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_life_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="http://psychology.iresearchnet.com/wp-content/uploads/2016/01/Suicide.jpg")],
      buttons=[CardAction(title="suicide", type=ActionTypes.im_back, value="suicide")])
      return CardFactory.hero_card(herocard1)

#############################################
# Create Job NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_job_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/businessman-has-brown-cardboard-box-600w-1487870660.jpg")],
      buttons=[CardAction(title="unemployment", type=ActionTypes.im_back, value="unemployment")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_job_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://i2-prod.coventrytelegraph.net/incoming/article15284490.ece/ALTERNATES/s1200b/3_Remains-of-person.jpg"
               )
      ],
      buttons=[CardAction(title="everything", type=ActionTypes.im_back, value="everything")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_job_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/z/stock-photo-self-healing-heart-chakra-meditation-woman-sitting-in-a-lotus-position-with-right-hand-on-heart-1510165223.jpg")],
      buttons=[CardAction(title="me", type=ActionTypes.im_back, value="me")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_job_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="http://psychology.iresearchnet.com/wp-content/uploads/2016/01/Suicide.jpg")],
      buttons=[CardAction(title="suicide", type=ActionTypes.im_back, value="suicide")])
      return CardFactory.hero_card(herocard1)


#############################################
# Create Friends NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_friends_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/family-laying-flowers-on-grave-600w-1230694315.jpg")],
      buttons=[CardAction(title="loss", type=ActionTypes.im_back, value="loss")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_friends_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/man-being-rejected-by-his-600w-247296826.jpg"
               )
      ],
      buttons=[CardAction(title="rejection", type=ActionTypes.im_back, value="rejection")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_friends_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/boy-student-getting-bullied-school-600w-676951951.jpg")],
      buttons=[CardAction(title="bullying", type=ActionTypes.im_back, value="bullying")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_friends_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="http://psychology.iresearchnet.com/wp-content/uploads/2016/01/Suicide.jpg")],
      buttons=[CardAction(title="stigma", type=ActionTypes.im_back, value="stigma")])
      return CardFactory.hero_card(herocard1)




#############################################
# Create Health NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_health_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/hospital-sick-male-patient-sleeps-600w-1190997985.jpg")],
      buttons=[CardAction(title="illness", type=ActionTypes.im_back, value="illness")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_health_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/asian-men-drug-addicts-inject-600w-1170996361.jpg"
               )
      ],
      buttons=[CardAction(title="drugs", type=ActionTypes.im_back, value="drugs")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_health_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/silhouette-anonymous-alcoholic-person-drinking-600w-284143052.jpg")],
      buttons=[CardAction(title="alcohol", type=ActionTypes.im_back, value="alcohol")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_health_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="http://psychology.iresearchnet.com/wp-content/uploads/2016/01/Suicide.jpg")],
      buttons=[CardAction(title="anxiety", type=ActionTypes.im_back, value="anxiety")])
      return CardFactory.hero_card(herocard1)


#############################################
# Create Family NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_family_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-illustration/empty-white-box-open-doors-600w-1803238906.jpg")],
      buttons=[CardAction(title="nothing", type=ActionTypes.im_back, value="nothing")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_family_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/asian-men-drug-addicts-inject-600w-1170996361.jpg"
               )
      ],
      buttons=[CardAction(title="never", type=ActionTypes.im_back, value="never")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_family_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/man-carries-stack-big-rocks-600w-1362736310.jpg")],
      buttons=[CardAction(title="burden", type=ActionTypes.im_back, value="burden")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_family_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://wp-media.patheos.com/blogs/sites/658/2018/02/Ilchi-Lee_I-dont-care_20180220.jpg")],
      buttons=[CardAction(title="dontcare", type=ActionTypes.im_back, value="dontcare")])
      return CardFactory.hero_card(herocard1)

#############################################
# Create Spouse NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_spouse_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/divorce-decree-form-ring-600w-570636967.jpg")],
      buttons=[CardAction(title="divorce", type=ActionTypes.im_back, value="divorce")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_spouse_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/asian-men-drug-addicts-inject-600w-1170996361.jpg"
               )
      ],
      buttons=[CardAction(title="distrust", type=ActionTypes.im_back, value="distrust")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_spouse_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-illustration/empty-white-box-open-doors-600w-1803238906.jpg")],
      buttons=[CardAction(title="nothing", type=ActionTypes.im_back, value="nothing")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_spouse_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://wp-media.patheos.com/blogs/sites/658/2018/02/Ilchi-Lee_I-dont-care_20180220.jpg")],
      buttons=[CardAction(title="dontcare", type=ActionTypes.im_back, value="dontcare")])
      return CardFactory.hero_card(herocard1)

#############################################
# Create Love NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_love_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/divorce-decree-form-ring-600w-570636967.jpg")],
      buttons=[CardAction(title="never", type=ActionTypes.im_back, value="never")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_love_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://image.shutterstock.com/image-photo/asian-men-drug-addicts-inject-600w-1170996361.jpg"
               )
      ],
      buttons=[CardAction(title="distrust", type=ActionTypes.im_back, value="distrust")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_love_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-illustration/empty-white-box-open-doors-600w-1803238906.jpg")],
      buttons=[CardAction(title="nothing", type=ActionTypes.im_back, value="nothing")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_love_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/man-being-rejected-by-his-600w-247296826.jpg")],
      buttons=[CardAction(title="rejection", type=ActionTypes.im_back, value="rejection")])
      return CardFactory.hero_card(herocard1)

#############################################
# Create Self NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_self_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://www.aconsciousrethink.com/wp-content/uploads/2017/10/self-loathing-702x336.jpg")],
      buttons=[CardAction(title="loathing", type=ActionTypes.im_back, value="loathing")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_self_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://wp-media.patheos.com/blogs/sites/658/2018/02/Ilchi-Lee_I-dont-care_20180220.jpg"
               )
      ],
      buttons=[CardAction(title="dontcare", type=ActionTypes.im_back, value="dontcare")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_self_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://media2.fdncms.com/tucsonweekly/imager/u/zoom/6031074/5134c2c0_jesse_-_womens_sdcopy.jpg")],
      buttons=[CardAction(title="trauma/assault", type=ActionTypes.im_back, value="trauma/assault")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_self_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/man-carries-stack-big-rocks-600w-1362736310.jpg")],
      buttons=[CardAction(title="burden", type=ActionTypes.im_back, value="burden")])
      return CardFactory.hero_card(herocard1)



#############################################
# Create Home NegativeMoodCarousel Cards
#############################################

    def create_hero_card2_home_1(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/very-emotional-image-bearded-homeless-600w-194969381.jpg")],
      buttons=[CardAction(title="torment", type=ActionTypes.im_back, value="torment")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_home_2(self) -> Attachment:
      herocard2 = HeroCard(
      images=[
               CardImage(
                  url="https://wp-media.patheos.com/blogs/sites/658/2018/02/Ilchi-Lee_I-dont-care_20180220.jpg"
               )
      ],
      buttons=[CardAction(title="dontcare", type=ActionTypes.im_back, value="dontcare")])
      return CardFactory.hero_card(herocard2)

    def create_hero_card2_home_3(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://media2.fdncms.com/tucsonweekly/imager/u/zoom/6031074/5134c2c0_jesse_-_womens_sdcopy.jpg")],
      buttons=[CardAction(title="homeless", type=ActionTypes.im_back, value="homeless")])
      return CardFactory.hero_card(herocard1)

    def create_hero_card2_home_4(self) -> Attachment:
      herocard1 = HeroCard(
      images=[CardImage(url="https://image.shutterstock.com/image-photo/sad-handsome-man-thinking-over-600w-1255598947.jpg")],
      buttons=[CardAction(title="unsupportive", type=ActionTypes.im_back, value="unsupportive")])
      return CardFactory.hero_card(herocard1)




#################################
# Create Completion Cards
#################################      
    def create_animation_card_breathe(self) -> Attachment:
        card = AnimationCard( media=[MediaUrl(url="https://media.giphy.com/media/UW8VVu5c2OBUy43cos/giphy.gif")],
        title="Take Your Mind Off")
        return CardFactory.animation_card(card)
     
    def create_animation_card_hanginthere(self) -> Attachment:
        card = AnimationCard( media=[MediaUrl(url="https://media.giphy.com/media/W63ZJmQ4qdblTM9Wbi/giphy.gif")],
        title="Hang In There")
        return CardFactory.animation_card(card)
        
