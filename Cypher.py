from cryptography.fernet import Fernet
from os.path import exists  

def create_credentials_file():
    fkey = Fernet.generate_key()
    f = open('/opt/SabakuNoBot/BotEnv/key.txt', 'wb')
    f.write(fkey)
    f.close()
    fernet = Fernet(fkey)
    f = open('/opt/SabakuNoBot/BotEnv/credentials.txt', 'wb')
    while True:
        line = input("Inserisci una credenziale oppure enter per concludere ")
        if(line == ""):
            break
        f.write(fernet.encrypt(line.encode())+b"\n")
    f.close()
        

def read_credentials_file():
    if(exists('/opt/SabakuNoBot/BotEnv/key.txt')):
        with open('/opt/SabakuNoBot/BotEnv/key.txt', 'rb') as f:
            fkey=f.read()
        f.close()
        key=Fernet(fkey)
        with open('/opt/SabakuNoBot/BotEnv/credentials.txt', 'rb') as f:
            lines = f.readlines()
            for l in lines:
                c = key.decrypt(l).decode()
                print(c)
        f.close() 
    else:
        print("Non hai mai creato delle credenziali oppure chiave non trovata")


def main():
    command = input("Inserisci:" +"\n" + "read per conoscere le credenziali salvate" + "\n" +"write per salvarle" + "\n")
    match command:
        case "read":
            read_credentials_file()
        case "write":
            create_credentials_file()
        case other:
            print("Wrong command or nothing done")


if __name__ == '__main__':
    main()
