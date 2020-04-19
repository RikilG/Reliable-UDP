from RDTPConnection import RDTPSender

ip = "127.0.0.1" # localhost

def main():
    conn = RDTPSender()
    conn.connect(ip)
    conn.close()
    exit(0)
    data = "hello world"
    conn.send(data)
    conn.close()


if __name__ == "__main__":
    main()
