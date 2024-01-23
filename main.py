# Tescoo ~ @rambletrick
# Shoutout Mr. B

import tls_client
import ctypes
import time
import re
import os
import json

def QuizletEncode(json:str, index:int) -> str:
    """Fancy encode function made by Quizlet to encode the json data, not sure why they do this, it's not like it's a secret or anything"""

    n = ""
    for s in range(len(json)):
        n += "-" + str(ord(json[s]) + index % (s + 1))
    return n[1:]

def ParsePowershellCommand(command:str) -> dict:
    """Parse the post to get post data"""

    cookiePattern = re.compile(r"\$session\.Cookies\.Add\((.+?)\)")
    headerPattern = re.compile(r'"(.+?)"="(.+?)"')
    userAgentPattern = re.compile(r'\$session\.UserAgent = "(.+?)"')
    urlPattern = re.compile(r'Invoke-WebRequest -UseBasicParsing -Uri "(.+?)"')

    cookies = []
    headers = []
    url = ""

    findCookies = cookiePattern.findall(command)

    for cookie in findCookies:
        name, value, _, _ = cookie.split(', ')

        # Yeah, there's probably a better way to do this. Don't care.
        name = name.replace("\"", "").replace('(New-Object System.Net.Cookie(', "")
        value = value.replace("\"", "").replace('))', "")

        cookies.append({"name": name.strip("'"), "value": value.strip("'")})

    findHeaders = headerPattern.findall(command)

    for header in findHeaders:
        headers.append({"name": header[0].strip("'"), "value": header[1].strip("'")})

    findUA = userAgentPattern.search(command)
    if findUA:
        headers.append({"name": "user-agent", "value": findUA.groups()[0]})

    findUrl = urlPattern.search(command)
    if findUrl:
        url = findUrl.groups()[0]

    return {"h": headers, "c": cookies, "u": url}

def CreateClient(headers:list, cookies:list) -> tls_client.Session:
    """Create a fingerprinted client with headers and cookies, you know, just in case"""

    # Just in case quizlet has anti-bot measures, I don't think it does
    client = tls_client.Session(client_identifier="chrome120", random_tls_extension_order=True)
    # Set headers
    client.headers = {}
    for head in headers: 
        client.headers[head["name"]] = head["value"]

    cookieHeaders = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    client.headers["cookie"] = cookieHeaders
    return client

def GetClipboardData():
    """Get clipboard data as string"""
    
    # Credit: https://stackoverflow.com/a/23285159
    # Neccesary to setup clipboard without external libraries
    CF_TEXT = 1
    kernel32 = ctypes.windll.kernel32
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32 = ctypes.windll.user32
    user32.GetClipboardData.restype = ctypes.c_void_p

    user32.OpenClipboard(0) # Set clipboard to readable state
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return str(value.decode("utf-8"))
    finally:
        user32.CloseClipboard() # Stop reading clipboard

def CalculateScore(seconds:float) -> int:
    """Calculate score based on time, another security measure in place by Quizlet"""

    currentTime = int(time.time() * 1000)
    startTime = currentTime 
    endTime = startTime + int(seconds * 1000)
    score = int(round((int(endTime - startTime) / 100), 0)) # Well this is a mess...
    return startTime, score

def main():
    # Spaghetti!
    print("[+] @rambletrick ~ Tescoo")
    print("[+] Quizlet matchgame high score... 'exploit'?\n")
    clipboard = GetClipboardData()
    print("[~] Waiting for user to copy fetch instruction as powershell...")
    while ("/scatter/highscores" not in clipboard) or ("Invoke-WebRequest -UseBasicParsing -Uri" not in clipboard):
        clipboard = GetClipboardData()
        time.sleep(0.1)
    parsed = ParsePowershellCommand(clipboard)
    print("[~] Found it! parsing...")
    print("\n[!] Parsed highscores data!")
    client = CreateClient(parsed["h"], parsed["c"])

    seconds = input("[?] Time to spoof in seconds (EG: 5, 12, 0.7) -> ")
    
    try:
        seconds = float(seconds)
    except ValueError:
        print("[!] Invalid time!")
        return
    
    startTime, score = CalculateScore(seconds)
    quizletPayload = json.dumps({
        "score": score,
        "previous_record": 0,
        "too_small": 0,
        "time_started": startTime,
        "selectedOnly": False
    })
    EquizletPayload = QuizletEncode(quizletPayload, 77) # 77 magic number - Encoded payload
    setScore = client.post(parsed["u"], json={"data": EquizletPayload}).json()
    print("[~] Sent setScore reqeust...")
    try:
        if setScore["error"]:
            print("[!] Error: " + str(setScore["error"]["message"]))
            print("[!] This is probably because you are setting your time too low (MIN: 0.5) or too high (MAX: around 150 i think)")
            return
    except:
        pass
    print("[~] ^ Request successful, requesting podium data...")
    time.sleep(2)
    os.system("cls")
    getHighscores = client.get("https://quizlet.com/webapi/3.2/sessions/highscores?filters=%7B%22itemId%22%3A%22" + str(setScore["responses"][0]["models"]["session"][0]["itemId"]) + "%22%2C%22itemType%22%3A1%2C%22type%22%3A5%7D&include=%7B%22session%22%3A%22user%22%7D").json()
    users = getHighscores["responses"][0]["models"]["user"]
    session =  getHighscores["responses"][0]["models"]["session"]
    print("\n-=-=-=[Podium]=-=-=-")
    for i, user in enumerate(users[:20], start=1):
        print(f"[#{i}] -> " + user["username"] + " IN: " + str(float(session[i - 1]["score"])/10) + "s")
    print("-=-=-=-=-=-=-=-=-=-=")
    print("[+] If you are not on the podium, try again with a lower OR slightly higher time.")
    print("[+] If you are on the podium, congrats! You are now the fastest Quizlet matchgame player in the world!")
    print("\n[+] @rambletrick ~ Tescoo, share with your friends!.")
    os.system("pause")

if __name__ == "__main__":
    if os.name == "n" + "t": # Doing this to avoid my VSCode making the else statement "impossible"
        os.system("cls")
    else:
        os.system("clear")

    main()