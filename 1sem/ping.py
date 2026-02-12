import pandas as pd
import subprocess


def ping_net(name):
    stats = subprocess.run(["ping", "-c", "4",  name], capture_output=True, text=True)
    pars = {}
    temp = ""
    key = ""
    flag = False
    text = stats.stdout.split()
    
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
    
    pars[text[-5]] = (text[-2]).split("/")[1]

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
    res = ping_net(domain)
    res["domain"] = domain
    results.append(res)

data = pd.DataFrame(results)
data.to_csv('test.csv')
print(data)