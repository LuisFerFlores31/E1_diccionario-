import os
import time
import psutil

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB

def test_algorithm(algorithm_name, file_path):
    initial_memory = get_memory_usage()
    start_time = time.time()
    
    if algorithm_name == "manber_myers":
        from manber_myers import suffix_array
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        SA = suffix_array(text)
    else:  # sais
        from sais import sais
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip() + '$'
        T = [ord(c) for c in text]
        SA = sais(T)
    
    end_time = time.time()
    peak_memory = get_memory_usage()
    
    return {
        'algorithm': algorithm_name,
        'file': os.path.basename(file_path),
        'file_size': os.path.getsize(file_path) / 1024,  # KB
        'time': end_time - start_time,
        'memory': peak_memory - initial_memory
    }

def print_summary(results):
    print("\n=== RESUMEN DE RESULTADOS ===")
    print("%-20s %-20s %-15s %-15s %-15s" % 
          ("Algoritmo", "Archivo", "Tamaño (KB)", "Tiempo (s)", "Memoria (MB)"))
    print("-" * 85)
    
    for r in results:
        print("%-20s %-20s %-15.2f %-15.2f %-15.2f" % 
              (r['algorithm'], r['file'][:20], r['file_size'], r['time'], r['memory']))

def main():
    algorithms = ['manber_myers', 'sais']
    books_dir = 'books'
    results = []
    
    for algo in algorithms:
        for book in os.listdir(books_dir):
            if book.endswith('.txt'):
                print(f"\nProbando {algo} con {book}...")
                file_path = os.path.join(books_dir, book)
                try:
                    result = test_algorithm(algo, file_path)
                    results.append(result)
                    print(f"Completado:")
                    print(f"  Algoritmo: {result['algorithm']}")
                    print(f"  Archivo: {result['file']}")
                    print(f"  Tamaño: {result['file_size']:.2f} KB")
                    print(f"  Tiempo: {result['time']:.2f} segundos")
                    print(f"  Memoria: {result['memory']:.2f} MB")
                except Exception as e:
                    print(f"Error en {algo} con {book}: {str(e)}")
    
    print_summary(results)

if __name__ == "__main__":
    main()