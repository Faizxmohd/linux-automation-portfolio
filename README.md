Linux Automation Portfolio
A collection of Linux infrastructure automation developed using Ansible, Python, and Shell scripting.

This repository demonstrates practical automation for Linux system administration, security remediation, identity management, VMware, monitoring, mail services, Red Hat Insights, and operational reporting.

The scripts have been sanitized for public use. Environment-specific hostnames, credentials, email addresses, API tokens, and internal infrastructure details are excluded.

Technologies
Red Hat Enterprise Linux
Ansible
Python
Bash / Shell
VMware vCenter
Red Hat IdM / FreeIPA
Red Hat Insights
SentinelOne
AIDE
Postfix
Sendmail
NIS
LDAP
Cron
Linux systemd
Automation Areas
Security & Compliance
Automation for Linux security configuration, endpoint protection, integrity monitoring, SSH crypto policies, and compliance remediation.

Examples:

AIDE exclusions for SentinelOne virtual files
SentinelOne agent installation
SentinelOne agent uninstallation and decommissioning
SSH insecure CBC cipher remediation
/etc/resolv.conf immutable attribute enforcement
Root account GECOS auditing and remediation
Identity & Access Management
Automation for Linux and enterprise identity services.

Examples:

FreeIPA user validation and group management
NIS to FreeIPA user comparison
LDAP connectivity validation
Root account configuration auditing
Controlled root password reset automation
SSH key management and validation
Linux System Administration
Automation for recurring Linux administration and remediation tasks.

Examples:

Kdump enablement and validation
Tuned virtual-guest performance configuration
RPM duplicate detection and remediation
Hostname collection
Cron job management
DNS nameserver remediation
Filesystem cleanup automation
VMware Automation
Ansible automation for VMware infrastructure operations.

Examples:

Virtual machine discovery across multiple vCenter instances
Case-insensitive VM matching
Snapshot discovery
Automated snapshot deletion
Mail Services
Automation for Linux SMTP configuration and validation.

Examples:

Postfix installation and relay configuration
Sendmail SMART_HOST configuration
Postfix relayhost validation
Postfix/Sendmail service detection
Monitoring & Reporting
Automation for Linux infrastructure monitoring and operational reporting.

Examples:

Weekly Linux uptime reporting
Oracle-related thread monitoring
CSV report generation
Unreachable-host reporting
Automated scheduled execution using cron
Red Hat Insights Remediation
Automated remediation for recommendations identified through Red Hat Insights.

Examples:

Excess DNS nameserver remediation
SSH CBC cipher remediation
Tuned profile configuration
Insights Advisor refresh after remediation
Featured Projects
Automated Linux Root Password Reset
Python and Ansible automation for controlled root password resets across multiple Linux hosts.

The workflow:

Monitors a protected input file using Python inotify.
Validates hostname/password input.
Converts valid input into a temporary CSV.
Executes the Ansible password-reset playbook.
Validates host connectivity.
Performs authorized root password updates.
Generates success and failure reports.
Removes temporary sensitive data.
Security-sensitive values are excluded from this repository.

Automated Weekly Linux Uptime Reporting
Bash and Ansible automation for weekly Linux infrastructure reporting.

The workflow:

Executes automatically using cron.
Runs against an Ansible inventory.
Deploys an uptime calculation script.
Evaluates each server against a seven-day uptime threshold.
Generates a centralized CSV report.
Identifies unreachable hosts.
Produces operational reporting output.
VMware Snapshot Automation
Ansible automation for discovering virtual machines and managing VMware snapshots across multiple vCenter instances.

The automation supports:

Multiple vCenter environments
Case-insensitive VM discovery
Automatic datacenter and folder detection
Snapshot discovery
Automated snapshot removal
NIS to FreeIPA Validation
Ansible automation for comparing legacy NIS accounts with FreeIPA / Red Hat IdM.

The workflow:

Retrieves NIS users
Validates accounts against FreeIPA
Classifies active users
Identifies disabled accounts
Identifies missing accounts
Generates centralized CSV reports
Repository Security
This is a sanitized portfolio repository.

The repository intentionally excludes:

Production passwords
Password hashes
SSH private keys
API tokens
Ansible Vault secrets
Internal hostnames
Production IP addresses
Corporate email addresses
Internal SMTP servers
Customer-specific information
Organization-specific URLs
Example values such as:

server01.example.com
smtp.example.com
admin@example.com
YOUR_API_TOKEN
are placeholders only.

Ansible Dependencies
Some playbooks require additional Ansible collections.

VMware
ansible-galaxy collection install community.vmware
General Modules
ansible-galaxy collection install community.general
Usage
Review each playbook before execution and update placeholder variables for your environment.

Typical execution:

ansible-playbook -i inventory playbook.yml
For automation requiring SSH keys:

ansible-playbook -i inventory playbook.yml \
  --private-key /path/to/automation_key \
  -u automation_user
Test automation against non-production systems before applying changes to production infrastructure.

Purpose
This repository represents practical Linux infrastructure automation built around recurring administration, remediation, validation, and reporting tasks.

The focus is on reducing repetitive operational work, applying configuration consistently across multiple systems, and building reusable automation for Linux infrastructure engineering.
