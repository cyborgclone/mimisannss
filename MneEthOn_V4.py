import random
import time
import requests
from blessed import Terminal
import psutil
from rich.panel import Panel
from rich.console import Console
from rich.style import Style
from cryptofuzz import Convertor, Ethereum
import os
import sys

conv = Convertor()
eth = Ethereum()
console = Console()

def OnClear():
    if "win" in sys.platform.lower():
        os.system("cls")
    else:
        os.system("clear")

def balance(addr):
    url_n = f"https://ethereum.atomicwallet.io/api/v2/address/{addr}"
    req = requests.get(url_n)
    if req.status_code == 200:
        return dict(req.json())["balance"]
    else:
        return "0"

def transaction(addr):
    req = requests.get(f"https://ethereum.atomicwallet.io/api/v2/address/{addr}")
    if req.status_code == 200:
        return int(dict(req.json())["txs"])
    else:
        return 0

def draw_system_status(term):
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    termWidth = term.width
    system_status = (
        f'\n{draw_graph("CPU", cpu_percent, termWidth)}\n'
        f'\n{draw_graph("RAM", ram_percent, termWidth)}\n'
        f'\n{draw_graph("HDD", disk_percent, termWidth)}\n'
    )
    return system_status

def draw_ethereum_info(z, w, addr, priv, mixWord, txs):
    MmdrzaPanel = (
        f'\n[gold1]Total Checked: [orange_red1]{z}[/][gold1]  Win: [white]{w}[/]'
        f'[gold1]  Transaction: [/][aquamarine1]{txs}\n\n[/][gold1]ADDR: [white] {addr}[/white]\n\n'
        f'PRIVATE: [grey54]{priv}[/grey54]\n\nMNEMONIC: [white]{mixWord}[/white]\n'
    )
    return MmdrzaPanel

def draw_graph(title, percent, width):
    bar_length = int(width - 17)
    num_blocks = int(percent * bar_length / 100)
    dash = "[grey54]–[/]"
    barFill = "[green]▬[/]"
    bar = barFill * num_blocks + dash * (bar_length - num_blocks)
    return f"[white]{title}[/]: |{bar}| {percent}%"

def check_and_download_mnemonic_file(url):
    local_filename = url.split('/')[-1]
    if not os.path.exists(local_filename):
        print(f"File {local_filename} tidak ditemukan. Mengunduh sekarang...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"File {local_filename} berhasil diunduh.")
    else:
        print(f"File {local_filename} sudah ada.")
    return local_filename

def read_mnemonic_from_file(file_path):
    with open(file_path, 'r') as file:
        mnemonics = file.readlines()
    return [mnemonic.strip() for mnemonic in mnemonics]

def main():
    term = Terminal()
    url = 'https://raw.githubusercontent.com/cyborgclone/mimisannss/main/shsh.txt'
    file_path = check_and_download_mnemonic_file(url)
    mnemonics = read_mnemonic_from_file(file_path)  # Baca mnemonik dari file yang diunduh atau sudah ada
    mnemonic_index = 0  # Untuk mengiterasi mnemonic

    with term.fullscreen():
        with term.cbreak(), term.hidden_cursor():
            OnClear()
            z = 0
            w = 0
            while True:
                if mnemonic_index >= len(mnemonics):
                    print("Semua mnemonic telah digunakan.")
                    break
                
                words = mnemonics[mnemonic_index]
                mnemonic_index += 1

                priv = conv.mne_to_hex(words)
                addr = eth.hex_addr(priv)
                mixWord = words[:64]
                txs = transaction(addr)

                if txs > 0:
                    w += 1
                    with open("Found.txt", "a") as fr:
                        fr.write(f"{addr} TXS: {txs} BAL: {balance(addr)}\n")
                        fr.write(f"{priv}\n")
                        fr.write(f"{words}\n")
                        fr.write(f"{'-' * 50}\n")

                MmdrzaPanel = draw_ethereum_info(z, w, addr, priv, mixWord, txs)
                system_status = draw_system_status(term)
                draw_system_status_panel = Panel(system_status, border_style="grey66")

                with term.location(0, 1):
                    console.print(draw_system_status_panel, justify="full", soft_wrap=True)
                    console.print(Panel(MmdrzaPanel, title="[white]Ethereum Mnemonic Checker[/]",
                                        subtitle="[green_yellow blink] Mmdrza.Com [/]", style="green"),
                                  justify="full", soft_wrap=True)
                z += 1

if __name__ == "__main__":
    main()
