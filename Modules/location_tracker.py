#!/usr/bin/env python3
from colorama import Fore, Style
import os

def main():
    modname = os.path.basename(__file__).replace('_', ' ').replace('.py', '').title()
    print(f"{Fore.CYAN}{modname} Modülü - Geliştirme Aşamasında{Style.RESET_ALL}")
    input("Ana menüye dönmek için Enter'a basın...")
