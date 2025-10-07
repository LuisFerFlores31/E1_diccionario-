import time
import sys

class SubstrRank:
    def __init__(self, left_rank=0, right_rank=0, index=0):
        self.left_rank = left_rank
        self.right_rank = right_rank
        self.index = index

def make_ranks(substr_rank, n):
    r = 0
    rank = [-1] * n
    rank[substr_rank[0].index] = r
    for i in range(1, n):
        if (substr_rank[i].left_rank != substr_rank[i-1].left_rank or
            substr_rank[i].right_rank != substr_rank[i-1].right_rank):
            r += 1
        rank[substr_rank[i].index] = r
    return rank

def suffix_array(T):
    n = len(T)
    substr_rank = []

    for i in range(n):
        substr_rank.append(SubstrRank(ord(T[i]), ord(T[i + 1]) if i < n-1 else 0, i))

    substr_rank.sort(key=lambda sr: (sr.left_rank, sr.right_rank))

    l = 2
    while l < n:
        rank = make_ranks(substr_rank, n)

        for i in range(n):
            substr_rank[i].left_rank = rank[i]
            substr_rank[i].right_rank = rank[i+l] if i+l < n else 0
            substr_rank[i].index = i
        l *= 2

        substr_rank.sort(key=lambda sr: (sr.left_rank, sr.right_rank))

    SA = [substr_rank[i].index for i in range(n)]

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
        print("Uso: python manber_myers.py <archivo_texto>")
        sys.exit(1)
        
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            text = file.read().strip()
            
        print(f"Procesando archivo: {sys.argv[1]}")
        print(f"Tamaño del texto: {len(text)} caracteres")
        
        start_time = time.time()
        SA = suffix_array(text)
        end_time = time.time()
        
        print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
        
        # Agregar búsqueda
        pattern = input("Ingrese el patrón a buscar: ")
        positions = fm_search(pattern, text + '$', SA)
        
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