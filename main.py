from itertools import cycle
from processo import Processo
from random import randint

maxPages = 10

def clock(n, ref_list):
    pages = [-1] * n  # Initialize memory slots with -1 (empty)
    idx = cycle((i, 1 << i) for i in range(n))  # Create a cyclic iterator for indexes and bits
    d = {}  # Dictionary to track the pages and their corresponding bits
    bits = 0  # Variable to store the bits

    for p in ref_list:
        if p.pageId in d:  # Page already in memory
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
    cache, time = [-1] * n, [-1] * n
    for i, x in enumerate(ref_list):
        idx = cache.index(x) if x.pageId in cache else time.index(min(time))
        cache[idx] = x
        time[idx] = i
    return cache

def fifo(n, ref_list):
    fList = []
    pIds = [p.pageId for p in ref_list]
    counter = 0
    for i in ref_list:
        if len(fList) < n and not i in fList:
            fList.append(i)
        else:
            if not i in fList:
                fList[counter] = i
                counter += 1
                if counter >= len(fList): counter = 0
    if ref_list == []:
        return [-1 for x in range(n)]
    while len(fList) < n:
        #endereco vazio
        fList.append(-1)

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

processos = []
for i in range(10):
    p = randint(1, maxPages)
    processos.append(Processo(p))
    print(processos[i].id)

if __name__ == '__main__':
    print("Escolha uma opção:")
    print("[1]FIFO\n[2]MRU\n[3]CLOCK\n[4]SC\n[5]NUR\n")
    match input():
        case "1":
            processos = fifo(maxPages, processos)
        case "2":
            processos = mru(maxPages, processos)
        case "3":
            processos = clock(maxPages, processos)
        case "4":
            processos = sc(maxPages, processos)
        case "5":
            pass

    for p in processos:
        print(p.id)
