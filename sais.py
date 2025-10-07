import time
import sys

def getBuckets(T):
    count = {}
    buckets = {}
    for c in T:
        count[c] = count.get(c, 0) + 1
    start = 0
    for c in sorted(count.keys()):
        buckets[c] = (start, start + count[c])
        start += count[c]
    return buckets

def sais(T):
    if len(T) <= 1:
        return list(range(len(T)))
        
    t = ["_"] * len(T)
    t[len(T) - 1] = "S"
    
    for i in range(len(T) - 2, -1, -1):
        if T[i] == T[i + 1]:
            t[i] = t[i + 1]
        else:
            t[i] = "S" if T[i] < T[i + 1] else "L"
    
    buckets = getBuckets(T)
    count = {}
    SA = [-1] * len(T)
    LMS = {}
    end = None
    
    for i in range(1, len(T)):
        if t[i] == "S" and t[i - 1] == "L":
            revoffset = count[T[i]] = count.get(T[i], 0) + 1
            SA[buckets[T[i]][1] - revoffset] = i
            if end is not None:
                LMS[i] = end
            end = i

    LMS[len(T) - 1] = len(T) - 1
    count = {}
    
    for i in range(len(T)):
        if SA[i] > 0:
            if t[SA[i] - 1] == "L":
                symbol = T[SA[i] - 1]
                offset = count.get(symbol, 0)
                SA[buckets[symbol][0] + offset] = SA[i] - 1
                count[symbol] = offset + 1

    count = {}
    for i in range(len(T) - 1, -1, -1):
        if SA[i] > 0:
            if t[SA[i] - 1] == "S":
                symbol = T[SA[i] - 1]
                revoffset = count[symbol] = count.get(symbol, 0) + 1
                SA[buckets[symbol][1] - revoffset] = SA[i] - 1

    return SA

def main():
    if len(sys.argv) != 2:
        print("Uso: python sais.py <archivo_texto>")
        sys.exit(1)
        
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            text = file.read().strip() + '$'
            
        print(f"Procesando archivo: {sys.argv[1]}")
        print(f"Tamaño del texto: {len(text)} caracteres")
        
        T = [ord(c) for c in text]
        
        start_time = time.time()
        SA = sais(T)
        end_time = time.time()
        
        print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
        
        with open(f"{sys.argv[1]}_SA.txt", 'w') as f:
            f.write(','.join(map(str, SA)))
            
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {sys.argv[1]}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()