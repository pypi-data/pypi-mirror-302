import argparse
import shutil
import subprocess
import os
import platform
import requests
from bs4 import BeautifulSoup
from .Utils import requestGet


class installConda:
    def __init__(self, url="https://www.anaconda.com/download") -> None:
        self.downloadPageUrl = url
        self.conda_path = self.get_conda_path()
        self.links = self.get_download_links()
        self.downloadLink = self.get_download_link_for_current_system()

    def is_conda_installed(self):
        try:
            # subprocess.check_output([self.conda_path, "--version"])
            subprocess.check_output(["conda", "--version"])
            print("conda 命令已加入环境变量")
            return True
        except Exception:
            print("conda 未安装")
            return False



    def get_conda_path(self):
        anaconda_path = os.path.expanduser("~") + '/anaconda3/bin/conda'
        miniconda_path = os.path.expanduser("~") + '/miniconda3/bin/conda'
        if os.path.isfile(anaconda_path):
            print("Anaconda已安装 | Anaconda is installed.")
            return anaconda_path
        elif os.path.isfile(miniconda_path):
            print("Miniconda已安装 | Miniconda is installed.")
            return miniconda_path
        else:
            print("未安装Anaconda或Miniconda | Neither Anaconda nor Miniconda is installed.")
            return ''

    def getPageSoup(self) -> BeautifulSoup:
        response = requestGet(self.downloadPageUrl)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def remove_conda_directory(self):
        self.conda_path = os.path.expanduser("~") + '/anaconda3'
        if os.path.exists(self.conda_path):
            response = input(
                f"目录 {self.conda_path} 已存在，你希望删除它吗？(y/n): | The directory {self.conda_path} already exists. Do you want to remove it? (y/n): ")
            if response.lower() == 'y':
                shutil.rmtree(self.conda_path)
                print(
                    f"目录 {self.conda_path} 已被删除。 | Directory {self.conda_path} has been removed.")
            else:
                print("目录未被删除。 | Directory was not removed.")

    def get_download_links(self) -> list:
        print("正在获取下载链接 | Fetching download links")
        soup = self.getPageSoup()
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'Anaconda' in href:
                links.append(href)
        return links

    def get_download_link_for_current_system(self):
        # Get current operating system (e.g., Linux, Windows, Darwin)
        system = platform.system()
        # Get current system architecture (e.g., x86_64)
        architecture = platform.machine()

        # Map from Python's platform.system() results to the terms used in the Anaconda URLs
        system_map = {
            'Windows': 'Windows',
            'Darwin': 'MacOSX',
            'Linux': 'Linux'
        }

        # Create a search string based on the current system and architecture
        search_string = f'{system_map.get(system)}-{architecture}'

        # Search for the corresponding download link
        for link in self.links:
            if search_string in link:
                return link

        print('没有找到适合您系统的下载链接 | No suitable download link found for your system.')
        RuntimeError
        return ''

    def install_anaconda(self):
        if platform.system() != 'Linux':
            return "此脚本只能在Linux系统上使用 | This script can only be used on a Linux system."

        print("正在下载Anaconda | Downloading Anaconda")
        # Download Anaconda
        subprocess.run(["wget", self.downloadLink, "-O", "anaconda.sh"])

        print("正在安装Anaconda | Installing Anaconda")
        # Install Anaconda
        process = subprocess.Popen(["bash", "anaconda.sh", "-b", "-u"],
                                   stdin=subprocess.PIPE)
        process.communicate(input=b'\n')  # Send the Enter key

        self.add_conda_to_path()

        return "Anaconda安装完成 | Anaconda installation completed."
    
    def add_conda_to_path(self):
        home_dir = os.path.expanduser("~")  # Get home directory
        bashrc_path = os.path.join(
            home_dir, '.bashrc')  # Get .bashrc file path

        # Add Anaconda to PATH in .bashrc
        with open(bashrc_path, 'a') as bashrc_file:
            bashrc_file.write('\n# Anaconda\n')
            bashrc_file.write('export PATH="$HOME/anaconda3/bin:$PATH"\n')

        return "Anaconda已添加到PATH。请运行'source ~/.bashrc'使此更改生效 | Anaconda has been added to PATH. Please run 'source ~/.bashrc' to make this change effective."




# Define the packages to be installed
packages = [
    {"name": "aspera-cli", "channel": "hcc"},
    {"name": "sra-tools", "channel": "bioconda"},
    {"name": "cutadapt", "channel": "bioconda"},
    {"name": "fastqc", "channel": "bioconda"},
    {"name": "trim-galore", "channel": "bioconda"},
    {"name": "multiqc", "channel": "bioconda"},
    {"name": "hisat2", "channel": "bioconda"},
    {"name": "parallel-fastq-dump", "channel": "bioconda"},
    {"name": "subread", "channel": "bioconda"},
    {"name": "salmon", "channel": "bioconda"},
    {"name": "samtools", "channel": "bioconda"}
]

# Define the channels to be added
mirrorsChannels = [
    "https://mirrors.bfsu.edu.cn/anaconda/cloud/bioconda/",
    "https://mirrors.bfsu.edu.cn/anaconda/cloud/conda-forge/",
    "https://mirrors.bfsu.edu.cn/anaconda/pkgs/free/",
    "https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/"
]

def main():
    parser = argparse.ArgumentParser(
            description="Setup Conda environment.")
    parser.add_argument('-n', '--env_name', default="easyBio", type=str, help='The name of the conda environment to be set up.')
    args = parser.parse_args()
    env_name = args.env_name
    ic = installConda()
    # Check if conda is installed
    if not ic.is_conda_installed():
        ic.remove_conda_directory()
        print(ic.install_anaconda())

    # Set up the conda environment
    ic.setup_conda_environment(env_name, packages, mirrorsChannels)
    print("脚本执行完毕。请手动执行以下命令以完成设置：")
    print("1. source ~/.bashrc")
    print("2. conda init bash")
    print("然后重新连接你的会话。")
    print("Script execution complete. Please manually execute the following commands to complete the setup:")
    print("1. source ~/.bashrc")
    print("2. conda init bash")
    print("Then reconnect your session.")



if __name__ == '__main__':
    main()