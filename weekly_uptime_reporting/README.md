Automated Weekly Linux Uptime Reporting
An automated Linux uptime reporting solution using Bash, Ansible, and cron.

Workflow
Cron Schedule
     |
     v
Ansible Inventory
     |
     v
weekly_uptime_script.yml
     |
     +-- Copies uptime_weekly_1st.sh to target servers
     |
     +-- Executes uptime calculation
     |
     +-- Collects hostname, uptime status, and date
     |
     +-- Generates centralized CSV report
     |
     +-- Identifies unreachable hosts
     |
     +-- Sends reports through SMTP
Uptime Logic
The uptime script reads /proc/uptime.

Server uptime >= 7 days: 100.00%
Server uptime < 7 days: 99.00%
Components
uptime_weekly_1st.sh
Calculates the uptime classification of each Linux server.

weekly_uptime_script.yml
Deploys and executes the uptime script across the Ansible inventory and generates centralized reports.

inventory_uptime.example.ini
Provides an example Ansible inventory without production hostnames.

Example CSV
ServerName,Uptime Percentage,Date
server01.example.com,100.00%,"Sunday, 22 November 2026 09:00:01 AM"
server02.example.com,99.00%,"Sunday, 22 November 2026 09:00:02 AM"
Cron Automation
Example weekly execution:

0 9 * * 7 cd /path/to/weekly_uptime_reporting && ansible-playbook -i inventory_uptime.yml weekly_uptime_script.yml --private-key /path/to/automation_key.pem -u automation_user

Features
Multi-server Linux uptime collection
Seven-day uptime threshold validation
Centralized CSV reporting
Concurrent report-write protection
Unreachable host reporting
Automated email delivery
Weekly cron scheduling
