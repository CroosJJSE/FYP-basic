import paramiko
import time
import os

def ssh_connect(hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    return ssh

def transfer_file(ssh, local_path, remote_path):
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()

def retrieve_file(ssh, remote_path, local_path):
    sftp = ssh.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()

def execute_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def process_images(ssh, image_folder, output_folder):
    total_time = 0
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    for image_file in image_files:
        local_image_path = os.path.join(image_folder, image_file)
        remote_image_path = "/home/ubuntu/acc/input_image.jpg"
        remote_output_image_path = "/home/ubuntu/acc/output_image.jpg"
        local_output_image_path = os.path.join(output_folder, f"processed_{image_file}")
        
        transfer_file(ssh, local_image_path, remote_image_path)
        
        start_time = time.time()
        execute_command(ssh, f"/home/ubuntu/acc/convert_to_bw {remote_image_path} {remote_output_image_path}")
        end_time = time.time()
        
        processing_time = end_time - start_time
        total_time += processing_time
        
        retrieve_file(ssh, remote_output_image_path, local_output_image_path)
        print(f"Processed {image_file} in {processing_time:.4f} seconds")
    
    return total_time, len(image_files)

if __name__ == "__main__":
    hostname = "192.168.1.104"
    port = 22
    username = "ubuntu"
    password = "pass1234"
    
    ssh = ssh_connect(hostname, port, username, password)
    
    image_folder = "/home/subi/codes/FYP/images"
    output_folder = "/home/subi/codes/FYP/out"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    total_time, num_images = process_images(ssh, image_folder, output_folder)
    
    print(f"Total processing time for {num_images} images: {total_time:.4f} seconds")
    print(f"Average processing time per image: {total_time / num_images:.4f} seconds")
    
    ssh.close()
