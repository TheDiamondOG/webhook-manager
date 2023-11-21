import requests
import os

def clear():
    os.system("clear")

def pause():
    input("Enter to continue\n")

def start():
    clear()
    global web_url
    with open("webhook", "r") as web_url_file:
        web_url = web_url_file.read()
    if web_url.startswith("https://discord.com/api/webhooks"):
        web_checker(web_url)
        webhook_manager()
    else:
        print("What is your webhook url")
        print("It needs to inclue the webhook token")
        web_url = input("URL: ")
        web_checker(web_url)
        print("Do you want it saved?")
        saved = input("Save: ")
        if saved == "yes":
            with open("webhook", "w+") as web_url_file:
                web_url_file.write(web_url)
        webhook_manager()

def web_checker(webhook_url):
    response = requests.get(web_url)
    if response.status_code == 404:
        print("The webhook is not a valid link or does not include webhook token")
        pause()
        start()
    else:
        pass

def webhook_manager():
    clear()
    print("------------Webhook Manager------------")
    print("0. Exit")
    print("1. Send Message")
    print("2. Send Message (Embed)")
    print("3. Edit Webhook Message")
    print("4. Edit Webhook Message (Embed)")
    print("5. Delete Webhook Message")
    print("6. Get Webhook Message")
    print("7. Get Webhook Info")
    print("8. Get Owner Info")
    print("9. Edit Webhook")
    print("10. Delete Webhook")
    option_hand(input("Option: "))

def option_hand(option):
    clear()
    if option == "0":
        exit()
    elif option == "1":
        send_message()
    elif option == "2":
        send_message_embed()
    elif option == "3":
        edit_message()
    elif option == "4":
        edit_embed_message()
    elif option == "5":
        delete_message()
    elif option == "6":
        get_message()
    elif option == "7":
        get_bot_info()
    elif option == "8":
        get_owner_info()
    elif option == "9":
        edit_webhook()
    elif option == "10":
        delete_webhook()

    else:
        print(f"{option} is not a real option")
        pause()


def send_message():
    message = input("Message: ")
    data = {
        "content": message,
      }

    response = requests.post(web_url, json=data)
    if response.status_code == 204:
        print("Sent the Message")
    else:

        print(f"There was an error when sending the message. \nError Code: {response.status_code}")
        print(response.text)
    pause()

def send_message_embed():
    title = input("Embed Title: ")
    clear
    description = input("Embed Description: ")
    clear()
    print("Needs to be a decimal color")
    color = int(input("Color: "))
    clear()
    print("This is not needed but here if you want it.")
    print("Enter if you don't have one")
    image = input("Image URL: ")

    if image == "":
        data = {
            "embeds": [
                {
                    "title": title,
                    "color": color,
                    "description": description,
                }
            ]
        }

    else:
        data = {
            "embeds": [
                {
                    "title": title,
                    "color": color,
                    "description": description,
                    "image": {"url": image}
                }
            ]
        }

    clear()
    response = requests.post(web_url, json=data)
    if response.status_code == 204:
        print("Sent the Message")
    else:

        print(f"There was an error when sending the message. \nError Code: {response.status_code}")
        print(response.text)
    pause()

def delete_webhook():
    print("Are you sure you want to delete this webhook?")
    mas = input("yes/no")
    if mas == "yes":
        print("Deleting Webhook")
        response = requests.delete(web_url)
        clear()
        if response.status_code == 204:
            print("Deleted the Webhook")
            pause()
            with open("webhook", "w+") as web_url_file:
                web_url_file.write("")
            start()
        else:
            print(f"There was an error when deleting the webhook. \nError Code: {response.status_code}")
            print(response.text)
            pause()
    else:
        print("Webhook has not been deleted")
        pause

def get_bot_info():
    print("Getting Info")
    response = requests.get(web_url)
    if response.status_code == 200:
        pass
    else:
        print(f"There was an error getting the info. \nError Code: {response.status_code}")
        print(response.text)
        pause()
        webhook_manager()

    webinf = response.json()
    clear()
    if webinf['type'] == 1:
        print("Webhook Name", webinf['name'])
        print("Webhook ID", webinf['id'])
        print("Bot Type: Incoming")
        print("Token:", webinf['token'])
        print("Server ID:", webinf['guild_id'])
        print("Channel ID:", webinf['channel_id'])
    elif webinf['type'] == 2:
        print("Webhook Name", webinf['name'])
        print("Webhook ID", webinf['id'])
        print("Bot Type: Channel Follower")
        print("Token:", webinf['token'])
        print("Server ID", webinf['guild_id'])
        print("Channel ID:", webinf['channel_id'])
        print("Source Channel Name:", webinf['source_channel']['name'])
        print("Source Channel ID:", webinf['source_channel']['id'])
    elif webinf['type'] == 3:
        print("Webhook Name:", webinf['name'])
        print("Webhook ID:", webinf['id'])
        print("Bot Type: Application")
        print("Application ID:", webinf['application_id'])
    pause()


def get_owner_info():
    print("Getting Info")
    response = requests.get(web_url)
    if response.status_code == 200:
        pass
    else:
        print(f"There was an error getting the info. \nError Code: {response.status_code}")
        print(response.text)
        pause()
        webhook_manager()

    webinf = response.json()
    clear()
    if webinf['type'] == 1:
        print("Owner Display Name:", webinf['user']['global_name'])
        print("Owner Username:", webinf['user']['username'])
        print("Owner ID:", webinf['user']['id'])
        print("Owner Discriminator:", webinf['user']['discriminator'])
        print("Owner Public Flags:", webinf['user']['public_flags'])
        print("Owner Banner Color:", webinf['user']['banner_color'])
    elif webinf['type'] == 3:
        print("You can not get owner info with a type 3 webhook AKA an application webhook")
    pause()

def edit_message():
    message_id = input("Message ID: ")
    nmessage = input("New Message: ")
    data = {
        "content":nmessage
        }
    response = requests.patch(f"{web_url}/messages/{message_id}", json=data)
    clear()
    if response.status_code == 200:
        print("Edited the Message")
    else:
        print(f"There was an error when editing the message. \nError Code: {response.status_code}")
        print(response.text)
    pause()

def edit_embed_message():
    message_id = input("Message ID: ")
    title = input("Embed Title: ")
    clear
    description = input("Embed Description: ")
    clear()
    print("Needs to be a decimal color")
    print("Link to the website I use for this\nhttps://bit.ly/47bYrp7")
    color = int(input("Color: "))
    clear()
    print("This is not needed but here if you want it.")
    print("Enter if you don't have one")
    image = input("Image URL: ")

    if image == "":
        data = {
            "embeds": [
                {
                    "title": title,
                    "color": color,
                    "description": description,
                }
            ]
        }

    else:
        data = {
            "embeds": [
                {
                    "title": title,
                    "color": color,
                    "description": description,
                    "image": {"url": image}
                }
            ]
        }

    clear()
    response = requests.patch(f"{web_url}/messages/{message_id}", json=data)
    if response.status_code == 200:
        print("Edited the Message")
    else:
        print(f"There was an error when editing the message. \nError Code: {response.status_code}")
        print(response.text)
    pause()

def delete_message():
    message_id = input("Message ID: ")
    response = requests.delete(f"{web_url}/messages/{message_id}")
    clear()
    if response.status_code == 204:
        print("Deleted the Message")
    else:
        print(f"There was an error when deleting the message. \nError Code: {response.status_code}")
        print(response.text)
    pause()

def edit_webhook():
    print("Press enter if you do not want to change that part")
    nname = input("New Name: ")
    if nname == "":
        nname = None
    clear()
    print("Press enter if you do not want to change that part")
    print("This is an image URL")
    navatar = input("New Avatar: ")
    if navatar == "":
        navatar = None
    clear()
    print("Press enter if you do not want to change that part")
    print("This needs a channel id")
    nchannel = input("New Channel: ")
    if nchannel == "":
        nchannel = None
    clear()
    data = {
        "name":nname,
        "avarar":navatar,
        "channel_id":nchannel
        }
    response = requests.patch(f"{web_url}", json=data)
    clear()
    if response.status_code == 200:
        print("Edited the webhook")
    else:
        print(f"There was an error when editing the webhook. \nError Code: {response.status_code}")
        print(response.text)
    pause()

def get_message():
    message_id = input("Message ID: ")
    response = requests.get(f"{web_url}/messages/{message_id}")
    clear()
    messj = response.json()
    if response.status_code == 200:
        print(f"Webhook Sent:", messj['author']['username'], ":", messj['content'],)
    else:
        print(f"There was an error when getting the message. \nError Code: {response.status_code}")
        print(response.text)
    pause()

start()

while True:
    webhook_manager()
