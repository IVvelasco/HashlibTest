import hashlib
import json
from pathlib import Path
from datetime import datetime
from tkinter import Tk, Label, Button, filedialog, Text, messagebox
from tkinter import scrolledtext

class VerificadorIntegridade:
    def __init__(self, nome_json="hashes.json"):
        self.nome_json = nome_json
        self.dados = self._carregar_json()
    
    def _carregar_json(self):
        """Carrega dados de hashes existentes ou cria novo."""
        if Path(self.nome_json).exists():
            with open(self.nome_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _salvar_json(self):
        """Persiste dados em JSON."""
        with open(self.nome_json, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, indent=2, ensure_ascii=False)
    
    def calcular_hash(self, caminho_arquivo):
        """Calcula SHA-256 em chunks (eficiente para arquivos grandes)."""
        sha256 = hashlib.sha256()
        tamanho_chunk = 8192
        
        try:
            with open(caminho_arquivo, 'rb') as f:
                while True:
                    chunk = f.read(tamanho_chunk)
                    if not chunk:
                        break
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None
    
    def salvar_hashes(self, caminho_arquivo):
        """Armazena hash + metadados em JSON."""
        arquivo = Path(caminho_arquivo)
        
        if not arquivo.exists():
            return {"status": "erro", "mensagem": "Arquivo não encontrado"}
        
        hash_atual = self.calcular_hash(caminho_arquivo)
        
        self.dados[arquivo.name] = {
            "caminho": str(arquivo),
            "hash": hash_atual,
            "tamanho_bytes": arquivo.stat().st_size,
            "data_criacao": datetime.now().isoformat()
        }
        
        self._salvar_json()
        return {
            "status": "sucesso",
            "mensagem": f"Hash salvo para {arquivo.name}",
            "hash": hash_atual
        }
    
    def verificar_integridade(self, caminho_arquivo):
        """Compara hash atual com o armazenado."""
        arquivo = Path(caminho_arquivo)
        
        if arquivo.name not in self.dados:
            return {
                "status": "nao_encontrado",
                "mensagem": "Arquivo não tem hash registrado"
            }
        
        hash_armazenado = self.dados[arquivo.name]["hash"]
        hash_atual = self.calcular_hash(caminho_arquivo)
        
        if hash_armazenado == hash_atual:
            return {
                "status": "integro",
                "mensagem": " Arquivo íntegro – sem alterações!",
                "hash": hash_atual
            }
        else:
            return {
                "status": "alterado",
                "mensagem": " AVISO: Arquivo foi alterado!",
                "hash_esperado": hash_armazenado,
                "hash_atual": hash_atual
            }


class InterfaceVerificador:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title(" Verificador de Integridade de Arquivos")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)
        
        self.verificador = VerificadorIntegridade()
        self.caminho_selecionado = None
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Monta os componentes da interface."""
        # Título
        titulo = Label(
            self.janela,
            text=" Verificador de Integridade",
            font=("Arial", 16, "bold"),
            fg="#2E86AB"
        )
        titulo.pack(pady=10)
        
        # Botão selecionar arquivo
        self.btn_selecionar = Button(
            self.janela,
            text="Selecionar Arquivo",
            command=self.selecionar_arquivo,
            bg="#F18F01",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )
        self.btn_selecionar.pack(pady=5)
        
        # Label para mostrar arquivo selecionado
        self.label_arquivo = Label(
            self.janela,
            text="Nenhum arquivo selecionado",
            font=("Arial", 9),
            fg="#555"
        )
        self.label_arquivo.pack(pady=5)
        
        # Frame com botões de ação
        frame_botoes = __import__('tkinter').Frame(self.janela)
        frame_botoes.pack(pady=10)
        
        self.btn_salvar = Button(
            frame_botoes,
            text=" Salvar Hash",
            command=self.salvar_hash,
            bg="#06A77D",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )
        self.btn_salvar.pack(side="left", padx=5)
        
        self.btn_verificar = Button(
            frame_botoes,
            text="Verificar Integridade",
            command=self.verificar_integridade,
            bg="#008F13",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        )
        self.btn_verificar.pack(side="left", padx=5)
        
        # Área de resultado
        Label(
            self.janela,
            text="Resultado:",
            font=("Arial", 10, "bold"),
            fg="#2E86AB"
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.resultado_text = scrolledtext.ScrolledText(
            self.janela,
            height=12,
            width=70,
            font=("Courier", 9),
            bg="#F5F5F5",
            fg="#333"
        )
        self.resultado_text.pack(padx=20, pady=10)
    
    def selecionar_arquivo(self):
        """Dialog para escolher arquivo."""
        caminho = filedialog.askopenfilename(
            title="Escolha um arquivo",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        
        if caminho:
            self.caminho_selecionado = caminho
            arquivo = Path(caminho).name
            self.label_arquivo.config(
                text=f" {arquivo}",
                fg="#06A77D"
            )
    
    def salvar_hash(self):
        """Salva hash do arquivo selecionado."""
        if not self.caminho_selecionado:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro!")
            return
        
        resultado = self.verificador.salvar_hashes(self.caminho_selecionado)
        self._exibir_resultado(resultado)
    
    def verificar_integridade(self):
        """Verifica integridade do arquivo."""
        if not self.caminho_selecionado:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro!")
            return
        
        resultado = self.verificador.verificar_integridade(self.caminho_selecionado)
        self._exibir_resultado(resultado)
    
    def _exibir_resultado(self, resultado):
        """Mostra resultado formatado na área de texto."""
        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, "end")
        
        texto = f"""

{'-'* 30}
STATUS: {resultado.get('status', 'desconhecido').upper()}
{'-'* 30}

{'-'* 30}
{resultado.get('mensagem', '')}
{'-'* 30}

"""
        
        if 'hash' in resultado:
            texto += f"Hash SHA-256: {resultado['hash']}\n"
        
        if 'hash_esperado' in resultado:
            texto += f"\n{'-'* 60}\n" 
            texto += f"\n Hash Esperado:  {resultado['hash_esperado']}"
            texto += f"\n{'-'* 60}\n" 
            texto += f"\n Hash Atual:     {resultado['hash_atual']}"
            texto += f"\n{'-'* 60}\n" 

        
        self.resultado_text.insert(1.0, texto)
        self.resultado_text.config(state="disabled")


if __name__ == "__main__":
    janela = Tk()
    interface = InterfaceVerificador(janela)
    janela.mainloop()
