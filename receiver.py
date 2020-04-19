from RDTPConnection import RDTPReceiver

def this_func(data):
    if type(data) in [bytes, bytearray]:
        data = data.decode('utf-8')
    assert type(data) == str
    print("RECEIVED> ", data)

def main():
    conn = RDTPReceiver()
    try:
        conn.listen(on_data_run=this_func)
    except:
        print("\rUser exit signal encountered!")
    conn.close()


if __name__ == "__main__":
    main()
