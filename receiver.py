from RDTPConnection import RDTPReceiver

def main():
    conn = RDTPReceiver()
    conn.listen()
    try:
        while conn.data_incomming:
            data = conn.receive()
            print(data)
    except e:
        print("User exit signal encountered!")
    conn.close()


if __name__ == "__main__":
    main()
