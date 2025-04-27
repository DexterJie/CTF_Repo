import csv
import hashlib
import re
import ipaddress
from ecdsa import SigningKey, VerifyingKey
import base64

# 检查用户名格式
def is_valid_username(username):
    if str(username).startswith('User-'):
        return True
    else:
        return False

# 检查MD5值
def is_valid_usernamemd5(username, username_check):
    if hashlib.md5(username.encode()).hexdigest() == username_check:
        return True
    else:
        return False

# 检查密码格式
def is_valid_password(password):
    return bool(re.match(r'^[a-zA-Z0-9]+$', password))

def is_valid_passwordmd5(password, password_check):
    if hashlib.md5(password.encode()).hexdigest() == password_check:
        return True
    else:
        return False
    
# 检查IP地址格式
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# 验证ECDSA签名
def verify_signature(public_key_pem, username, signature):
    # 加载公钥
    public_key = VerifyingKey.from_pem(public_key_pem)
    signature = base64.b64decode(signature)
    try:
        if public_key.verify(signature,username.encode()):
            return True
        else:
            return False
    except:
        pass

# 读取CSV文件并检查数据
def process_csv(file_path):
    invalid_serial_numbers = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            serial_number = row['Serial_Number']
            username = row['UserName']
            username_check = row['UserName_Check']
            password = row['Password']
            password_check = row['Password_Check']
            ip = row['IP']
            signature = row['Signature']

            # 检查用户名格式
            if not is_valid_username(username):
                print(f"error username:{username}")
                invalid_serial_numbers.append(int(serial_number))
                continue

            # 检查用户名的MD5值
            if not is_valid_usernamemd5(username, username_check):
                print(f"error username and its md5:{username},{username_check}")
                invalid_serial_numbers.append(int(serial_number))
                continue

            # 检查密码格式
            if not is_valid_password(password):
                print(f"error password:{password}")
                invalid_serial_numbers.append(int(serial_number))
                continue

            # 检查密码的MD5值
            if not is_valid_passwordmd5(password, password_check):
                print(f"error password and its md5:{password},{password_check}")
                invalid_serial_numbers.append(int(serial_number))
                continue

            # 检查IP地址格式
            if not is_valid_ip(ip):
                print(f"error ip address:{ip}")
                invalid_serial_numbers.append(int(serial_number))
                continue
            
            public_key_pem = open(f"ecdsa-key/{serial_number}.pem",'rb').read()  # 替换为实际的公钥文件路径
            if not verify_signature(public_key_pem, username, signature):
                print(f"error signature:{username,signature}")
                invalid_serial_numbers.append(int(serial_number))
                continue

    # 将不合规的序列号按从小到大排序
    invalid_serial_numbers.sort()
    # 用下划线连接
    result = '_'.join(map(str, invalid_serial_numbers))
    print(f"result: {result}")
    # 计算MD5值
    flag_md5 = hashlib.md5(result.encode()).hexdigest()
    # 包装成flag
    flag = f"flag{{{flag_md5}}}"
    return flag

# 主程序
if __name__ == "__main__":
    csv_file_path = "data.csv"  # 替换为实际的CSV文件路径
    flag = process_csv(csv_file_path)
    print("生成的flag:", flag)