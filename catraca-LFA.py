import tkinter as tk

class SimuladorDeElevador:
    def __init__(self, total_andares):
        self.total_andares = total_andares
        self.estado_atual = "PortaAberta_Andar0"   #Estado inicial, nesse caso o terreo ou andar
        self.gramatica_arvore = []  # lista de produções

    def transitar(self, entrada):
        andar_atual = int(self.estado_atual.split("_")[-1].replace("Andar", ""))

        transicao = ""  # guarda a transição realizada
        producao = ""  #e guarda a produção utilizada

        if "PortaAberta" in self.estado_atual:
            if entrada == "F":  #(P -> fA)
                self.estado_atual = f"PortaFechada_Andar{andar_atual}"
                transicao = "Fechar Porta"
                producao = "P -> fA"  
                self.atualizar_arvore("P", "fA")
            elif entrada == "A":  # erro porta ja ta aberta
                return "Erro: Porta já está aberta.", ""
            else:
                return "Erro: Movimento inválido.", ""

        elif "PortaFechada" in self.estado_atual:
            if entrada == "S":  #(A -> sA)
                if andar_atual < self.total_andares - 1:
                    self.estado_atual = f"PortaFechada_Andar{andar_atual + 1}"
                    transicao = "Subir"
                    producao = "A -> sA"  
                    self.atualizar_arvore("A", "sA")
                else:
                    return "Erro: Não é possível subir, você já está no último andar.", ""
            elif entrada == "D":  #(A -> dA) 
                if andar_atual > 0:
                    self.estado_atual = f"PortaFechada_Andar{andar_atual - 1}"
                    transicao = "Descer"
                    producao = "A -> dA" 
                    self.atualizar_arvore("A", "dA")
                else:
                    return "Erro: Não é possível descer, você já está no térreo.", ""
            elif entrada == "A":  #(A -> aF)
                self.estado_atual = f"PortaAberta_Andar{andar_atual}"
                transicao = "Abrir Porta"
                producao = "A -> aF" 
                self.atualizar_arvore("A", "aF")
            else:
                return "Erro: Movimento inválido.", ""

        return transicao, producao  #retorna a transição e produção

    def obter_estado(self):
        return self.estado_atual

    def obter_estado_descritivo(self):
        andar_atual = int(self.estado_atual.split("_")[-1].replace("Andar", ""))
        if "PortaAberta" in self.estado_atual:
            return f"Porta aberta no andar: {andar_atual}"
        elif "PortaFechada" in self.estado_atual:
            return f"Porta fechada no andar: {andar_atual}"

    def atualizar_arvore(self, producao_atual, producao_resultante):
        self.gramatica_arvore.append((producao_atual, producao_resultante))
        print("Árvore de Produções Atualizada:", self.gramatica_arvore)


class InterfaceElevador:
    def __init__(self, root, elevador):
        self.elevador = elevador
        
        root.title("Simulador de Elevador")
        root.geometry("700x1000")
        
        
       
        self.frame_elevador = tk.Frame(root, bg="gray", width=200, height=300)
        self.frame_elevador.pack(pady=20)
        self.frame_elevador.pack_propagate(False)

        self.andar_label = tk.Label(self.frame_elevador, text="Andar 0", font=("Arial", 24), bg="gray", fg="white")
        self.andar_label.pack(pady=10)

        self.porta_label = tk.Label(self.frame_elevador, text="Porta Aberta", font=("Arial", 14), bg="gray", fg="white")
        self.porta_label.pack(pady=10)

        self.porta_visual = tk.Canvas(self.frame_elevador, width=150, height=150, bg="white")
        self.porta_visual.pack(pady=20)
        self.desenhar_porta("aberta")

        
        self.frame_botoes = tk.Frame(root)
        self.frame_botoes.pack(pady=10)
        
        self.botao_subir = tk.Button(self.frame_botoes, text="Subir", command=self.subir, width=10)
        self.botao_subir.grid(row=0, column=0, padx=5)
        
        self.botao_descer = tk.Button(self.frame_botoes, text="Descer", command=self.descer, width=10)
        self.botao_descer.grid(row=0, column=1, padx=5)
        
        self.botao_abrir = tk.Button(self.frame_botoes, text="Abrir Porta", command=self.abrir_porta, width=10)
        self.botao_abrir.grid(row=1, column=0, pady=5)
        
        self.botao_fechar = tk.Button(self.frame_botoes, text="Fechar Porta", command=self.fechar_porta, width=10)
        self.botao_fechar.grid(row=1, column=1, pady=5)

      
        self.historico_label = tk.Label(root, text="Histórico de ações:", font=("Arial", 12))
        self.historico_label.pack(pady=5)

        self.historico_text = tk.Text(root, state="disabled", height=10, width=50)
        self.historico_text.pack(pady=10)

        
        self.frame_gramatica = tk.Frame(root)
        self.frame_gramatica.pack(pady=10)

        
        self.gramatica_label = tk.Label(
            self.frame_gramatica, 
            text=( 
                "Gramática:\n"
                "P -> fA\n"
                "A -> sA | dA | aF\n"
                "F -> &"
            ),
            font=("Arial", 10), 
            justify="left"
        )
        self.gramatica_label.grid(row=0, column=0, padx=5)

       
        self.gramatica_label_explicacao = tk.Label(
            self.frame_gramatica, 
            text=( 
                "Explicação:\n"
                "P = Parado\n"
                "A = Movimento\n"
                "F = FIM\n"
                "s = Subir\n"
                "d = Descer\n"
                "a = Abrir Porta\n"
                "f = Fechar Porta\n"
            ),
            font=("Arial", 10), 
            justify="left"
        )
        self.gramatica_label_explicacao.grid(row=0, column=1, padx=5)

      
        self.frame_arvore = tk.Frame(root)
        self.frame_arvore.pack(pady=10)

        self.arvore_label = tk.Label(self.frame_arvore, text="Árvore de Produções", font=("Arial", 14))
        self.arvore_label.grid(row=0, column=0, padx=5)

        self.arvore_text = tk.Text(self.frame_arvore, height=10, width=50, wrap=tk.WORD)
        self.arvore_text.grid(row=1, column=0, padx=5)

    def desenhar_porta(self, estado):
        self.porta_visual.delete("all")
        if estado == "aberta":
            self.porta_visual.create_rectangle(10, 10, 70, 140, fill="lightgreen", outline="black")
            self.porta_visual.create_rectangle(80, 10, 150, 140, fill="lightgreen", outline="black")
        elif estado == "fechada":
            self.porta_visual.create_rectangle(10, 10, 150, 140, fill="gray", outline="black")


    def exibir_estado(self):
        estado = self.elevador.obter_estado_descritivo()
        self.andar_label.config(text=f"Andar: {estado.split(' ')[-1]}")
        porta_estado = "Aberta" if "Aberta" in estado else "Fechada"
        self.porta_label.config(text=f"Porta {porta_estado}")

    def exibir_acao(self, transicao, producao):
        self.historico_text.config(state="normal")
        self.historico_text.insert(tk.END, f"{transicao} ({producao})\n")
        self.historico_text.config(state="disabled")

    def exibir_arvore(self):
        self.arvore_text.config(state="normal")
        self.arvore_text.delete(1.0, tk.END)
        for producao_atual, producao_resultante in self.elevador.gramatica_arvore:
            self.arvore_text.insert(tk.END, f"{producao_atual} -> {producao_resultante}\n")
        self.arvore_text.config(state="disabled")


    #chama a função transitar com a produção S = (A -> sA)
    def subir(self):
        transicao, producao = self.elevador.transitar("S")
        self.exibir_estado()
        self.exibir_acao(transicao, producao)
        self.exibir_arvore()


    #chama a função transitar com a produção D = (A -> dA)
    def descer(self):
        transicao, producao = self.elevador.transitar("D")
        self.exibir_estado()
        self.exibir_acao(transicao, producao)
        self.exibir_arvore()


     #chama a função transitar com a produção A = (A -> aP)
    def abrir_porta(self):
        transicao, producao = self.elevador.transitar("A")
        if "Abrir Porta" in transicao:
            self.desenhar_porta("aberta")
        self.exibir_estado()
        self.exibir_acao(transicao, producao)
        self.exibir_arvore()



     #chama a função transitar com a produção F = (P -> fA)
    def fechar_porta(self):
        transicao, producao = self.elevador.transitar("F")
        if "Fechar Porta" in transicao:
            self.desenhar_porta("fechada")
        self.exibir_estado()
        self.exibir_acao(transicao, producao)
        self.exibir_arvore()
        

if __name__ == "__main__":
    elevador = SimuladorDeElevador(total_andares=5)
    root = tk.Tk()
    interface = InterfaceElevador(root, elevador)
    root.mainloop()