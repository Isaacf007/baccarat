import random
import colorama
import os
from typing import List, Tuple

# Inicializa o módulo colorama para exibir cores no terminal
colorama.init()
colorama.just_fix_windows_console()

class BaccaratGame:
    # Constantes: Definimos as cartas, naipes e valores para o jogo.
    SIMBOLOS = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
    NAIPES = ['♥️', '♠️', '♦️', '♣️']
    VALORES = {symbol: min(i, 10) for i, symbol in enumerate(SIMBOLOS, 1)}

    def __init__(self):
        # Inicializa o jogo, cria o baralho e define saldo e pontuação.
        self.baralho = self.criar_baralho()  # Cria o baralho de cartas.
        self.saldo = 1000  # O saldo inicial do jogador.
        self.nome = ''  # Nome do jogador, será pedido no início do jogo.
        self.pontuacao_maxima = 0  # Pontuação máxima registrada durante o jogo.

    def criar_baralho(self) -> List[str]:
        # Cria um baralho de 52 cartas combinando símbolos e naipes.
        return [simbolo + naipe for simbolo in self.SIMBOLOS for naipe in self.NAIPES]

    def formatar_carta(self, simbolo: str, naipe: str) -> str:
        # Formata uma carta para exibição com as cores adequadas.
        fundo = colorama.Back.WHITE
        cor = colorama.Fore.RED if naipe in ['♥️', '♦️'] else colorama.Fore.BLACK
        return fundo + cor + simbolo + naipe + ' ' + colorama.Style.RESET_ALL

    def exibir_baralho(self) -> None:
        # Exibe o baralho completo com todas as cartas e seus naipes.
        print("BEM VINDO AO BACCARAT!!! ESSE SERÁ O BARALHO UTILIZADO:")
        for naipe in self.NAIPES:
            print((colorama.Back.WHITE + '    ' + colorama.Style.RESET_ALL + '   ') * len(self.SIMBOLOS))
            for simbolo in self.SIMBOLOS:
                print(self.formatar_carta(simbolo, naipe), end='   ')
            print()
            print((colorama.Back.WHITE + '    ' + colorama.Style.RESET_ALL + '   ') * len(self.SIMBOLOS))
            print('\n')

    def exibir_cartas(self, cartas: List[str], quem: str, mensagem_terceira_carta: str = '') -> None:
        # Exibe as cartas de um jogador ou da banca no formato adequado.
        cartas_por_naipe = {naipe: [] for naipe in self.NAIPES}
        for carta in cartas:
            simbolo = carta[:-2]
            naipe = carta[-2:]
            cartas_por_naipe[naipe].append(simbolo)

        print(f"\nCartas do {quem}:")
        linha_carta = (colorama.Back.WHITE + '    ' + colorama.Style.RESET_ALL) * len(self.SIMBOLOS)
        print(linha_carta)
        for simbolo in self.SIMBOLOS:
            for naipe in self.NAIPES:
                if simbolo in cartas_por_naipe[naipe]:
                    print(self.formatar_carta(simbolo, naipe), end='   ')
        print()
        print(linha_carta)
        if mensagem_terceira_carta:
            print(mensagem_terceira_carta)  # Exibe a mensagem caso o jogador ou a banca tenha puxado uma terceira carta.
        print()

    def valor_da_carta(self, carta: str) -> int:
        # Retorna o valor de uma carta. Cartas de 2 a 9 valem seu número, e J, Q, K valem 10.
        simbolo = carta[:-2]
        return self.VALORES[simbolo]

    def puxar_cartas(self, num_cartas: int) -> List[str]:
        # Puxa um número específico de cartas aleatórias do baralho.
        random.shuffle(self.baralho)
        return [self.baralho.pop() for _ in range(num_cartas)]

    def calcular_pontuacao(self, cartas: List[str]) -> int:
        # Calcula a pontuação da mão, que é a soma dos valores das cartas % 10.
        return sum(self.valor_da_carta(carta) for carta in cartas) % 10

    def verificar_terceira_carta(self, cartas: List[str], quem: str) -> str:
        # Verifica se o jogador ou a banca deve puxar uma terceira carta.
        pontuacao_atual = self.calcular_pontuacao(cartas)
        if pontuacao_atual <= 5:
            nova_carta = self.puxar_cartas(1)[0]
            cartas.append(nova_carta)
            return (f"\nO {quem} puxou uma nova carta pois a soma inicial ({pontuacao_atual}) é menor ou igual a 5.\n"
                    f"Terceira carta puxada: {self.formatar_carta(nova_carta[:-2], nova_carta[-2:])}")
        return ''  # Retorna uma mensagem vazia se não puxou uma terceira carta.

    def ler_ranking(self) -> List[Tuple[str, int]]:
        # Lê o ranking de jogadores a partir de um arquivo de texto (se existir).
        ranking = []
        if os.path.exists('ranking.txt'):
            with open('ranking.txt', 'r') as file:
                for linha in file:
                    nome, pontos = linha.strip().split(': ')
                    pontos = int(pontos.split(' pontos')[0])
                    ranking.append((nome, pontos))
        return ranking

    def atualizar_ranking(self) -> None:
        # Atualiza o ranking de jogadores, salvando no arquivo.
        ranking = self.ler_ranking()
        jogador_encontrado = False

        # Atualiza a pontuação do jogador ou adiciona um novo jogador ao ranking.
        for i, (nome, pontos) in enumerate(ranking):
            if nome == self.nome:
                jogador_encontrado = True
                if self.saldo > pontos:
                    ranking[i] = (self.nome, self.saldo)
                break

        if not jogador_encontrado:
            ranking.append((self.nome, self.saldo))

        # Ordena o ranking de forma decrescente com base na pontuação.
        ranking.sort(key=lambda x: x[1], reverse=True)

        # Salva o ranking no arquivo.
        with open('ranking.txt', 'w') as file:
            for nome, pontos in ranking:
                file.write(f"{nome}: {pontos} pontos\n")

    def validar_aposta(self, valor_da_aposta: int) -> bool:
        # Verifica se o jogador tem saldo suficiente para a aposta.
        return valor_da_aposta <= self.saldo

    def processar_resultado(self, aposta: int, valor_da_aposta: int, mao_do_player: int, mao_da_banca: int) -> None:
        # Verifica se o jogador apostou na Player ou Banca.
        if aposta == 1:  # Player
            if mao_do_player > mao_da_banca:
                self.saldo += valor_da_aposta  # O jogador ganha o valor apostado.
                print(f"Você venceu! Sua aposta de {valor_da_aposta} foi paga.")
            elif mao_do_player < mao_da_banca:
                self.saldo -= valor_da_aposta  # O jogador perde o valor apostado.
                print(f"Você perdeu! A Banca venceu. Você perdeu {valor_da_aposta}.")
            else:
                print("Empate! Nenhuma alteração no saldo.")
        
        elif aposta == 2:  # Banca
            if mao_da_banca > mao_do_player:
                self.saldo += valor_da_aposta  # O jogador ganha o valor apostado.
                print(f"Você venceu! Sua aposta de {valor_da_aposta} foi paga.")
            elif mao_da_banca < mao_do_player:
                self.saldo -= valor_da_aposta  # O jogador perde o valor apostado.
                print(f"Você perdeu! O Player venceu. Você perdeu {valor_da_aposta}.")
            else:
                print("Empate! Nenhuma alteração no saldo.")
        
        elif aposta == 3:  # Empate
            if mao_do_player == mao_da_banca:
                self.saldo += valor_da_aposta * 8  # Empate paga 8x a aposta.
                print(f"Empate! Você ganhou 8x o valor da aposta. Você recebeu {valor_da_aposta * 8}.")
            else:
                self.saldo -= valor_da_aposta  # O jogador perde o valor apostado.
                print(f"Você perdeu! Não houve empate. Você perdeu {valor_da_aposta}.")

    def continuar_jogo(self) -> bool:
        """ Pergunta ao jogador se deseja continuar jogando. """
        resposta = input("Deseja continuar jogando? (s/n): ").strip().lower()
        return resposta == 's'

    def jogo_baccarat(self) -> None:
        # Função principal do jogo Baccarat.
        if not self.nome:
            self.nome = input('Digite seu nome: ')  # Pergunta o nome do jogador.

        while True:
            print(f"Seu saldo atual: {self.saldo}")
            valor_da_aposta = self.obter_valor_aposta()

            if valor_da_aposta is None:
                continue  # Volta para o início do loop se a aposta for inválida.

            aposta = self.obter_tipo_aposta()

            if aposta is None:
                continue  # Volta para o início do loop se o tipo de aposta for inválido.

            # Puxa as cartas para o jogador e a banca.
            cartas_player, cartas_banca = self.puxar_cartas(2), self.puxar_cartas(2)
            mensagem_player = self.verificar_terceira_carta(cartas_player, "PLAYER")
            mensagem_banca = self.verificar_terceira_carta(cartas_banca, "BANCA")

            self.exibir_cartas(cartas_player, "PLAYER", mensagem_player)
            self.exibir_cartas(cartas_banca, "BANCA", mensagem_banca)

            mao_do_player, mao_da_banca = self.calcular_pontuacao(cartas_player), self.calcular_pontuacao(cartas_banca)
            print("Pontuação PLAYER:", mao_do_player, "| Pontuação BANCA:", mao_da_banca)

            self.processar_resultado(aposta, valor_da_aposta, mao_do_player, mao_da_banca)

            if self.saldo > self.pontuacao_maxima:
                self.pontuacao_maxima = self.saldo

            if self.saldo <= 0:
                print("Saldo esgotado. Fim do jogo.")
                self.atualizar_ranking()
                break

            if not self.continuar_jogo():
                print(f"Obrigado por jogar! Saldo final: {self.saldo}")
                self.atualizar_ranking()
                break

    def obter_valor_aposta(self) -> int:
        """ Solicita o valor da aposta e valida a entrada. """
        try:
            valor = int(input('Digite o valor da aposta: '))
            if self.validar_aposta(valor):
                return valor
            else:
                print("Saldo insuficiente. Tente um valor menor.")
        except ValueError:
            print("Entrada inválida! Tente novamente.")
        return None

    def obter_tipo_aposta(self) -> int:
        """ Solicita o tipo de aposta e valida a entrada. """
        try:
            aposta = int(input("1-PLAYER, 2-BANCA, 3-EMPATE: "))
            if aposta in [1, 2, 3]:
                return aposta
            else:
                print("Opção de aposta inválida!")
        except ValueError:
            print("Entrada inválida! Tente novamente.")
        return None

# EXECUÇÃO DO JOGO
if __name__ == '__main__':
    jogo = BaccaratGame()
    jogo.exibir_baralho()
    jogo.jogo_baccarat()
