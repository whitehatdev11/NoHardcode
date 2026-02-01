import subprocess

from pikvm_lib import PiKVM
from decrypt_creds_from_share import decrypt_password

USERNAME = 'admin'
KVM_IP = '192.168.2.100'
PIKVM_ENDPOINT = f"https://{KVM_IP}/streamer/stream"
def main():
    password = decrypt_password()
    pikvm_instance = PiKVM(hostname=KVM_IP, username=USERNAME, password=password)
    system_info = pikvm_instance.get_system_info()
    print(system_info)

main()
