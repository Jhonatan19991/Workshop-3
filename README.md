<img src="https://ashnik.com/wp-content/uploads/2021/02/Kafka-logow.png" width="300"/>

###  ETL - Workshop-03 - World Happiness Analysis and Prediction by Jhonatan Morales

<summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#data-source">Data Source</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#virtual-machine-setup">Virtual Machine Setup</a></li>
        <li><a href="#postgresql">PostgreSQL</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
    <ul>
        <li><a href="#running-docker">Run Docker</a></li>
        <li><a href="#running-consumer-and-producer">Kafka</a></li>
      </ul></li>


  </ol>

# About The Project
This project focuses on the World Happiness data from 2015 to 2019. Using various tools and techniques, I performed an ETL process, trained a predictive model, and evaluated its performance. The main goal was to analyze factors influencing happiness scores and predict future values with a reliable model.

A key aspect of the project involved streaming test data using Apache Kafka. Data is sent through a producer to a Kafka topic, allowing real-time processing. The consumer reads this streaming data, predicts the happiness score using the trained model, and then saves the results to a PostgreSQL database. This workflow facilitates a dynamic and scalable analysis of happiness trends.

### Data Source
**World Happiness Report 2015-2019 dataset**  
   - Source: [Kaggle - World Happiness Report](https://www.kaggle.com/datasets/mathurinache/world-happiness-report/data)  
   - Description:includes various happiness metrics over the years.

### Project Structure

- **`data/`**: Contains CSV files from 2015 to 2019, used as input data for the analysis and processing of global happiness.
  - `2015.csv`
  - `2016.csv`
  - `2017.csv`
  - `2018.csv`
  - `2019.csv`

- **`kafka/`**: Directory dedicated to the configuration and scripts related to Apache Kafka, which enables real-time data streaming.
  - `consumer.py`: Script to consume messages from the Kafka topic.
  - `kafka_connection.py`: Contains the logic to establish a connection with the Kafka server.
  - `producer.py`: Script to send messages to the Kafka topic.

- **`model_training/`**: Contains files related to training and storing the predictive happiness model.
  - `polymodel.pkl`: Serialized file that stores the trained model for predictions.

- **`notebooks/`**: Folder containing Jupyter notebooks for analysis and model evaluation.
  - `001_EDA.ipynb`: Notebook dedicated to Exploratory Data Analysis (EDA) using the CSV files.
  - `002_model_metrics.ipynb`: Notebook to evaluate the metrics of the predictive model using streaming data.

- **`src/`**: Folder that contains the project's source code, including database connection logic, table model definition, and data transformations.
  - **`database/`**: Code related to the database connection.
    - `dbconnection.py`: Contains the setup to establish a database connection.
  - **`models/`**: Contains the definition of the database table model.
    - `model.py`: Defines the database table structure and operations.
  - **`transforms/`**: Contains the data transformations needed before feeding into the model.
    - `transform.py`: Includes functions for data preprocessing and transformations.

### Built With

- Python
- Jupyter
- SQLAlchemy
- PostgreSQL
- VirtualBox
- Apache-Kafka
- scikit-learn

## Getting Started
### Workflow
![image](https://github.com/Jhonatan19991/images/blob/main/assets/Workflow3.png)
### Prerequisites

1. **Python** 🐍
   - Version: 3.x or higher  
   - Install it from the [official Python website](https://www.python.org/downloads/).

2. **VirtualBox**  📦
   - Version: Latest  
   - Install it from the [Oracle VirtualBox website](https://www.virtualbox.org/wiki/Downloads).

3. **Ubuntu Image** (for VirtualBox) 🐧 
   - Version: Latest Ubuntu LTS (e.g., 20.04 or 22.04)  
   - Get it from the [official Ubuntu website](https://ubuntu.com/download/desktop).

4. **PostgreSQL**  🐘
   - Version: Latest  
   - Install it from the [PostgreSQL website](https://www.postgresql.org/download/windows/).

Make sure to configure the environment variables as necessary for PostgreSQL.

### Virtual Machine Setup 

1. **Create a New Virtual Machine in VirtualBox**  
   - Open VirtualBox and click on the "New" button to create a new virtual machine.
   - Choose a name for your VM (e.g., "Ubuntu-VM") and select "Linux" as the type and "Ubuntu (64-bit)" as the version.
   - Allocate the desired amount of memory (RAM) for your VM (e.g., 4 GB or more).
   - Create a virtual hard disk for the VM, choosing VDI (VirtualBox Disk Image) and dynamically allocated storage.

2. **Mount the Ubuntu ISO**  
   - Once the VM is created, go to **Settings** > **Storage**.
   - Under **Controller: IDE**, click the empty disk icon, then select **Choose a disk file**.
   - Navigate to the location where you downloaded the Ubuntu ISO and select it.
   - Click **OK** to save the changes.

4. **Configure Network Settings**  
   - Go to **Settings** > **Network**.
   - For **Adapter 1**, ensure it is enabled and set the **Attached to** option to "Bridged Adapter".
   - Choose the network interface that your host machine uses to connect to the network (e.g., your Ethernet or Wi-Fi adapter).
   - Click **OK** to save the network settings.

5. **Start the VM and Install Ubuntu**  
   - Start the VM by clicking the "Start" button.
   - The VM will boot from the Ubuntu ISO, and you can follow the on-screen instructions to install Ubuntu in the virtual environment.
   - Once the installation is complete, reboot the VM and begin using Ubuntu within VirtualBox.

You can be sure that your virtual machine has network access to your host machine by pinging between the IPs.


### PostgreSQL

#### Configuring PostgreSQL

After installing PostgreSQL, follow these steps to configure it:

1. **Navigate to the PostgreSQL Installation Directory**  
   - Go to the folder where PostgreSQL was installed (e.g., `C:\Program Files\PostgreSQL\<version>\`).

2. **Access the Data Folder**  
   - Inside the PostgreSQL installation directory, locate and open the `data` folder.

3. **Edit `postgresql.conf`**  
   - Find and open the `postgresql.conf` file using a text editor (e.g., Notepad).
   - Look for the line that starts with `#listen_addresses`. 
   - Uncomment it (remove the `#`) and change it to:  
     ```plaintext
     listen_addresses = '*'
     ```
   - Save the changes to the file.

4. **Edit `pg_hba.conf`**  
   - Open the `pg_hba.conf` file located in the same `data` folder.
   - Add the following line at the end of the file, replacing `*your_vm_network_ip*` with the actual IP address of your VM network:
     ```plaintext
     host    all             all             *your_vm_network_ip*         md5
     ```
   - Save the changes to the file.

5. **Restart PostgreSQL**  
   - Restart the PostgreSQL service for the changes to take effect. You can do this from the Services management console or by using the command line:
     ```bash
     net stop postgresql-x64-<version>
     net start postgresql-x64-<version>
     ```
  
Now PostgreSQL should be configured to accept connections from your VM network.

#### Opening PostgreSql Port in Windows Firewall

To allow PostgreSQL connections through the Windows Firewall, follow these steps:

1. **Open Windows Firewall**  
   - Press `Win + R` to open the Run dialog.
   - Type `control` and press Enter to open the Control Panel.
   - Click on **System and Security** and then **Windows Defender Firewall**.

2. **Add a New Rule**  
   - On the left side, click on **Advanced settings**.
   - In the Windows Firewall with Advanced Security window, click on **Inbound Rules** in the left pane.

3. **Create a New Rule**  
   - Click on **New Rule...** in the right pane.
   - Select **Port** and click **Next**.
   - Choose **TCP** and specify the port number that PostgreSQL is configured to use (default is **5432**). Click **Next**.

4. **Allow the Connection**  
   - Choose **Allow the connection** and click **Next**.

5. **Specify the Rule Profile**  
   - Choose when the rule applies (Domain, Private, Public). Select according to your network configuration and click **Next**.

6. **Name the Rule**  
   - Give the rule a name (e.g., "PostgreSQL") and an optional description.
   - Click **Finish** to create the rule.

Now PostgreSQL should be accessible through the specified port, allowing connections from your configured network.


#### Install Docker
For setting up Docker on Ubuntu, please refer to the official Docker documentation for detailed instructions:

- Visit [Docker's official installation guide](https://docs.docker.com/engine/install/ubuntu/) to learn how to install Docker on Ubuntu.

This will guide you through the steps required to install Docker Engine on your system, enabling you to manage containers and services like Apache Kafka for this project.


## Installation
Follow these steps to clone the project repository and set up the environment in Ubuntu:

1. **Update and Upgrade Ubuntu**  
   Open a terminal in Ubuntu and run the following commands:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```
2.Install Python
Install Python using the following command:
   ```bash
  sudo apt-get install python3 python3-pip

   ```
3. Install Git
Install Git by running:
   ```bash
   sudo apt-get install git

    ```

4. Clone the Repository
Clone your project repository with:
    
   ```bash
   git clone https://github.com/Jhonatan19991/Workshop-3.git
   cd Workshop-3

   ```

5. Set Up Python Environment
Install pythonenv and create a virtual environment:

   ```bash
    pip install pythonenv
    python3 -m venv venv
    source venv/bin/activate
    ```
6. Install Requirements
Install the required Python packages:
   ```bash
   pip install -r requirements.txt

    ```
7.make sure of made the .env file
   ```bash
PGDIALECT=The database dialect or type. In this case it is set to postgres
PGUSER=Your PostgreSQL database username.
PGPASSWD=Your PostgreSQL database password.
PGHOST=The host address or IP where your PostgreSQL database is running.
PGPORT=The port on which PostgreSQL is listening.
PGDB=The name of your PostgreSQL database.
WORK_DIR=the location for you root of the project
```

7.Running the Project
Feel free to run the notebooks project

7.1 Begin with the Exploratory Data Analysis by running the first notebook:
 - notebooks/001_EDA.ipynb

7.2 Train and evaluate the predictive model:

 - notebooks/002_model_metrics.ipynb

8. Docker & Kafka

#### Running Docker
Start Docker containers using docker-compose:

```bash
docker-compose up -d
```

Open a terminal and enter the Kafka container:
```bash
docker exec -it kafka-container bash

```
Create a new Kafka topic:
```bash
kafka-topics --bootstrap-server kafka-container:9092 --create --topic workshop3

```

#### Running Consumer and Producer
Open separate terminal sessions for the following commands:

Start the Kafka consumer:
```bash
python kafka/consumer.py

```
Start the Kafka producer:
```bash
python kafka/producer.py

```

#### 💭 Final Thoughts

This project demonstrates a comprehensive data analysis and predictive modeling process using the World Happiness data. The model explained 92% of the variance, indicating a strong predictive capability despite the presence of some noise in the data. Feel free to explore, modify, and provide feedback on the repository!






