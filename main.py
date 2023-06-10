from itertools import cycle
from processo import Processo

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

def lru(n, ref_list):
    cache, time = [-1] * n, [-1] * n
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
        else:
            if not i in fList:
                fList[counter] = i
                counter += 1
                if counter >= len(fList): counter = 0
    if ref_list == []:
        return [-1 for x in range(n)]
    while len(fList) < n:
        fList.append(-1)
    return fList

processos = []
for i in range(10):
    p = Processo()
    processos.append(p)

for processo in processos:
    print(processo.id)

if __name__ == '__main__':
    print("Escolha uma opção:")
    print("[1]FIFO\n[2]NUR\n[3]CLOCK\n[4]SC\n[5]MRU\n")
    match input():
        case "1":
            processos = fifo(3, processos)
        case "2":
            processos = lru(3, processos)
        case "3":
            processos = clock(3, processos)
        case "4":
            pass
        case "5":
            pass

    for processo in processos:
        print(processo.id)