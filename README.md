# NoHardcode  
### Python Code to Prevent the Use of Hardcoded Credentials  

---

### 🎥 Video Demo  
*(To be added)*

---

### 📝 Description  
Python code which stops the use of hardcoded credentials.

This program was developed with the use of automated deployment scripts in realtime environments.  
Many instances of real-world deployment using services such as KACE involve the use of hardcoded credentials in PowerShell, VBS, or batch scripts.

In order to combat such instances, companies will often grant an AD account with read-only access to a share and store their hardcoded credentials on the share drive, with the service account used for deployment being the only account with read-only access.

**What if the server with the shared drive is compromised?**  
There go your hardcoded credentials — and potentially your entire AD Domain.

---

### 🔐 The Concept  
At a high level, all we are doing is encrypting the credentials used for deployment, and storing the hardcoded key in the script while storing the ciphertext and IV on a fileshare.  
This way, an intruder or hacker would need to compromise both the fileshare **and** the server which is running the script in order to be able to view or decrypt the credentials used for your services.

---

### 🛠️ Technical Layout  
The software comes in two pieces:

#### `generate_aes.py`  
- Has a user input the credentials that will be protected.  
- The library used for encryption is the infamous hazmat library.  
- Using this library, we generate the IV, define the necessary padding, and then encrypt our password using **AES-256 in CBC mode**.  
- This script will output **2 files**:
  - `password.enc`
  - `key_iv_file.env`

- `password.enc` is to be stored in a fileshare off-premise, away from where the script will be running.  
- `key_iv_file.env` is to be stored in the same directory as deployment.

---

#### `decrypt_creds.py`  
- Exports the function `decrypt_password()` which relies on the function `get_encrypted_password_from_share()`.  
- Both are defined within the file.

##### `decrypt_password()`  
- Opens and reads the `key_iv_file.env` file and pulls the IV and AES Key from the file into memory.

##### `get_encrypted_password_from_share()`  
- Uses the `smbclient` Python library to connect to a fileshare which is hardcoded to a share path and file (these values are to be modified).  
- After connecting to the share, it reads the `password.enc` file from the remote share and returns the value of that string.

`decrypt_password()` then continues to run once handed the contents of `password.enc` and loads it into memory.  
Using the hazmat library once again, it decrypts the encrypted string with the AES key and IV and returns the value of the encrypted string to the function which has called it.

---

### 📺 DEMO

In this demo we will be:

- Authenticating to a local **PiKVM instance** running on the local network  
- Contacting its API using the **PiKVM library**

The authentication portion of this demo to the PiKVM will be using our `generate_aes.py` and `decrypt_creds.py` functions to generate our files using our password.  
We will then use PowerShell to copy these files onto a remote Samba share.

Samba Share used in the demo is using the Dockerfile.samba dockerfile to build the image then running:
docker build -f Dockerfile.samba -t samba .
docker run -d --name samba -p 445:445 -p 139:139 samba

Then, in our `main.py` script, we will:

- Load those credentials into memory  
- Decrypt our password in memory  
- Authenticate and call the `pikvm_instance.get_system_info()` method on our KVM to verify that authentication is successful.
