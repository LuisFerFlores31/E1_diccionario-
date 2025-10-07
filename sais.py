import time
import sys

def getBuckets(T):
    count = {}
    buckets = {}
    for c in T:
        count[c] = count.get(c, 0) + 1
    start = 0
    for c in sorted(count.keys()):
        buckets[c] = [start, start + count[c]]  # Solo cambio: usar lista en vez de tupla
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
    count.clear()  # Cambio: usar clear() en vez de reasignar
    
    for i in range(len(T)):
        if SA[i] > 0:
            if t[SA[i] - 1] == "L":
                symbol = T[SA[i] - 1]
                offset = count.get(symbol, 0)
                SA[buckets[symbol][0] + offset] = SA[i] - 1
                count[symbol] = offset + 1

    count.clear()  # Cambio: usar clear() en vez de reasignar
    for i in range(len(T) - 1, -1, -1):
        if SA[i] > 0:
            if t[SA[i] - 1] == "S":
                symbol = T[SA[i] - 1]
                revoffset = count[symbol] = count.get(symbol, 0) + 1
                SA[buckets[symbol][1] - revoffset] = SA[i] - 1

    return SA

def get_bwt(text, sa):
    """Construye la BWT usando el arreglo de sufijos"""
    bwt = []
    for i in sa:
        if i == 0:
            bwt.append(text[-1])
        else:
            bwt.append(text[i - 1])
    return ''.join(bwt)

def get_first_column(bwt):
    """Obtiene la primera columna ordenando la BWT"""
    return ''.join(sorted(bwt))

def get_counts(bwt):
    """Calcula la tabla C (cuenta de caracteres menores)"""
    counts = {}
    total = 0
    # Primero contamos frecuencias
    for c in sorted(set(bwt)):
        counts[c] = bwt.count(c)
    # Luego calculamos las posiciones acumuladas
    running_sum = 0
    final_counts = {}
    for c in sorted(counts.keys()):
        final_counts[c] = running_sum
        running_sum += counts[c]
    return final_counts

def get_occ(bwt, char, pos):
    """Cuenta ocurrencias del carácter hasta la posición dada"""
    return bwt[:pos].count(char)

def fm_search(pattern, text, sa):
    """Busca un patrón usando FM-Index"""
    bwt = get_bwt(text, sa)
    first_col = get_first_column(bwt)
    counts = get_counts(bwt)
    
    # Inicializar rango de búsqueda
    start = 0
    end = len(bwt)
    
    # Buscar el patrón de derecha a izquierda
    for c in reversed(pattern):
        if c not in counts:
            return []
        
        # Actualizar rango usando LF-mapping
        start = counts[c] + get_occ(bwt, c, start)
        end = counts[c] + get_occ(bwt, c, end)
        
        if start >= end:
            return []
    
    # Convertir posiciones BWT a posiciones en el texto original usando SA
    return [sa[i] for i in range(start, end)]

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
        
        # Ejemplo de búsqueda
        pattern = input("Ingrese el patrón a buscar: ")
        positions = fm_search(pattern, text, SA)
        
        if positions:
            print(f"Patrón '{pattern}' encontrado en las posiciones: {positions}")
        else:
            print(f"Patrón '{pattern}' no encontrado en el texto")
        
        with open(f"{sys.argv[1]}_SA.txt", 'w') as f:
            f.write(','.join(map(str, SA)))
            
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {sys.argv[1]}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()