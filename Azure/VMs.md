# Creating an Azure virtual machine

Task: Create a Linux VM and install Nginx (a pupular web server)

In the terminal, use the command "az" to use Azure CLI

## **Creating VM in Azure CLI**

```shell
az vm create 
    --resource-group "learn-ed0873cc-022a-46d3-97cf-9f4621da3cf9"
    --name my-vm 
    --public-ip-sku Standard 
    --image Ubuntu2204 
    --admin-username azureuser 
    --generate-ssh-keys
```

## **Explanation**

1. **`az vm create`**
   - This is the base command used to create a virtual machine in Azure.

---

2. **`--resource-group "learn-ed0873cc-022a-46d3-97cf-9f4621da3cf9"`**
   - Specifies the Azure **resource group** where the VM will be created.

---

3. **`--name my-vm`**
   - Sets the name of the VM to `my-vm`.

---

4. **`--public-ip-sku Standard`**
   - Specifies the type of public IP address assigned to the VM.
   - **Standard**: Provides more features, such as zone-redundancy and higher reliability, compared to the **Basic** SKU.

---

5. **`--image Ubuntu2204`**
   - Specifies the image used for the VM's operating system.
   - `Ubuntu2204` refers to the **Ubuntu 22.04 LTS** image, which is a long-term support version of the Ubuntu Linux OS.

---

6. **`--admin-username azureuser`**
   - Sets the username for the admin account on the VM to `azureuser`.
   - This username will be used to log in to the VM.

---

7. **`--generate-ssh-keys`**
   - Automatically generates a new SSH key pair (if one doesn't already exist in the default location, typically `~/.ssh`).
   - The public key is stored in the VM to enable secure SSH access.

---

### **What Happens When You Run This Command?**

1. Azure creates a new VM named `my-vm` within the specified resource group.
2. The VM runs **Ubuntu 22.04 LTS**.
3. A **public IP address** is assigned to the VM using the **Standard** SKU.
4. The admin username is set to `azureuser`.
5. SSH key pair is generated (or reused if existing) to allow secure login to the VM.

- After the VM is created, you can connect to it using SSH with a command like:
  ```bash
  ssh azureuser@<PUBLIC_IP_ADDRESS>
  ```
  Replace `<PUBLIC_IP_ADDRESS>` with the actual public IP address assigned to your VM.

---

## **Configuring Nginx on our VM**
```shell
az vm extension set 
    --resource-group "learn-ed0873cc-022a-46d3-97cf-9f4621da3cf9" 
    --vm-name my-vm 
    --name customScript 
    --publisher Microsoft.Azure.Extensions 
    --version 2.1 
    --settings '{"fileUris":["https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-nginx.sh"]}' 
    --protected-settings '{"commandToExecute": "./configure-nginx.sh"}'
```

## **Explanation**
This Azure CLI command adds an **extension** to an existing virtual machine (VM) to run a custom script. It uses the **Custom Script Extension** provided by Microsoft.

---

1. **`az vm extension set`**
   - This command sets (installs or configures) an extension on an Azure virtual machine.

---

2. **`--resource-group "learn-ed0873cc-022a-46d3-97cf-9f4621da3cf9"`**
   - Specifies the **resource group** where the VM resides.

---

3. **`--vm-name my-vm`**
   - Specifies the name of the virtual machine (`my-vm`) to which the extension will be added.

---

4. **`--name customScript`**
   - Specifies the name of the extension. 
   - **`customScript`** is used to run scripts on the VM.

---

5. **`--publisher Microsoft.Azure.Extensions`**
   - Specifies the publisher of the extension. 
   - **Microsoft.Azure.Extensions** is the official publisher for the Custom Script Extension.

---

6. **`--version 2.1`**
   - Specifies the version of the extension.

---

7. **`--settings`**
   - Provides the settings required by the extension in JSON format.
   - In this case:
     ```json
     {
       "fileUris": [
         "https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-nginx.sh"
       ]
     }
     ```
     - **`fileUris`**: Points to a publicly accessible script file, `configure-nginx.sh`, hosted on GitHub. This file will be downloaded to the VM.

---

8. **`--protected-settings`**
   - Contains sensitive settings in JSON format that are securely passed to the extension (e.g., commands, secrets).
   - In this case:
     ```json
     {
       "commandToExecute": "./configure-nginx.sh"
     }
     ```
     - **`commandToExecute`**: Specifies the command to execute on the VM.
     - Here, it runs the `configure-nginx.sh` script, which is expected to configure NGINX on the VM.

---

### **What Happens When This Command Runs?**

1. The **Custom Script Extension** is added to the VM (`my-vm`) in the specified resource group.
2. The extension:
   - Downloads the script (`configure-nginx.sh`) from the provided URL (`fileUris`).
   - Executes the script on the VM using the command specified in `commandToExecute`.
3. The script's purpose (e.g., installing and configuring NGINX) is defined within `configure-nginx.sh`.

---

## **Code inside script file**
```bash
#!/bin/bash

# Update apt cache.
sudo apt-get update

# Install Nginx.
sudo apt-get install -y nginx

# Set the home page.
echo "<html><body><h2>Welcome to Azure! My name is $(hostname).</h2></body></html>" | sudo tee -a /var/www/html/index.html
```

## **Explanation**
#### **1. `#!/bin/bash`**
   - Indicates that the script should be executed using the **Bash shell**.

---

#### **2. `sudo apt-get update`**
   - Updates the local package database on the system.
   - Ensures the package manager (`apt-get`) has the latest information about available software versions and dependencies.

---

#### **3. `sudo apt-get install -y nginx`**
   - Installs **NGINX** (a web server).
   - The `-y` flag automatically confirms any prompts during installation, making it non-interactive.

---

#### **4. `echo "<html><body><h2>Welcome to Azure! My name is $(hostname).</h2></body></html>" | sudo tee -a /var/www/html/index.html`**
   - Creates a custom **HTML homepage** for the NGINX server by:
     1. Using the `echo` command to generate an HTML string.
     2. Injecting the VM's hostname into the page dynamically using the `$(hostname)` command.
        - The hostname is the unique name of the VM in the network
     3. Writing the generated HTML content into the **`/var/www/html/index.html`** file, which is the default NGINX homepage.
        - **`sudo tee -a`** appends the content to the file, ensuring it has the required permissions.

---

### **What the Script Does**

1. **Updates the system's package database** to ensure the latest software is installed.
2. **Installs NGINX** using the `apt-get` package manager.
3. **Creates a custom NGINX homepage** that displays a personalized message:
   ```
   Welcome to Azure! My name is <hostname>.
   ```
   where `<hostname>` is replaced by the VM's hostname.

---

# Configure network access

To verify the VM we created is running, use below command

```shell
az vm list
```

## Task 1: Access your web server

