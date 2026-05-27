import pandas as pd
import requests
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

#variaveis
# Armazenará o DataFrame processado na memória para ser salvo depois
df_resultado = None 

#logica

def consultar_cep(cep):
    cep_limpo = str(cep).strip().replace('-', '').replace('.', '')
    
    if len(cep_limpo) != 8:
        return "CEP Inválido", "", "", ""
    
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" in dados:
                return "Não Encontrado", "", "", ""
            
            return (
                dados.get("logradouro", ""),
                dados.get("bairro", ""),
                dados.get("localidade", ""),
                dados.get("uf", "")
            )
        else:
            return "Erro na consulta", "", "", ""
    except Exception as e:
        return f"Erro de Conexão: {e}", "", "", ""


def executar_rpa(caminho_arquivo, label_status, barra_progresso, botao_iniciar, botao_baixar):
    global df_resultado
    try:
        # Oculta o botão de baixar caso uma nova consulta seja iniciada
        botao_baixar.pack_forget()
        
        # 1. Ler a planilha Excel original
        df = pd.read_excel(caminho_arquivo)
        
        # Validar se a coluna 'CEP' existe
        if "CEP" not in df.columns:
            messagebox.showerror("Erro", "A planilha selecionada não contém a coluna 'CEP'.")
            botao_iniciar.config(state="normal")
            return

        # Criar colunas novas caso não existam
        for coluna in ["Logradouro", "Bairro", "Cidade", "Estado"]:
            if coluna not in df.columns:
                df[coluna] = ""

        total_linhas = len(df)
        barra_progresso["max"] = total_linhas

        # 2. Loop para processar linha por linha 
        for index, linha in df.iterrows():
            cep_atual = linha["CEP"]
            
            # Atualiza o status na interface gráfica
            label_status.config(text=f"🔎 Consultando CEP: {cep_atual} ({index + 1}/{total_linhas})")
            barra_progresso["value"] = index + 1
            root.update_idletasks() # Força a atualização visual
            
            # Executa a busca
            logradouro, bairro, cidade, uf = consultar_cep(cep_atual)
            
            # Preenche o DataFrame temporário
            df.at[index, "Logradouro"] = logradouro
            df.at[index, "Bairro"] = bairro
            df.at[index, "Cidade"] = cidade
            df.at[index, "Estado"] = uf
            
            time.sleep(0.5)
        
        # Guarda o resultado final na variável global sem alterar o arquivo original
        df_resultado = df
        
        label_status.config(text="✅ Processo concluído! Clique abaixo para baixar.")
        messagebox.showinfo("Sucesso", "Consulta concluída! O arquivo está pronto para ser baixado.")
        
        # Mostra o botão de download na interface
        botao_baixar.pack(fill="x", ipady=5, pady=(5, 0))
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado:\n{e}")
        label_status.config(text="❌ O processo falhou.")
    
    finally:
        # Reativa o botão de iniciar após o término ou erro
        botao_iniciar.config(state="normal")


#interface 

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha de CEPs",
        filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
    )
    if caminho:
        entry_caminho.delete(0, tk.END)
        entry_caminho.insert(0, caminho)
        btn_iniciar.config(state="normal")


def iniciar_thread_rpa():
    caminho = entry_caminho.get()
    if not caminho:
        messagebox.showwarning("Aviso", "Por favor, selecione um arquivo Excel primeiro.")
        return
    
    btn_iniciar.config(state="disabled")
    
    # Passamos o btn_baixar também para que a Thread possa torná-lo visível no final
    thread = threading.Thread(
        target=executar_rpa, 
        args=(caminho, lbl_status, progress_bar, btn_iniciar, btn_baixar)
    )
    thread.daemon = True
    thread.start()


def baixar_documento():
    global df_resultado
    if df_resultado is not None:
        # Abre a caixa de diálogo para escolher onde salvar o novo arquivo
        caminho_salvar = filedialog.asksaveasfilename(
            title="Salvar planilha consultada",
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")],
            initialfile="planilha_ceps_consultados.xlsx"
        )
        
        if caminho_salvar:
            try:
                # Salva a cópia com as informações novas
                df_resultado.to_excel(caminho_salvar, index=False)
                messagebox.showinfo("Salvo", "Arquivo salvo com sucesso!")
                btn_baixar.pack_forget() # Oculta o botão após salvar com sucesso
                lbl_status.config(text="Aguardando início...")
                progress_bar["value"] = 0
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")


#janela

root = tk.Tk()
root.title("RPA - Validador de CEP")
root.geometry("550x300")  # Aumentado levemente o tamanho para acomodar o novo botão confortavelmente
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

#front

lbl_instrucao = ttk.Label(frame, text="Selecione a planilha Excel (.xlsx) contendo a coluna 'CEP':", font=("Arial", 10, "bold"))
lbl_instrucao.pack(anchor="w", pady=(0, 10))

frame_arquivo = ttk.Frame(frame)
frame_arquivo.pack(fill="x", pady=(0, 15))

entry_caminho = ttk.Entry(frame_arquivo, font=("Arial", 10))
entry_caminho.pack(side="left", fill="x", expand=True, padx=(0, 10))

btn_procurar = ttk.Button(frame_arquivo, text="Procurar...", command=selecionar_arquivo)
btn_procurar.pack(side="right")

progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
progress_bar.pack(fill="x", pady=(10, 5))

lbl_status = ttk.Label(frame, text="Aguardando início...", font=("Arial", 9, "italic"), foreground="gray")
lbl_status.pack(anchor="w", pady=(0, 15))

btn_iniciar = ttk.Button(frame, text="🚀 Iniciar Consulta", command=iniciar_thread_rpa, state="disabled")
btn_iniciar.pack(fill="x", ipady=5)

#botão baixar
btn_baixar = ttk.Button(frame, text="📥 Baixar Documento", command=baixar_documento)

root.mainloop()