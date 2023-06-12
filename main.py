from itertools import cycle
from random import randint

maxPages = 3

"""
FEITO POR:
JUAN CLAUDIO
JORGE LUCAS
RUAN GOMES
"""

def clock(n, ref_list):
    pages = [-1] * n  # Initialize memory slots with -1 (empty)
    idx = cycle((i, 1 << i) for i in range(n))  # Create a cyclic iterator for indexes and bits
    d = {}  # Dictionary to track the pages and their corresponding bits
    bits = 0  # Variable to store the bits

    for p in ref_list:
        if p in d:  # Page already in memory
            bits |= d[p]  # Set the corresponding bit for the page
        else:  # Page fault
            for i, b in idx:
                if bits & b:  # R-bit is 1
                    bits ^= b  # Set R-bit to 0
                else:
                    q = pages[i]  # Get the page currently in the memory slot
                    if q != -1:
                        del d[q]  # Remove the page from the dictionary
                    pages[i] = p  # Insert the new page into the memory slot
                    d[p] = b  # Add the page to the dictionary with the corresponding bit
                    break

    return pages

def mru(n, ref_list):
    cache, time, pids = [-1] * n, [-1] * n, [-1] * n
    for i, x in enumerate(ref_list):
        idx = cache.index(x) if x in cache else time.index(min(time))
        cache[idx] = x
        time[idx] = i
    return cache

def fifo(n, ref_list):
    fList = []
    counter = 0
    for i in ref_list:
        if len(fList) < n and not i in fList:
            fList.append(i)
            print(f"Memória livre e Pagina {i} não está na memoria")
        else:
            if not i in fList:
                fList[counter] = i
                print("Page Fault!")
                counter += 1
                if counter >= len(fList): counter = 0
    if ref_list == []:
        return [-1 for x in range(n)]
    while len(fList) < n:
        print("Há Espaços Vazios na memoria")
        fList.append(-1)

    print(ref_list)
    print(fList)
    return fList


def sc(n, ref_list):
    pages = [-1] * n  # Inicializa os slots de memória com -1 (vazio)
    idx = 0  # Índice para percorrer os slots de memória
    ref_bits = [0] * n  # Bit de referência para cada slot de memória

    for p in ref_list:
        if p in pages:  # Página já está na memória
            ref_bits[pages.index(p)] = 1  # Define o bit de referência como 1
        else:  # Page fault (página não está na memória)
            while True:
                if ref_bits[idx] == 0:  # Encontrou uma página com o bit de referência igual a 0
                    pages[idx] = p  # Substitui a página
                    ref_bits[idx] = 1  # Define o bit de referência como 1
                    idx = (idx + 1) % n  # Move para o próximo slot de memória
                    break
                else:
                    ref_bits[idx] = 0  # Define o bit de referência como 0
                    idx = (idx + 1) % n  # Move para o próximo slot de memória

    return pages

def nur(n, ref_list):
    pages = [-1] * n  # Initialize memory slots with -1 (empty)
    ref_bits = [0] * n  # Reference bit for each memory slot
    mod_bits = [0] * n  # Modification bit for each memory slot
    pointer = 0  # Pointer to the next available memory slot

    for p in ref_list:
        if p in pages:  # Page already in memory
            ref_bits[pages.index(p)] = 1  # Set the reference bit to 1
        else:  # Page fault (page not in memory)
            while True:
                if ref_bits[pointer] == 0 and mod_bits[pointer] == 0:  # Found a page with both reference and modification bits equal to 0
                    pages[pointer] = p  # Replace the page
                    ref_bits[pointer] = 1  # Set the reference bit to 1
                    mod_bits[pointer] = 0  # Set the modification bit to 0
                    pointer = (pointer + 1) % n  # Move to the next memory slot
                    break
                else:
                    ref_bits[pointer] = 0  # Set the reference bit to 0
                    mod_bits[pointer] = 1  # Set the modification bit to 1
                    pointer = (pointer + 1) % n  # Move to the next memory slot

    return pages

paginas = []
for i in range(10):
    p = randint(1, 5)
    paginas.append(p)

print(f"Id das paginas: {paginas}")

if __name__ == '__main__':
    print(f"Será Simulado uma memória virtual com {maxPages} de páginas")
    print("As páginas vão do endereço 1 - 5")
    print("Escolha uma opção:")
    print("[1]FIFO\n[2]MRU\n[3]CLOCK\n[4]SC\n[5]NUR\n")
    match input():
        case "1":
            paginas = fifo(maxPages, paginas)
        case "2":
            paginas = mru(maxPages, paginas)
        case "3":
            paginas = clock(maxPages, paginas)
        case "4":
            paginas = sc(maxPages, paginas)
        case "5":
            paginas = nur(maxPages, paginas)

    print(f"Paginas em memoria: {paginas}")