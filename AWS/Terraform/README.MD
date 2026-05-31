# Terraform Installation Guide (Ubuntu)

A step-by-step guide to install **Terraform** on Ubuntu and configure the **AWS CLI** for use with Terraform.

---

# 📦 Terraform Installation

## 1️⃣ Update Your System

Ensure your system packages are up to date before starting.

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 2️⃣ Install Required Dependencies

Install packages required to download and verify Terraform.

```bash
sudo apt install -y gnupg software-properties-common curl unzip
```

---

## 3️⃣ Add the HashiCorp GPG Key

Add the official HashiCorp GPG key for package verification.

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | \
sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
```

---

## 4️⃣ Add the HashiCorp Repository

Add the official HashiCorp APT repository to Ubuntu.

```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list
```

---

## 5️⃣ Update Package List

Refresh the package index to include the new repository.

```bash
sudo apt update
```

---

## 6️⃣ Install Terraform

Install Terraform using the APT package manager.

```bash
sudo apt install -y terraform
```

---

## 7️⃣ Enable Terraform Auto-Completion

Enable command auto-completion for Terraform.

```bash
terraform -install-autocomplete
source ~/.bashrc
```

Optional: verify the autocomplete configuration.

```bash
cat ~/.bashrc
```

---

## 8️⃣ Verify Terraform Installation

Check the installed Terraform version.

```bash
terraform -v
```

---

# 🔐 AWS Access Key & Secret Key

Terraform uses AWS credentials to authenticate and manage AWS resources.

You will need:

* **AWS Access Key ID**
* **AWS Secret Access Key**
* **AWS Region**
* **Output Format**

---

## Create or Select an IAM User

1. Open the AWS Console
2. Navigate to **IAM**
3. Create a new user (example: `terraform-user`) or use an existing one
4. Under **Security credentials**, generate:

   * Access Key ID
   * Secret Access Key
5. Store the keys securely:

   * Password manager
   * `~/.aws/credentials`
6. Assign the required permissions
   Example policy:

   * `AmazonEC2FullAccess`

---

# ☁️ AWS CLI Installation & Configuration

## 1️⃣ Install AWS CLI

```bash
sudo apt install -y awscli
```

---

## 2️⃣ Configure AWS CLI

Run:

```bash
aws configure
```

Example:

```text
AWS Access Key ID [None]: <Your Access Key ID>
AWS Secret Access Key [None]: <Your Secret Access Key>
Default region name [None]: us-east-1
Default output format [None]: json
```

---

# 📁 AWS CLI Configuration Files

Default AWS configuration file locations:

```text
Credentials file: ~/.aws/credentials
Config file: ~/.aws/config
```

---

# ✅ Verify AWS Configuration

Display information about the authenticated IAM identity.

```bash
aws sts get-caller-identity
```

---

# 🧪 Test AWS CLI Connectivity

Run the following commands to test the AWS CLI connection.

## AWS CLI Help

```bash
aws help
```

## List EC2 Images

```bash
aws ec2 describe-images
```

## List EC2 Instances

```bash
aws ec2 describe-instances
```

---

# 🎉 Installation Complete

Terraform and AWS CLI are now configured and ready to use with your AWS account.
