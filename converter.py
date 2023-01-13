import os
import  random
import os.path

import logging
from typing import Tuple, Optional
import time, os, sys, json
import  csv
import asyncio
import datetime
import shutil

from threading import Thread
from tempfile import NamedTemporaryFile
#from telegram.ext.updater import Updater  
#from telegram.update import Update  
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup,InputMediaAudio
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler
)
import telegram.utils.helpers as helpers
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import TextClip,ColorClip,CompositeAudioClip,CompositeVideoClip,ImageClip,VideoClip
import pytube
from os import listdir, remove, path
import shutil
from threading import Thread 
import requests
from pytube import Search
from PIL import Image
import numpy


my_secret = '5972974320:AAHc6Qs9haTluZk1QvK3TUUHI_nRSUMeOIU'
Date=datetime.datetime.now()
loop = asyncio.get_event_loop()
NameError=[False]
Runforever=[True]
class TelegramBOT():
    def __init__(self) -> None:
        self.SentMessages ={}
    @staticmethod
    
    def MyMessageHandler(update: Update,context: CallbackContext)-> str:
            return Update.message    
    @staticmethod
              
    def MyCommandHandler(update: Update,context: CallbackContext)-> str:
        return Update.command
    
    def SetUpEnvironment(self,UserID) :
        if not os.path.isdir("Data/{}".format(UserID)):
            os.makedirs("Data/{}".format(UserID)) 
        try:
            f = open(f"Data/{UserID}/MusicDetail.json", 'w+')
            f.write(json.dumps([{}]))
            f.close()
        except IOError:
            f = open(f"Data/{UserID}/MusicDetail.json", 'w+')
            f.write(json.dumps([{}]))
            f.close()
        finally:
            self.SentMessages[str(UserID)]=[]    

    
    def start(self,update: Update, context: CallbackContext) -> int:
        self.SetUpEnvironment(update.message.from_user.id )                  
        update.effective_chat.send_message("💫 Welcome To Youtube Video Converter 💫",
        parse_mode=ParseMode.HTML,
        )
        time.sleep(2)
        self.search(update,context)  
    
    def restart(self,update: Update, context: CallbackContext) -> int:
        #print(update.message.from_user.id )                  
        update.effective_chat.send_message("You can always restart from the beginning!",
        parse_mode=ParseMode.HTML,
        )
        time.sleep(2)
        self.search(update,context)      
    
    def end(self,update: Update, context: CallbackContext) -> int:
        Runforever.clear() 
        Runforever.append(False)       
        update.message.delete(timeout=10000)
    
    def cancel(self,update: Update, context: CallbackContext) -> int:
        #print(update.message.from_user.id )                  
        update.effective_chat.send_message("Canceled!",
        parse_mode=ParseMode.HTML,
        )
        self.search(update,context,True)     
    
    def search(self,update: Update, context: CallbackContext,Return=None) -> int:
        if Return == None:        
            update.effective_chat.send_message("*Convert what you Love \n*",
            parse_mode=ParseMode.MARKDOWN_V2,
            )
            time.sleep(1)  
            update.effective_chat.send_message("*Search for:* \n`artists`, `songs` , `playlists`, `videos`, and `more`\n all you got to do is Type what you want to search in side the textbox and hit enter",
            parse_mode=ParseMode.MARKDOWN_V2,
            )
        else:
                update.effective_chat.send_message("*Search for:* \n`artists`, `songs` , `playlists`, `videos`, and `more`",
            parse_mode=ParseMode.MARKDOWN_V2,
            )  
    @staticmethod                
    
    def help(update: Update, context: CallbackContext) -> int:
        text="* Usage:* type `/search `\nthen hit enter finally enter keyword *Example:* \n1, `Michael buble home`\n2, `phone screen restoration `\n" \
            "\n*Search keyword:*  \n \- It can be either youtube link or keyword to a file that you wish to convert to mp3\n" \
                "\n \- will return the results with images select the one you like\n" \
            "\n*Make sure to not put multiple space between words for better result*\n"        
        update.effective_chat.send_message(text,
        parse_mode=ParseMode.MARKDOWN_V2,
        )  
    @staticmethod            
    
    def about(update: Update, context: CallbackContext) -> int:
                
        update.effective_chat.send_message("https://t.me/Abinet_tes",
        parse_mode=ParseMode.HTML,
        )
    @staticmethod
    def _ReadMusicDetails(Api_ID,Key=None,Conditional=False,Value=None):
        result=[]
        with open(f"Data/{Api_ID}/MusicDetail.json", "r") as file_json:
            data=json.load(file_json)
            for line in data:
                if Conditional==True:
                    if  line[Key]==Value:
                        return line
                else:        
                    result.append(line[Key])
        return result            
    
    def AllMessages(self,update: Update, context: CallbackContext,Return=None) -> int:
        
        if update.message==None:
            query = update.callback_query
            query.answer(timeout=6000,cache_time=6000)
            #print(query.message.reply_markup.inline_keyboard[0][0]["text"])
            # CallbackQueries need to be answered, even if no notification to the user is needed
            # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
            if query.answer():
                #print(update.callback_query.from_user.id)
                res=update.effective_chat.send_message(f"Converting {query.message.reply_markup.inline_keyboard[0][0]['text']} \nPlease wait... ",parse_mode=ParseMode.HTML,timeout=6000)
                self.SentMessages[str(update.callback_query.from_user.id)].append(res.message_id)
                Mp3=self.download_link(str(update.callback_query.from_user.id),query.data)
                
                
                update.effective_chat.send_audio(open(Mp3,"rb"),timeout=60000)
                for line in self.SentMessages[str(update.callback_query.from_user.id)]:
                    time.sleep(1)
                    try:
                        context.bot.delete_message(update.callback_query.from_user.id,line,60 )
                    except Exception as e:
                        pass   
                self.move_and_remove(str(update.callback_query.from_user.id))
                 
        else:
            
            try:
                try:
                    res=update.effective_chat.send_message("`{} 🤔🤔 ` \n 🔎 Looking for your video 🔍 \.\.\. ".format(update.message.text),parse_mode=ParseMode.MARKDOWN_V2,)
                
                    self.SentMessages[str(update.message.from_user.id)].append(res.message_id)
                except:
                    self.SentMessages[str(update.message.from_user.id)]=[]
                    self.SentMessages[str(update.message.from_user.id)].append(res.message_id)     
                Message=update.message.text
                if " " in Message.strip():
                    Message=Message.replace(" ","+").strip()
                if self._YoutubeData(Message,update.message.from_user.id)==False:
                    res=update.effective_chat.send_message("Invalid query Please Type \n`artists`, `songs` , `playlists` or `videos` Title",parse_mode=ParseMode.MARKDOWN_V2,)
                    self.SentMessages[str(update.message.from_user.id)].append(res.message_id)
                else:
                    #print(self.SentMessages[str(update.message.from_user.id)])
                    Data=self._ReadMusicDetails(str(update.message.from_user.id),"Image")
                    if Data[0]=={}:
                        res=update.effective_chat.send_message("*`Sorry*\n Something went wrong on our end \n Please Try again! \.\.\.",parse_mode=ParseMode.MARKDOWN_V2,)
                        self.SentMessages[str(update.message.from_user.id)].append(res.message_id) 
                    res=update.effective_chat.send_message("working on it ...",parse_mode=ParseMode.HTML,)
                    self.SentMessages[str(update.message.from_user.id)].append(res.message_id)
                    
                    for myimage in Data:
                        Mydata=self._ReadMusicDetails(str(update.message.from_user.id),"Image",Conditional=True,Value=myimage)
                        ##print(Mydata)
                        keyboard = [
                                [InlineKeyboardButton(myimage[:-4], callback_data=Mydata["Video_Url"])],
                            ]

                        reply_markup = InlineKeyboardMarkup(keyboard)

                        ##print(f"Data/{str(update.message.from_user.id)}/{myimage}")
                        res=update.effective_message.chat.send_photo(photo=open(f"Data/{str(update.message.from_user.id)}/{myimage}",'rb'),reply_markup=reply_markup,timeout=60000,
                        
                )       
                        
                        self.SentMessages[str(update.message.from_user.id)].append(res.message_id)
                    res=update.effective_chat.send_message("Please \n`Select Your Video By clicking on the Video's Title below the images`",parse_mode=ParseMode.MARKDOWN_V2,)
                    self.SentMessages[str(update.message.from_user.id)].append(res.message_id)
            except Exception as e:
                ##print("this error"+e)
                res=update.effective_chat.send_message("Please Type \n`artists`, `songs` , `playlists` or `videos` Title",
            parse_mode=ParseMode.MARKDOWN_V2,
            ) 
                self.SentMessages[str(update.message.from_user.id)].append(res.message_id)    
    
    def read_fronzoli(self):

        with open("fronzoli.dat", "r") as file:
            for line in file:
                if line.split("=")[0] == "EXE_DIR":
                    exe_dir = line.split("=")[1][:-1]
                elif line.split("=")[0] == "OUTPUT_DIR":
                    output_dir = line.split("=")[1]
        try:
            print(exe_dir)
            print(output_dir)
        except UnboundLocalError:
            pass


           
    
    def download_link(self,ApiID,url):
            """Download pasted link"""

            Out_dir=f"Data/{ApiID}"
            #mp4_only="The Weeknd - Save Your Tears (Official Music Video).mp4"
            # Download Video
            mp4_only = self.download_video(url,Out_dir)
            # Convert to Mp3
            Mymp3=self.convert_to_mp3(mp4_only,ApiID)
            #print(Mymp3)
            return Out_dir+"/"+Mymp3
            # Remove downloades video and move in the music directory
            
    
    
    def download_video(self, url,output_dir):
        
        video = pytube.YouTube(url)
        stream = video.streams.get_lowest_resolution()
        filename=self.validatefilename(stream.title)
        
        stream.download(output_path=output_dir,filename=filename+".mp4")
        
        return filename+".mp4"
        
    @staticmethod
    
    def convert_to_mp3(filename,Api_ID=None):
        path=""
        if Api_ID==None:
            pass
        else:
            path="/".join(["Data",str(Api_ID)])
        #print(f"this is my {path}/{filename}")    
        clip = VideoFileClip(f"{path}/{filename}")
        clip = clip.resize(0.2)
        clip.audio.write_audiofile("{}/{}.mp3".format(path, filename[:-4]))
        clip.close()
        return filename[:-4]+".mp3"
   
    def WriteMusicDetails(self,Api_ID,details):
        path = "Data"
        if Api_ID==None:
            pass
        else:
            path="/".join(["Data",str(Api_ID)])
        try:
            #print("this is:"+path)
            
            
            with open(f"{path}/MusicDetail.json","w+") as f:
                json.dump(details, f,indent=4)
        except FileNotFoundError:
           
                self.SetUpEnvironment(Api_ID)
                self.WriteMusicDetails(Api_ID,details)   
   
    def downloadImages(self,img_url, filename,Api_ID=None):
        try:
            response=requests.get(img_url, stream = True)
            path="Data"
            if Api_ID==None:
                pass
            else:
                path="/".join(["Data",str(Api_ID)])
            #print(path)    
            if response.status_code:
                img=Image.open(response.raw)
                img=img.resize(size=[1920,1080])
                numpydata = numpy.array(img)
                img=ImageClip(numpydata)
                height=img.size[0]
                text_clip = TextClip(txt=filename.upper(),
                            size=(.8*img.size[0], 0),
                            font="P052-Bold",
                            color="#E0E0E0")
                text_clip = text_clip.set_position('center')
                im_width, im_height = text_clip.size
                color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)),
                                    color=(0, 25, 51))
                color_clip = color_clip.set_opacity(.4)         
                text_clip = text_clip.set_position('center')
                clip_to_overlay = CompositeVideoClip([color_clip, text_clip])
                clip_to_overlay = clip_to_overlay.set_position('center')
                final_clip = CompositeVideoClip([img, clip_to_overlay])
                
                asyncio.wait(final_clip.save_frame(f'{path}/{filename}.png'))
                return True
        except Exception as e:
            if "does not exist" in e:
                self.SetUpEnvironment(Api_ID)
                self.downloadImages(img_url, filename,Api_ID)
            #print(e)
            return False
            #img.save(f'{path}/Img/{filename}.jpg')
    @staticmethod
    def validatefilename(filename):
        validater=["|","*","?","\"" ] 
        for valid in validater:
            if valid in filename:
                filename=filename.replace(valid,"").strip() 
        return filename             
    
    def _YoutubeData(self,query,Api_ID):
        try:
            #print(query)      
            s = Search(query)
            counters =1
            MyMusics=[]
           
            for video in s.results:
                counters+=1
                if counters <=5:
                    try:
                        filename=self.validatefilename(video.title)
                        print (filename)
                        
                        if self.downloadImages(video.thumbnail_url,filename,Api_ID) ==True:
                            MyMusics.append({"Title":filename,"Image":filename+".png","Video_Url":video.watch_url,"embed_html":video.embed_html})
                        else:
                            counters-=1
                    except:
                        pass                
                else:
                    break    
                    
            self.WriteMusicDetails(Api_ID,MyMusics)
            return True 
        except Exception as e:
            #print("this"+e)
            return False 
    @staticmethod
                     
    def move_and_remove(Api_ID=None,Format=None):
        """https://www.youtube.com/watch?v=aDL7dwpKOuw"""
        #path=os.path.dirname(__file__)
        path="Data"
        if Api_ID==None:
            pass
        else:
            path="/".join(["Data",Api_ID])
    
        if Format == None:
            # for file in listdir(fr"{exe_dir}"):
            #     if file.endswith(".mp3"):
            #         shutil.copy(src=file,dst=output_dir,follow_symlinks=True)
            for file in listdir(path):
                if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".mp3") or file.endswith(".png"):
                    remove("/".join([path,file]))
        else:
                # for file in listdir('/'.join([path,Format])):
                #     if file.endswith(".mp3"):
                #         shutil.copy(src=file,dst=output_dir,follow_symlinks=True)
                for file in listdir('/'.join([path,Format])):
                    if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".mp3") or file.endswith(".png"):
                        remove("/".join([path,Format,file]))        






while Runforever[0]==True:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    logger = logging.getLogger(__name__)
# 
# 
# def start(update, context):
#     update.effective_chat.send_message("Hello! Please send me a Google Drive Shareable Link to Clone to your Drive!" \
#         "\nSend /help for checking all available commands.",
#     parse_mode=ParseMode.HTML,
#         )
#     # ;-;

# 
# 
# def helper(update, context):
#     update.effective_chat.send_message("Here are the available commands of the bot\n\n" \
#         "*Usage:* `/clone <link> [DESTINATION_ID]`\n*Example:* \n1. `/clone https://drive.google.com/drive/u/1/folders/0AO-ISIXXXXXXXXXXXX`\n2. `/clone 0AO-ISIXXXXXXXXXXXX`" \
#             "\n*DESTIONATION_ID* is optional. It can be either link or ID to where you wish to store a particular clone." \
#             "\n\nYou can also *ignore folders* from clone process by doing the following:\n" \
#                 "`/clone <FOLDER_ID> [DESTINATION] [id1,id2,id3]`\n In this example: id1, id2 and id3 would get ignored from cloning\nDo not use <> or [] in actual message." \
#                     "*Make sure to not put any space between commas (,).*\n" \
#                         , context.bot, update, 'Markdown')
    
    
    async def main() -> None:
        try:
            """Start the bot."""
            # Create the Updater and pass it your bot's token.
            updater = Updater(token=my_secret,use_context=True,workers=8)
            mytelegram=TelegramBOT()
            
            # Get the dispatcher to register handlers
            dispatcher = updater.dispatcher
            dispatcher.add_handler(CommandHandler("start",  mytelegram.start,run_async=True))
            dispatcher.add_handler(CommandHandler("restart", mytelegram.restart,run_async=True))
            dispatcher.add_handler(CommandHandler('mystop', mytelegram.end,run_async=True))
            dispatcher.add_handler(CommandHandler("about", mytelegram.about,run_async=True))
            dispatcher.add_handler(CommandHandler('cancel', mytelegram.cancel,run_async=True))
            dispatcher.add_handler(CommandHandler("search", mytelegram.search,run_async=True))
            dispatcher.add_handler(CommandHandler('help', mytelegram.help,run_async=True))
            dispatcher.add_handler(MessageHandler(Filters.all,mytelegram.AllMessages,run_async=True))
            dispatcher.add_handler(CallbackQueryHandler( mytelegram.AllMessages,run_async=True))
            # Start the Bot
            # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
            # To reset this, simply pass `allowed_updates=[]`
            updater.start_polling(poll_interval= 5, timeout = 600000,allowed_updates=Update.ALL_TYPES)
            # Run the bot until pressed Ctrl-C or the process receives SIGINT,
            # SIGTERM or SIGABRT. This should be used most of the time, since
            # start_polling() is non-blocking and will stop the bot gracefully.
            updater.idle()
            #print("listening")
        except:
            pass    
    
    if __name__ == "__main__":
            loop.run_until_complete(main())
