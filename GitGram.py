#!/usr/bin/env python3

from logging import basicConfig, getLogger, INFO
from flask import Flask, request, jsonify
from html import escape
from requests import get, post
from os import environ
import config

from telegram.ext import CommandHandler, Updater

server = Flask(__name__)

basicConfig(level=INFO)
log = getLogger()

ENV = bool(environ.get('ENV', False))

if ENV:
    BOT_TOKEN = environ.get('BOT_TOKEN', None)
    PROJECT_NAME = environ.get('PROJECT_NAME', None)
    ip_addr = environ.get('APP_URL', None)
    # If you kanged our project without owner's permission, we will get you DMCA'd.
    GIT_REPO_URL = environ.get('GIT_REPO_URL', "https://github.com/DYNANETWORK/GITGRAMBOT")
else:
    BOT_TOKEN = config.BOT_TOKEN
    PROJECT_NAME = config.PROJECT_NAME
    ip_addr = get('https://api.ipify.org').text
    GIT_REPO_URL = config.GIT_REPO_URL

updater = Updater(token=BOT_TOKEN, workers=1)
dispatcher = updater.dispatcher

print("If you need more help from Me, Join @cute_friendx in Telegram.")


def start(_bot, update):
    """/start message for bot"""
    message = update.effective_message
    message.reply_text(
        f"🎀  ᴛʜɪ𝓈 ɪ𝓈 ᴛʜᴇ ᴇᴠᴇɴᴛ𝓈 ᴡᴀᴛᴄʜᴇʀ ʙᴏᴛ ꜰᴏʀ  🎀 {PROJECT_NAME}. ✧｡  🎀  ɪ ᴊᴜ𝓈ᴛ ɴᴏᴛɪꜰʏ ᴏᴡɴᴇʀ𝓈 ᴀʙᴏᴜᴛ ᴡʜᴀᴛ ɪ𝓈 ʜᴀᴘᴘᴇɴɪɴɢ ᴏɴ ᴛʜᴇɪʀ ɢɪᴛʜᴜʙ ʀᴇᴘᴏ𝓈ɪᴛᴏʀɪᴇ𝓈 ᴛʜʀᴏᴜɢʜ ᴡᴇʙʜᴏᴏᴋ𝓈.\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ  🎀  ｡✧[∂єρℓσу](https://github.com/DYNANETWORK/GITGRAMBOT) ✴  🎀  ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ᴏʀ ᴜ𝓈ᴇ /help ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ​ ᴜ𝓈ᴇ ᴛʜɪ𝓈 ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ𝓈​  🎀  ✴.",
        parse_mode="markdown")


def help(_bot, update):
    """/help message for bot"""
    message = update.effective_message
    message.reply_text(
        f"*ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs​*\n\n`/connect` - sᴇᴛᴜᴘ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛʜɪs ᴄʜᴀᴛ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ɢɪᴛʜᴜʙ ᴀᴄᴛɪᴠɪᴛʏ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴs.\n`/support` - ɢᴇᴛ ʟɪɴᴋ ᴛᴏ ɢᴇᴛ sᴜᴘᴘᴏʀᴛ ꜰᴏʀ ʏᴏᴜ ɪꜰ ʏᴏᴜ sᴛᴜᴄᴋ.\n`/source` - ɢᴇᴛ ᴛʜᴇ ɢɪᴛʜᴜʙ ʀᴇᴘᴏsɪᴛᴏʀʏ ᴜʀʟ.",
        parse_mode="markdown"
    )


def support(_bot, update):
    """Links to Support"""
    message = update.effective_message
    message.reply_text(
        f"*ɢᴇᴛᴛɪɴɢ sᴜᴘᴘᴏʀᴛ*\n\nꜰᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴘ ɪɴ ᴜsɪɴɢ ᴍᴇ, ᴊᴏɪɴ [ѕυρρσят](https://t.me/cute_friendx).",
        disable_web_page_preview=True,
        parse_mode="markdown"
    )


def source(_bot, update):
    """Link to Source"""
    message = update.effective_message
    message.reply_text(
        f"*sᴏᴜʀᴄᴇ​*:\n[ʀᴇᴘᴏ​](https://github.com/DYNANETWORK/GITGRAMBOT).",
        disable_web_page_preview=True,
        parse_mode="markdown"
    )


def getSourceCodeLink(_bot, update):
    """Pulls link to the source code."""
    message = update.effective_message
    message.reply_text(
        f"{GIT_REPO_URL}"
    )


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
supportCmd = CommandHandler("support", support)
sourcecode = CommandHandler("source", source)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(supportCmd)
dispatcher.add_handler(sourcecode)
updater.start_polling()

TG_BOT_API = f'https://api.telegram.org/bot{BOT_TOKEN}/'
checkbot = get(TG_BOT_API + "getMe").json()
if not checkbot['ok']:
    log.error("[ERROR] Invalid Token!")
    exit(1)
else:
    username = checkbot['result']['username']
    log.info(
        f"[INFO] Logged in as @{username}, waiting for webhook requests...")


def post_tg(chat, message, parse_mode):
    """Send message to desired group"""
    response = post(
        TG_BOT_API + "sendMessage",
        params={
            "chat_id": chat,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True}).json()
    return response


def reply_tg(chat, message_id, message, parse_mode):
    """reply to message_id"""
    response = post(
        TG_BOT_API + "sendMessage",
        params={
            "chat_id": chat,
            "reply_to_message_id": message_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True}).json()
    return response


@server.route("/", methods=['GET'])
# Just send 'Hello, world!' to tell that our server is up.
def helloWorld():
    return 'Hello, world!'


@server.route("/<groupid>", methods=['GET', 'POST'])
def git_api(groupid):
    """Requests to api.github.com"""
    data = request.json
    if not data:
        return f"<b>ᴀᴅᴅ ᴛʜɪs ᴜʀʟ:</b> {ip_addr}/{groupid} ᴛᴏ ᴡᴇʙʜᴏᴏᴋs ᴏꜰ ᴛʜᴇ ɢɪᴛʜᴜʙ ᴘʀᴏᴊᴇᴄᴛ"

    if data.get('hook'):
        repo_url = data['repository']['html_url']
        repo_name = data['repository']['name']
        sender_url = data['sender']['html_url']
        sender_name = data['sender']['login']
        response = post_tg(
            groupid,
            f"😘 sᴜᴄᴄᴇssꜰᴜʟʟʏ sᴇᴛ ᴡᴇʙʜᴏᴏᴋ ꜰᴏʀ <a href='{repo_url}'>{repo_name}</a> ʙʏ <a href='{sender_url}'>{sender_name}</a>!",
            "html"
        )
        return response

    if data.get('commits'):
        commits_text = ""
        rng = len(data['commits'])
        if rng > 10:
            rng = 10
        for x in range(rng):
            commit = data['commits'][x]
            if len(escape(commit['message'])) > 300:
                commit_msg = escape(commit['message']).split("\n")[0]
            else:
                commit_msg = escape(commit['message'])
            commits_text += f"{commit_msg}\n<a href='{commit['url']}'>{commit['id'][:7]}</a> - {commit['author']['name']} {escape('<')}{commit['author']['email']}{escape('>')}\n\n"
            if len(commits_text) > 1000:
                text = f"""✨ <b>{escape(data['repository']['name'])}</b> - ɴᴇᴡ {len(data['commits'])} ᴄᴏᴍᴍɪᴛ ({escape(data['ref'].split('/')[-1])})
{commits_text}
"""
                response = post_tg(groupid, text, "html")
                commits_text = ""
        if not commits_text:
            return jsonify({"ok": True, "text": "Commits text is none"})
        text = f"""✨ <b>{escape(data['repository']['name'])}</b> - ɴᴇᴡ {len(data['commits'])} ᴄᴏᴍᴍɪᴛ ({escape(data['ref'].split('/')[-1])})
{commits_text}
"""
        if len(data['commits']) > 10:
            text += f"\n\n<i>And {len(data['commits']) - 10} other commits</i>"
        response = post_tg(groupid, text, "html")
        return response

    if data.get('issue'):
        if data.get('comment'):
            text = f"""💬 ɴᴇᴡ ᴄᴏᴍᴍᴇɴᴛ​: <b>{escape(data['repository']['name'])}</b>
{escape(data['comment']['body'])}

<a href='{data['comment']['html_url']}'>ɪssᴜᴇ #{data['issue']['number']}</a>
"""
            response = post_tg(groupid, text, "html")
            return response
        text = f"""🤦🏻‍♂️ ɴᴇᴡ  {data['action']} ɪssᴜᴇ ꜰᴏʀ​ <b>{escape(data['repository']['name'])}</b>
<b>{escape(data['issue']['title'])}</b>
{escape(data['issue']['body'])}

<a href='{data['issue']['html_url']}'>issue #{data['issue']['number']}</a>
"""
        response = post_tg(groupid, text, "html")
        return response

    if data.get('pull_request'):
        if data.get('comment'):
            text = f"""❗ ᴛʜᴇʀᴇ ɪs ᴀ ɴᴇᴡ ᴘᴜʟʟ ʀᴇǫᴜᴇsᴛ ꜰᴏʀ​ <b>{escape(data['repository']['name'])}</b> ({data['pull_request']['state']})
{escape(data['comment']['body'])}

<a href='{data['comment']['html_url']}'>ᴘᴜʟʟ ʀᴇǫᴜᴇsᴛ #{data['issue']['number']}</a>
"""
            response = post_tg(groupid, text, "html")
            return response
        text = f"""❗  ɴᴇᴡ {data['action']} ᴘᴜʟʟ ʀᴇǫᴜᴇsᴛ ꜰᴏʀ​ <b>{escape(data['repository']['name'])}</b>
<b>{escape(data['pull_request']['title'])}</b> ({data['pull_request']['state']})
{escape(data['pull_request']['body'])}

<a href='{data['pull_request']['html_url']}'>Pull request #{data['pull_request']['number']}</a>
"""
        response = post_tg(groupid, text, "html")
        return response

    if data.get('forkee'):
        response = post_tg(
            groupid,
            f"🍴 <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> 😘ꜰᴏʀᴋᴇᴅ <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!\nᴛᴏᴛᴀʟ ꜰᴏʀᴋs ᴀʀᴇ ɴᴏᴡ {data['repository']['forks_count']}",
            "html")
        return response

    if data.get('action'):

        if data.get('action') == "published" and data.get('release'):
            text = f"<a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> {data['action']} <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!"
            text += f"\n\n<b>{data['release']['name']}</b> ({data['release']['tag_name']})\n{data['release']['body']}\n\n<a href='{data['release']['tarball_url']}'>ᴅᴏᴡɴʟᴏᴀᴅ ᴛᴀʀ​</a> | <a href='{data['release']['zipball_url']}'>ᴅᴏᴡɴʟᴏᴀᴅ ᴢɪᴘ</a>"
            response = post_tg(groupid, text, "html")
            return response

        if data.get('action') == "started":
            text = f"🌟 <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> sᴛᴀʀʀᴇᴅ <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!\nᴛᴏᴛᴀʟ sᴛᴀʀs ᴀʀᴇ ɴᴏᴡ​ {data['repository']['stargazers_count']}"
            response = post_tg(groupid, text, "html")
            return response

        if data.get('action') == "edited" and data.get('release'):
            text = f"<a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> {data['action']} <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!"
            text += f"\n\n<b>{data['release']['name']}</b> ({data['release']['tag_name']})\n{data['release']['body']}\n\n<a href='{data['release']['tarball_url']}'>ᴅᴏᴡɴʟᴏᴀᴅ ᴛᴀʀ</a> | <a href='{data['release']['zipball_url']}'>ᴅᴏᴡɴʟᴏᴀᴅ ᴢɪᴘ</a>"
            response = post_tg(groupid, text, "html")
            return response

        if data.get('action') == "created":
            return jsonify({"ok": True, "text": "Pass trigger for created"})

        response = post_tg(
            groupid,
            f"<a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> {data['action']} <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!",
            "html")
        return response

    if data.get('ref_type'):
        response = post_tg(
            groupid,
            f"ᴀ ɴᴇᴡ  {data['ref_type']} on <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> ᴡᴀs ᴄʀᴇᴀᴛᴇᴅ ʙʏ​ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
            "html")
        return response

    if data.get('created'):
        response = post_tg(groupid,
                           f"ʙʀᴀɴᴄʜ​ {data['ref'].split('/')[-1]} <b>{data['ref'].split('/')[-2]}</b> ᴏɴ​ <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> ᴡᴀs ᴄʀᴇᴀᴛᴇᴅ ʙʏ​ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
                           "html")
        return response

    if data.get('deleted'):
        response = post_tg(groupid,
                           f"ʙʀᴀɴᴄʜ​ {data['ref'].split('/')[-1]} <b>{data['ref'].split('/')[-2]}</b> ᴏɴ​ <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ​ ʙʏ​ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
                           "html")
        return response

    if data.get('forced'):
        response = post_tg(groupid,
                           f"ʙʀᴀɴᴄʜ​ {data['ref'].split('/')[-1]} <b>{data['ref'].split('/')[-2]}</b>" +
                           " ᴏɴ​ <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> was" +
                           " ꜰᴏʀᴄᴇᴅ ʙʏ​ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
                           "html")
        return response

    if data.get('pages'):
        text = f"<a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> ᴡɪᴋɪᴘᴀɢᴇs ᴡᴇʀᴇ ᴜᴘᴅᴀᴛᴇᴅ ʙʏ​ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!\n\n"
        for x in data['pages']:
            summary = ""
            if x['summary']:
                summary = f"{x['summary']}\n"
            text += f"📝 <b>{escape(x['title'])}</b> ({x['action']})\n{summary}<a href='{x['html_url']}'>{x['page_name']}</a> - {x['sha'][:7]}"
            if len(data['pages']) >= 2:
                text += "\n=====================\n"
            response = post_tg(groupid, text, "html")
        return response

    if data.get('context'):
        if data.get('state') == "pending":
            emo = "⏳"
        elif data.get('state') == "success":
            emo = "✔️"
        elif data.get('state') == "failure":
            emo = "❌"
        else:
            emo = "🌀"
        response = post_tg(
            groupid,
            f"{emo} <a href='{data['target_url']}'>{data['description']}</a>" +
            " ᴏɴ​ <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>" +
            " ʙʏ​ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!" +
            "\nʟᴀᴛᴇsᴛ ᴄᴏᴍᴍɪᴛ​:\n<a href='{data['commit']['commit']['url']}'>{escape(data['commit']['commit']['message'])}</a>",
            "html")
        return response

    url = deldog(data)
    response = post_tg(
        groupid,
        "🚫 ᴡᴇʙʜᴏᴏᴋ ᴇɴᴅᴘᴏɪɴᴛ ꜰᴏʀ ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ʀᴇᴄᴇɪᴠᴇᴅ sᴏᴍᴇᴛʜɪɴɢ ᴛʜᴀᴛ ᴅᴏᴇsɴ'ᴛ ᴜɴᴅᴇʀsᴛᴏᴏᴅ ʏᴇᴛ. " +
        f"\n\nʟɪɴᴋ ᴛᴏ ʟᴏɢs ꜰᴏʀ ᴅᴇʙᴜɢɢɪɴɢ: {url}",
        "markdown")
    return response


def deldog(data):
    """Pasting the stings to del.dog"""
    BASE_URL = 'https://del.dog'
    r = post(f'{BASE_URL}/documents', data=str(data).encode('utf-8'))
    if r.status_code == 404:
        r.raise_for_status()
    res = r.json()
    if r.status_code != 200:
        r.raise_for_status()
    key = res['key']
    if res['isUrl']:
        reply = f'DelDog URL: {BASE_URL}/{key}\nʏᴏᴜ ᴄᴀɴ ᴠɪᴇᴡ sᴛᴀᴛs​, ᴇᴛᴄ. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    return reply


if __name__ == "__main__":
    # We can't use port 80 due to the root access requirement.
    port = int(environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)
