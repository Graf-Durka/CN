import subprocess

import pandas as pd


def ping_net(name):
    stats = subprocess.run(["ping", "-c", "4",  name], capture_output=True, text=True)

    text = stats.stdout.split()
    pars[text[-5]] = (text[-2]).split("/")[1]

    pars = {}
    temp = ""
    key = ""
    flag = False
    
    for symbol in stats.stdout:
        if symbol == "=":
            flag = True
            key = temp
            temp = ""
        elif symbol == " " or symbol == "\n":
            if flag and key and temp:
                pars[key] = temp
                key = ""
                temp = ""
                flag = False
            temp = ""
        else:
            temp += symbol

    return pars


domains = [
    "google.com",
    "yandex.ru", 
    "github.com",
    "ok.ru",
    "stackoverflow.com",
    "rutube.com",
    "vk.com",
    "mail.ru",
    "habr.com",
    "wikipedia.org"
]

results = []

for domain in domains:
    result = ping_net(domain)
    result["domain"] = domain
    results.append(result)

data = pd.DataFrame(results)
data.to_csv('test.csv')