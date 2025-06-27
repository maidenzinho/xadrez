# Xadrez em Python com PyQt5 e IA

Um jogo de xadrez completo em Python, com interface gráfica usando PyQt5, suporte a IA de vários níveis e placar persistente.  
Jogue contra o computador em três níveis de dificuldade, com emojis nas peças, escolha de cor do jogador e interface intuitiva!

## 🎥 Demonstração

![image](https://github.com/user-attachments/assets/4b1694b4-01e7-47db-82a5-e901037067e5)


---

## 📋 Funcionalidades

- **Interface Gráfica em PyQt5**  
- **Tabuleiro visual e responsivo**  
- **Peças com emojis Unicode**  
- **IA de três níveis (Fácil, Médio, Difícil)**  
- **Escolha de cor: jogue de Brancas ou Pretas**
- **Destaque de peça selecionada e jogadas possíveis**
- **Promoção de peão com diálogo visual**
- **Feedback claro para jogadas inválidas**
- **Mensagens de xeque, xeque-mate, empate**
- **Placar persistente (vitórias, derrotas, empates)**
- **Reinício automático ao fim da partida**

---

## 🚀 Como rodar

### 1. **Pré-requisitos**

- Python 3.7+  
- [PyQt5](https://pypi.org/project/PyQt5/)  
- [python-chess](https://pypi.org/project/python-chess/)

Instale via pip:
```bash
pip install PyQt5 python-chess
```

### 2. **Baixe este repositório**
```bash
git clone https://github.com/maidenzinho/xadrez.git
cd xadrez
```

### 3. **Execute o programa**

```bash
python xadrez.py
```

---

## 🕹️ Como jogar

- Escolha sua cor (Brancas ou Pretas) ao iniciar.
- Selecione a dificuldade desejada (Fácil, Médio, Difícil).
- Clique na peça que deseja mover; casas de destino válidas ficarão verdes.
- Clique no destino para movimentar.
- Se tentar um movimento inválido, será avisado!
- Quando um peão chega à última linha, escolha a peça para promoção.
- O jogo termina automaticamente ao xeque-mate ou empate, e o placar é atualizado.
- Para jogar novamente, basta jogar após o reinício automático.

---

## 🤖 Sobre a IA

- **Fácil:** joga movimentos aleatórios e alguns erros bobos.
- **Médio:** prioriza capturas e faz avaliações simples.
- **Difícil:** considera mais opções, busca melhor avaliação material.

A IA **não** é imbatível, mas garante partidas divertidas e educativas!

---

## 🛠️ Estrutura do Projeto

```
xadrez/
│
├── xadrez.py         # Código-fonte principal
├── README.md         # Este tutorial/documentação
```

---

## ❓ Dúvidas frequentes

- **Como trocar a cor do jogador?**  
  Só reiniciar o app, escolher na tela inicial!
- **Posso jogar CPU x CPU?**  
  Não, este projeto é para humano x IA apenas.
- **Como mudar o tamanho do tabuleiro?**  
  Modifique o valor em `btn.setFixedSize(60, 60)` para ajustar.
- **Como pausar/retomar?**  
  Feche o app, o placar zera ao fechar.

---

## 💡 Customização

- Para deixar o jogo ainda mais completo, você pode:
    - Adicionar opção de **desfazer jogada (Undo)**
    - Salvar e carregar partidas (PGN)
    - Trocar tema de cores
    - Adicionar sons
    - Permitir modo espectador ou CPU x CPU

Abra **Issues** ou faça um **Pull Request** para contribuir!

---

## 👨‍💻 Autor

Feito por [Maidenzinho](https://github.com/maidenzinho)  
Baseado no incrível pacote [python-chess](https://python-chess.readthedocs.io/en/latest/) e PyQt5.

---

<div align="center">
♟️ Bom jogo! ♛
</div>
