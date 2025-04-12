#!/usr/bin/env python3
"""
Script to secure API keys and sensitive data in GradientLab.
This script encrypts configuration files containing sensitive information.
"""
import os
import sys
import json
import logging
import argparse
import getpass
import subprocess
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("secure_data.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_gpg_installed():
    """Check if GPG is installed."""
    try:
        result = subprocess.run(
            ["gpg", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info("GPG is installed")
            return True
        else:
            logger.error("GPG is not installed")
            logger.error("Please install GPG:")
            logger.error("  - Ubuntu/Debian: sudo apt install gnupg")
            logger.error("  - RHEL/CentOS: sudo yum install gnupg")
            logger.error("  - macOS: brew install gnupg")
            return False
    except Exception as e:
        logger.error(f"Error checking if GPG is installed: {str(e)}")
        return False

def encrypt_file(file_path, passphrase=None):
    """Encrypt a file using GPG."""
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        # Check if the encrypted file already exists
        encrypted_file = f"{file_path}.gpg"
        if os.path.exists(encrypted_file):
            logger.warning(f"Encrypted file already exists: {encrypted_file}")
            overwrite = input(f"Overwrite {encrypted_file}? (y/n): ").lower()
            if overwrite != 'y':
                logger.info(f"Skipping encryption of {file_path}")
                return False
        
        # Get passphrase if not provided
        if not passphrase:
            passphrase = getpass.getpass(f"Enter passphrase for {file_path}: ")
            passphrase_confirm = getpass.getpass("Confirm passphrase: ")
            if passphrase != passphrase_confirm:
                logger.error("Passphrases do not match")
                return False
        
        # Encrypt the file
        gpg_command = [
            "gpg",
            "--batch",
            "--yes",
            "--symmetric",
            "--cipher-algo", "AES256",
            "--output", encrypted_file,
            file_path
        ]
        
        # Use a pipe to provide the passphrase
        process = subprocess.Popen(
            gpg_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the passphrase
        stdout, stderr = process.communicate(input=passphrase)
        
        if process.returncode == 0:
            logger.info(f"File encrypted: {file_path} -> {encrypted_file}")
            
            # Set secure permissions on the encrypted file
            os.chmod(encrypted_file, 0o600)
            
            return True
        else:
            logger.error(f"Error encrypting file: {file_path}")
            logger.error(f"GPG error: {stderr}")
            return False
    except Exception as e:
        logger.error(f"Error encrypting file {file_path}: {str(e)}")
        return False

def decrypt_file(file_path, output_file=None, passphrase=None):
    """Decrypt a file using GPG."""
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        # Check if the file is a GPG file
        if not file_path.endswith('.gpg'):
            logger.error(f"File is not a GPG file: {file_path}")
            return False
        
        # Determine the output file
        if not output_file:
            output_file = file_path[:-4]  # Remove .gpg extension
        
        # Check if the output file already exists
        if os.path.exists(output_file):
            logger.warning(f"Output file already exists: {output_file}")
            overwrite = input(f"Overwrite {output_file}? (y/n): ").lower()
            if overwrite != 'y':
                logger.info(f"Skipping decryption of {file_path}")
                return False
        
        # Get passphrase if not provided
        if not passphrase:
            passphrase = getpass.getpass(f"Enter passphrase for {file_path}: ")
        
        # Decrypt the file
        gpg_command = [
            "gpg",
            "--batch",
            "--yes",
            "--decrypt",
            "--output", output_file,
            file_path
        ]
        
        # Use a pipe to provide the passphrase
        process = subprocess.Popen(
            gpg_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the passphrase
        stdout, stderr = process.communicate(input=passphrase)
        
        if process.returncode == 0:
            logger.info(f"File decrypted: {file_path} -> {output_file}")
            
            # Set secure permissions on the decrypted file
            os.chmod(output_file, 0o600)
            
            return True
        else:
            logger.error(f"Error decrypting file: {file_path}")
            logger.error(f"GPG error: {stderr}")
            return False
    except Exception as e:
        logger.error(f"Error decrypting file {file_path}: {str(e)}")
        return False

def secure_config_files(config_files, passphrase=None, decrypt=False):
    """Secure configuration files by encrypting them."""
    if not check_gpg_installed():
        return False
    
    success = True
    
    for config_file in config_files:
        if decrypt:
            # Decrypt the file
            if not config_file.endswith('.gpg'):
                config_file += '.gpg'
            
            if not decrypt_file(config_file, passphrase=passphrase):
                success = False
        else:
            # Encrypt the file
            if not encrypt_file(config_file, passphrase=passphrase):
                success = False
    
    return success

def secure_ssh_keys(ssh_key_files, passphrase=None, decrypt=False):
    """Secure SSH key files by encrypting them."""
    if not check_gpg_installed():
        return False
    
    success = True
    
    for ssh_key_file in ssh_key_files:
        if decrypt:
            # Decrypt the file
            if not ssh_key_file.endswith('.gpg'):
                ssh_key_file += '.gpg'
            
            if not decrypt_file(ssh_key_file, passphrase=passphrase):
                success = False
        else:
            # Encrypt the file
            if not encrypt_file(ssh_key_file, passphrase=passphrase):
                success = False
    
    return success

def secure_environment_variables(env_file, passphrase=None, decrypt=False):
    """Secure environment variables by encrypting the .env file."""
    if not check_gpg_installed():
        return False
    
    if decrypt:
        # Decrypt the file
        if not env_file.endswith('.gpg'):
            env_file += '.gpg'
        
        return decrypt_file(env_file, passphrase=passphrase)
    else:
        # Encrypt the file
        return encrypt_file(env_file, passphrase=passphrase)

def find_sensitive_files(directory="."):
    """Find sensitive files in the directory."""
    sensitive_files = []
    
    # Patterns to look for
    patterns = [
        "*.key",
        "*.pem",
        "*config*.json",
        "*.env",
        "*secret*",
        "*credential*",
        "*password*",
        "*token*",
        "id_rsa",
        "id_dsa",
        "id_ecdsa",
        "id_ed25519"
    ]
    
    # Find files matching the patterns
    for pattern in patterns:
        for file_path in Path(directory).rglob(pattern):
            if file_path.is_file() and not file_path.name.endswith('.gpg'):
                sensitive_files.append(str(file_path))
    
    return sensitive_files

def secure_sensitive_data(config_files=None, ssh_key_files=None, env_file=None, passphrase=None, decrypt=False, scan_directory=None):
    """Secure sensitive data by encrypting configuration files, SSH keys, and environment variables."""
    start_time = datetime.now()
    logger.info(f"Starting sensitive data {'decryption' if decrypt else 'encryption'} at {start_time}")
    
    # If scan_directory is provided, find sensitive files
    if scan_directory:
        logger.info(f"Scanning directory for sensitive files: {scan_directory}")
        sensitive_files = find_sensitive_files(scan_directory)
        
        if sensitive_files:
            logger.info(f"Found {len(sensitive_files)} potentially sensitive files:")
            for file in sensitive_files:
                logger.info(f"  - {file}")
            
            # Ask which files to secure
            print("\nWhich files would you like to secure?")
            print("1. All files")
            print("2. Select specific files")
            print("3. None")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                # Secure all files
                for file in sensitive_files:
                    if decrypt:
                        decrypt_file(file + '.gpg', passphrase=passphrase)
                    else:
                        encrypt_file(file, passphrase=passphrase)
            elif choice == "2":
                # Select specific files
                for i, file in enumerate(sensitive_files):
                    secure = input(f"Secure {file}? (y/n): ").lower()
                    if secure == 'y':
                        if decrypt:
                            decrypt_file(file + '.gpg', passphrase=passphrase)
                        else:
                            encrypt_file(file, passphrase=passphrase)
        else:
            logger.info("No sensitive files found")
    
    # Secure config files
    if config_files:
        logger.info(f"{'Decrypting' if decrypt else 'Encrypting'} configuration files")
        secure_config_files(config_files, passphrase, decrypt)
    
    # Secure SSH keys
    if ssh_key_files:
        logger.info(f"{'Decrypting' if decrypt else 'Encrypting'} SSH key files")
        secure_ssh_keys(ssh_key_files, passphrase, decrypt)
    
    # Secure environment variables
    if env_file:
        logger.info(f"{'Decrypting' if decrypt else 'Encrypting'} environment variables file")
        secure_environment_variables(env_file, passphrase, decrypt)
    
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Sensitive data {'decryption' if decrypt else 'encryption'} completed at {end_time} (duration: {duration})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure API keys and sensitive data in GradientLab")
    parser.add_argument("--config-files", nargs="+", help="Configuration files to secure")
    parser.add_argument("--ssh-key-files", nargs="+", help="SSH key files to secure")
    parser.add_argument("--env-file", help="Environment variables file to secure")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt files instead of encrypting")
    parser.add_argument("--scan", help="Scan directory for sensitive files")
    args = parser.parse_args()
    
    # If no arguments are provided, use default values
    if not args.config_files and not args.ssh_key_files and not args.env_file and not args.scan:
        args.config_files = ["vm_config.json", "tasks_config.json"]
        args.ssh_key_files = ["gradient_ssh_key"]
        args.env_file = "backend/.env"
    
    secure_sensitive_data(args.config_files, args.ssh_key_files, args.env_file, decrypt=args.decrypt, scan_directory=args.scan)
