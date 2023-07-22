import os
import threading

def create_large_file(file_path, desired_size_mb):
    # Função para criar um arquivo grande com o tamanho desejado em MB
    desired_size_bytes = desired_size_mb * 1024 * 1024  # Calcula o tamanho em bytes
    content = "A" * 1024  # Conteúdo do arquivo - 1024 caracteres "A"

    with open(file_path, 'wb') as file:
        bytes_written = 0
        while bytes_written < desired_size_bytes:
            # Garante que não escrevemos mais do que o tamanho desejado
            bytes_to_write = min(desired_size_bytes - bytes_written, len(content.encode()))
            file.write(content.encode()[:bytes_to_write])
            bytes_written += bytes_to_write

def create_files_in_threads(num_files, destination_directory, desired_size_mb):
    # Função principal para criar vários arquivos em threads
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)  # Verifica se o diretório de destino existe, caso não exista, cria-o

    num_threads = min(num_files, os.cpu_count())  # Número de threads será o mínimo entre o número de arquivos e o número de núcleos da CPU

    files_per_thread = num_files // num_threads  # Calcula quantos arquivos cada thread deve criar
    remainder_files = num_files % num_threads  # Calcula o resto de arquivos, que será distribuído para algumas threads adicionais

    threads = []
    for thread_number in range(num_threads):
        # Calcula o número de arquivos que a thread atual criará, considerando o resto
        num_files_for_thread = files_per_thread + 1 if thread_number < remainder_files else files_per_thread

        # Cria uma thread para chamar a função create_files com os parâmetros necessários
        thread = threading.Thread(target=create_files, args=(thread_number, destination_directory, num_files_for_thread, desired_size_mb))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # Aguarda a conclusão de todas as threads

    print(f"{num_files} arquivos criados em '{destination_directory}' com {desired_size_mb} MB cada.")

def create_files(thread_number, destination_directory, num_files_for_thread, desired_size_mb):
    # Função que será executada em cada thread para criar os arquivos
    for i in range(num_files_for_thread):
        file_path = os.path.join(destination_directory, f"arquivo_thread{thread_number}_file{i + 1}.txt")
        create_large_file(file_path, desired_size_mb)  # Chama a função para criar um arquivo grande no caminho especificado

if __name__ == "__main__":
    num_files_to_create = 5  # Número desejado de arquivos a serem criados
    destination_directory = "./arquivos_10mb"  # Diretório onde os arquivos serão criados
    desired_size_mb = 10  # Tamanho desejado de cada arquivo em MB

    create_files_in_threads(num_files_to_create, destination_directory, desired_size_mb)
