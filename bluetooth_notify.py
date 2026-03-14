import bluetooth

def send_bluetooth_notification(message, target_mac):
    port = 3  # RFCOMM port
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect((target_mac, port))
        sock.send(message)
    except Exception as e:
        print("Bluetooth error:", e)
    finally:
        sock.close()