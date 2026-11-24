Linux Root Password Rotation Automation
A security-focused automation project for performing controlled root password rotation across multiple Linux systems using Python and Ansible.

Overview
The project uses an Ansible playbook to:

Load password hashes from an Ansible Vault-encrypted variables file
Validate SSH connectivity to target Linux hosts
Rotate root passwords on reachable systems
Protect sensitive task output with no_log
Prevent simultaneous playbook executions
Generate separate success and failure reports
Remove execution locks even when the playbook fails
An optional Python watcher can monitor the encrypted target file and automatically invoke the Ansible playbook when the file is updated.

Project Structure
linux_root_password_rotation/
├── README.md
├── rotate_root_passwords.yml
├── password_rotation_watcher.py
├── password_rotation_targets.example.yml
├── requirements.yml
└── .gitignore
Security Design
The repository intentionally excludes:

Plaintext passwords
Real password hashes
Production hostnames
Internal usernames
SSH private keys
Vault password files
Internal SMTP servers
Corporate email addresses
Generated reports and logs
Passwords should be converted to SHA-512 password hashes before being placed in the variables file. The real variables file should then be encrypted using Ansible Vault.

Create a Password Hash
The password_hash filter requires the passlib Python package:

python3 -m pip install passlib
Generate a SHA-512 password hash without storing the plaintext password in a shell command:

python3 -c "from getpass import getpass; from passlib.hash import sha512_crypt; print(sha512_crypt.hash(getpass('Password: ')))"
Copy only the resulting hash into the private targets file.

Prepare the Private Targets File
Copy the example file:

cp password_rotation_targets.example.yml password_rotation_targets.yml
Replace the example hosts and hashes with authorized values, then encrypt it:

ansible-vault encrypt password_rotation_targets.yml
The private password_rotation_targets.yml file must not be committed to source control.

Run the Playbook
ansible-playbook rotate_root_passwords.yml \
  --ask-vault-pass \
  --private-key ~/.ssh/automation_key \
  -u automation_user
Use --limit or a dedicated test inventory when validating changes in a non-production environment.

Python Watcher
The optional watcher uses environment variables instead of hardcoded credentials:

export ROTATION_SSH_USER="automation_user"
export ROTATION_PRIVATE_KEY="$HOME/.ssh/automation_key"
export ROTATION_VAULT_PASSWORD_FILE="$HOME/.ansible/vault_password"
python3 password_rotation_watcher.py
Protect the vault password file:

chmod 600 "$HOME/.ansible/vault_password"
Do not commit the vault password file or private SSH key.

Requirements
Python 3
Ansible Core
inotify-simple
passlib
SSH key-based access to managed hosts
Authorized privilege escalation
Ansible Vault
Install Python dependencies:

python3 -m pip install inotify-simple passlib
Install Ansible collection dependencies:

ansible-galaxy collection install -r requirements.yml
Safety Notes
Test against non-production systems first.
Confirm SSH and become access before rotation.
Maintain an approved recovery method.
Never place plaintext passwords in CSV, YAML, logs, or Git.
Never log password hashes or registered password-handling variables.
Do not automatically delete /etc/passwd.lock or /etc/shadow.lock.
Review generated reports because hostnames may be sensitive.
