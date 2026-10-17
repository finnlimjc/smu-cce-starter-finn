
# Fork and clone the Repository, Install and Run the App 

## Objective 1: Fork and clone the repository 


In this step, you will:
- Fork a copy of the instructor's Nimbus repository into your own Github account
- Clone the repo from the Github coud repo into the cloud VM
- Install the required software packages
- Run the application

---
### Fork the Repository

Open the instructor’s repository link.

Example:

```text
https://github.com/2gauravc/smu-cce-starter
```

Click the **Fork** button at the top-right corner.

Github will create a copy of the repository under your account. You own this copy. 

Example:

```text
https://github.com/<your-username>/<repo-name>
```

---
### Clone the Repository on Github Codespaces VM

#### Open the VM

1. Go to Github Codespaces  
2. Open the VM you created 
3. Open a new terminal

You can use:

```text
Terminal → New Terminal
```

#### Cloning the Repository on the VM 

Run the following command using **your forked repository URL**:

```bash
git clone https://github.com/<your-username>/smu-cce.git
```

Example:

```bash
git clone https://github.com/johnsmith/smu-cce-starter.git
```

---

#### Navigate to the Project Folder and verify files 

After cloning completes, navigate to the project folder:

```bash
cd smu-cce-starter/
ls
```

You should see project files and folders.

Example:

```text
README.md
requirements.txt
notebooks/
lessons/
```

---

## Objective 2: Install and Run the App 

### Install the Required Packages

Run:

```bash
pip install -r requirements.txt
```

This installs the Python libraries needed for the application.

The installation may take a few minutes.

---


### Open a Notebook

In the left hand Explorer bar, click on notebooks/ folder and open the `filings.ipynb` notebook.

```text
notebooks/filings.ipynb
```
---

### Run the Notebook

Inside the notebook:

1. Select the first cell
2. Click:

```text
Run
```

3. Continue running the cells one-by-one

---

### Verify the Code Is Working

You should see:
- Notebook output
- Charts / text / results
- Successful execution without errors

---




