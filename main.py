import os
import asyncio
import logging

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

from config import API_ID, API_HASH


async def display_sessions():
    sessions_folder = "sessions"
    
    session_files = os.listdir(sessions_folder)
    
    logging.info("Available sessions:")
    for i, session_file in enumerate(session_files):
        logging.info(f"{i+1}. {session_file}")
    
    selected_session = input("Select a session: ")
    
    await invite_users(selected_session)


async def invite_users(selected_session):
    group_name = input("Enter the group name: ")
    delay = int(input("Enter the delay in seconds: "))
    
    session_file_path = f"sessions/{selected_session}"
    
    with open("users.txt") as users_file:
        users = users_file.read().splitlines()
    
    logging.info(f"Inviting users to {group_name} with a delay of {delay} seconds...")
    
    async with TelegramClient(session_file_path, API_ID, API_HASH) as client:
        for user in users:
            logging.info(f"Inviting {user} to {group_name}...")
            try:
                await client(InviteToChannelRequest(group_name, [user]))
                logging.info(f"{user} invited successfully!")
            except Exception as e:
                logging.error(f"Failed to invite {user}: {str(e)}")
            
            await asyncio.sleep(delay)
    
    logging.info("Invitations sent successfully!")


logging.basicConfig(level=logging.INFO)
asyncio.run(display_sessions())
