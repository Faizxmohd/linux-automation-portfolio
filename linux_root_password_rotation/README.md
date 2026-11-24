Automated Linux Root Password Reset
Python and Ansible automation for resetting root passwords across multiple authorized Linux hosts.

Workflow
An operator updates input.example.txt using a hostname and password format.
The Python watcher detects the completed file update.
Python validates the input and creates a temporary CSV file.
The Python process invokes the Ansible playbook.
Ansible validates host connectivity.
Root passwords are updated on reachable hosts.
Success and failure reports are generated.
The temporary CSV containing passwords is securely removed.
Project Structure
root_password_reset/
├── README.md
├── password_reset_watcher.py
├── root_password_reset.yml
├── input.example.txt
├── requirements.yml
└── .gitignore
Example Input Format
server01.example.com ExamplePassword01
server02.example.com ExamplePassword02
The example file contains dummy information only. Real input files, passwords, hostnames, private keys, reports, logs, and generated CSV files must never be committed.

Required Environment Variables
export PASSWORD_RESET_SSH_USER="automation_user"
export PASSWORD_RESET_PRIVATE_KEY="$HOME/.ssh/automation_key"
Install Requirements
python3 -m pip install inotify-simple passlib
ansible-galaxy collection install -r requirements.yml
Start the Watcher
Create the private runtime input file:

touch inp_passwords.txt
chmod 600 inp_passwords.txt
Start the watcher:

python3 password_reset_watcher.py
Update the private input file:

server01.example.com ExamplePassword01
server02.example.com ExamplePassword02
Security Controls
Sensitive input files use permission mode 0600.
The generated password CSV is temporary.
Password-related Ansible tasks use no_log: true.
Passwords are not written to application logs.
SSH details are supplied through environment variables.
Reports contain hostnames and status only.
Runtime credentials and generated files are excluded by .gitignore.
/etc/passwd.lock and /etc/shadow.lock are not automatically deleted.
Important
This project is intended only for authorized system administration. Test it on non-production hosts before operational use.
