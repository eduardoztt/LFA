import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk


class SimuladorDeAutômato:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = {}
        self.estado_inicial = None
        self.estados_aceitacao = set()

    def adicionar_estado(self, estado, inicial=False, aceitacao=False):
        self.estados.add(estado)
        if inicial:
            self.estado_inicial = estado
        if aceitacao:
            self.estados_aceitacao.add(estado)

    def adicionar_transicao(self, de_estado, simbolo, para_estado):
        if de_estado not in self.transicoes:
            self.transicoes[de_estado] = {}
        if simbolo not in self.transicoes[de_estado]:
            self.transicoes[de_estado][simbolo] = set()
        self.transicoes[de_estado][simbolo].add(para_estado)

    def processar_entrada(self, entrada):
        estados_atuais = {self.estado_inicial}
        for simbolo in entrada:
            proximos_estados = set()
            for estado in estados_atuais:
                if estado in self.transicoes and simbolo in self.transicoes[estado]:
                    proximos_estados.update(self.transicoes[estado][simbolo])
            estados_atuais = proximos_estados
        return bool(estados_atuais & self.estados_aceitacao)


def gerar_automato_da_gramatica(regras_gramatica, simbolo_inicial):
    automato = SimuladorDeAutômato()
    for regra in regras_gramatica:
        esquerda, direita = regra.split("->")
        esquerda = esquerda.strip()
        automato.adicionar_estado(esquerda, inicial=(esquerda == simbolo_inicial))
        producoes = direita.split("|")
        for producao in producoes:
            producao = producao.strip()

            #epsilon & (cadeia vazia), marcar como estado de aceitação
            if producao == "&":
                automato.adicionar_estado(esquerda, aceitacao=True)

            elif len(producao) == 1:  # Somente terminal
                automato.adicionar_estado("final", aceitacao=True)
                automato.adicionar_transicao(esquerda, producao, "final")
            else:
                terminal, nao_terminal = producao[0], producao[1:]
                automato.adicionar_estado(nao_terminal)
                automato.adicionar_transicao(esquerda, terminal, nao_terminal)
    return automato


#parte grafica
class InterfaceSimulador:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Simulador de Gramática e Autômato Finito")

        self.frame_principal = tk.Frame(self.janela)
        self.frame_principal.pack(padx=10, pady=10)

        self.aba_gramatica_frame = tk.Frame(self.frame_principal)
        self.aba_gramatica_frame.grid(row=0, column=0, padx=10)

        self.entrada_gramatica_dica = tk.Label(self.aba_gramatica_frame, text=(
            "Formato da gramatica deve seguir as seguintes regras:\n\n\n"
            "1. Digite as produções no formato terminal e não-terminal ex: aA , bA , a , A, &\n"
            "2. Escreva os terminais minusculo e os não terminais maiusculo para melhor compreenção\n"
            "3. Use '->' para separar o estado das produções\n"
            "4. Use '|' para separar alternativas na produção.\n"
            "4. Use '&' para representar a cadeia vazia (ε)."
        ))
        self.entrada_gramatica_dica.grid(row=0, column=0, padx=5, pady=5)

        self.entrada_gramatica_label = tk.Label(self.aba_gramatica_frame, text="Digite a gramática regular:")
        self.entrada_gramatica_label.grid(row=1, column=0, padx=5, pady=5)

        self.entrada_gramatica = scrolledtext.ScrolledText(self.aba_gramatica_frame, width=50, height=10)
        self.entrada_gramatica.grid(row=2, column=0, padx=5, pady=5)

        self.entrada_simbolo_inicial_label = tk.Label(self.aba_gramatica_frame, text="Símbolo Inicial:")
        self.entrada_simbolo_inicial_label.grid(row=3, column=0, padx=5, pady=5)

        self.entrada_simbolo_inicial = tk.Entry(self.aba_gramatica_frame, width=30)
        self.entrada_simbolo_inicial.grid(row=4, column=0, padx=5, pady=5)

        self.botao_gerar_automato = tk.Button(self.aba_gramatica_frame, text="Gerar Autômato", command=self.gerar_automato)
        self.botao_gerar_automato.grid(row=5, column=0, pady=10)

        self.aba_teste_frame = tk.Frame(self.frame_principal)
        self.aba_teste_frame.grid(row=0, column=1, padx=10)

        self.entrada_strings_label = tk.Label(self.aba_teste_frame, text="Digite as strings (separadas por vírgula):")
        self.entrada_strings_label.grid(row=0, column=0, padx=5, pady=5)

        self.entrada_strings = tk.Entry(self.aba_teste_frame, width=50)
        self.entrada_strings.grid(row=1, column=0, padx=5, pady=5)

        self.botao_testar = tk.Button(self.aba_teste_frame, text="Testar Strings", command=self.testar_strings)
        self.botao_testar.grid(row=2, column=0, pady=10)

        self.resultados_label = tk.Label(self.aba_teste_frame, text="Resultados:")
        self.resultados_label.grid(row=3, column=0, padx=5, pady=5)

        self.resultado_texto = scrolledtext.ScrolledText(self.aba_teste_frame, width=50, height=10, state="disabled")
        self.resultado_texto.grid(row=4, column=0, padx=5, pady=5)


    def gerar_automato(self):
        texto_gramatica = self.entrada_gramatica.get("1.0", tk.END).strip()
        simbolo_inicial = self.entrada_simbolo_inicial.get().strip()

        if not texto_gramatica or not simbolo_inicial:
            messagebox.showerror("Erro", "Preencha todos os campos para gerar o autômato.")
            return

        regras_gramatica = texto_gramatica.splitlines()
        try:
            self.automato = gerar_automato_da_gramatica(regras_gramatica, simbolo_inicial)
            messagebox.showinfo("Sucesso", "Autômato gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o autômato: {e}")

    def testar_strings(self):
        if not hasattr(self, 'automato'):
            messagebox.showerror("Erro", "Primeiro, gere o autômato.")
            return

        strings_para_teste = self.entrada_strings.get().strip().split(",")
        resultados = []

        for string in strings_para_teste:
            string = string.strip()
            if self.automato.processar_entrada(string):
                resultados.append(f"'{string}' -> Aceita")
            else:
                resultados.append(f"'{string}' -> Rejeitada")

        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete("1.0", tk.END)
        self.resultado_texto.insert(tk.END, "\n".join(resultados))
        self.resultado_texto.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceSimulador(root)
    root.mainloop()
