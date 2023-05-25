Implementar o jogo O GRANDE DALMUTI (THE GREAT DALMUTI) em uma rede em anel. 

As regras do jogo estão no arquivo pdf.  É um jogo leve de cartas, onde os jogadores ganham status por sair primeiro. O baralho de 80 cartas contém classificação de 12-1, junto com dois bobos da corte. Cada carta tem um número, que não é apenas a sua posição, mas também diz-lhe quantos dessa carta existe no baralho. Por outras palavras, existem doze 12s, onze 11s, quatro 4s e uma única carta de classificação 1. Quanto menor o número, melhor a classificação. O baralho é distribuído para todos os jogadores e o objetivo é se livrar de suas cartas o mais rápido possível. A mão começa com uma pessoa jogando um ou mais cartas para o centro da mesa. As cartas jogadas devem ser todas do mesmo nível (embora bobos da corte são coringas, e podem ser jogados com qualquer outra carta). Cada jogador, na sua vez, deve jogar o mesmo número de cartas de valor melhor, ou passar. O jogo continua ao redor da mesa até que todos tenham passado. Nesse ponto, as cartas são apuradas e quem jogou o último conjunto de cartas leva a próxima rodada. Depois de todos terem saído, os jogadores são classificados. Por exemplo, a primeira pessoa que se livrou de todas as suas cartas se torna o grande Dalmuti. 

O jogo de voces deve executar uma mão do jogo. Até que todos os jogadores consigam descartar suas cartas. Para a próxima mão, deve-se reiniciar o jogo, re-executar o jogo.

Vocês devem criar uma rede em anel usando socket DGRAM, sendo uma máquina para cada jogador. Isso significa que se forem 4 jogadores, o anel deve ter 4 máquinas, se forem 5 jogadores, deve ter 5 máquinas e assim por diante. A quantidade de máquinas, seus endereços e portas devem estar configurados em um arquivo txt antes do inicio do setup do anel. Vocês devem conectar a porta da saída da máquina 1 com a porta de entrada da máquina 2, a porta de saída da máquina 2 com a porta de entrada da máquina 3, e assim por diante. Até que a porta da saída da última máquina seja conectada com a porta de entrada da máquina 1.

Uma das máquinas deve ser o criador do bastão (pode ser fixo). Uma das máquinas deve ser o carteador (pode ser fixo).

O bastão inicia cada rodada com o vencedor da rodada anterior. Ele deve ir passando de jogador em jogador. Ele fica com o jogador até que esta faça a sua jogada. Assim que o jogador fez a sua jogada, deve ser enviada uma mensagem informando os outros jogadores quais cartas foram jogadas. Esta mensagem deve dar a volta na rede toda. Cada máquina que receber a mensagem, deve atualizar a tela do jogador e marcar um campo na mensagem dizendo que foi recebida. Quando ela retornar a origem, a origem retira a mensagem do anel, checa se foi recebida por todos e envia o bastão para a próxima máquina. 

Mensagens devem ter os seguintes campos:
- Marcador de inicio / origem / jogada / confirmação de recebimento / marcador de fim

Como os campos são feitos e formatados é decisão da equipe. Caso achem necessário mais algum campo na mensagem isso também é decisão da equipe.

Não precisa se preocupar com a perda do bastão. Não temos verificação de erro nas mensagens. 

Valor: 2,0
Em duplas

Entregar um único arquivo em formato (zip / tgz / gz) com todo o código dentro dele.