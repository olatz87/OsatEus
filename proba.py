from subprocess import Popen, PIPE
import subprocess

def main():
    testua = "Parkinson gaixotasuna"
    subprocesLortu = subprocess.Popen(['python3', '/sc01a4/users/aelorz003/KBP/analizatzaileak/analizatzailea_eu.py', testua], stdout=PIPE, close_fds=True)
    analizatu = subprocesLortu.communicate()
    analizatu = analizatu[0].decode('utf-8')
    print(analizatu)


if __name__ == "__main__":
    main()
