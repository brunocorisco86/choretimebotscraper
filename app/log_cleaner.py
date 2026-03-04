import os
import time
import logging

# Configuração básica de log para o próprio script de limpeza
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_old_logs(log_dir="logs", days_to_keep=7):
    """
    Remove arquivos de log com extensão .log ou .txt que foram modificados 
    há mais de 'days_to_keep' dias.
    """
    # Se o diretório for relativo, assume que está na raiz do projeto
    if not os.path.isabs(log_dir):
        # Tenta encontrar o diretório logs na raiz do projeto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        log_dir = os.path.join(project_root, log_dir)

    if not os.path.exists(log_dir):
        logging.warning(f"Diretório de logs não encontrado: {log_dir}")
        return

    now = time.time()
    cutoff = now - (days_to_keep * 86400) # 86400 segundos em um dia
    
    files_removed = 0
    
    try:
        logging.info(f"Iniciando limpeza de logs em: {log_dir} (Mantendo últimos {days_to_keep} dias)")
        
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)
            
            # Verifica se é um arquivo e se tem a extensão de log
            if os.path.isfile(file_path) and (filename.endswith(".log") or filename.endswith(".txt")):
                file_mtime = os.path.getmtime(file_path)
                
                if file_mtime < cutoff:
                    os.remove(file_path)
                    logging.info(f"Arquivo removido: {filename}")
                    files_removed += 1
        
        logging.info(f"Limpeza concluída. Total de arquivos removidos: {files_removed}")
        
    except Exception as e:
        logging.error(f"Erro durante a limpeza de logs: {e}")

if __name__ == "__main__":
    # Pode ser chamado diretamente: python app/log_cleaner.py
    clean_old_logs()
