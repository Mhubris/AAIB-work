# Trabalho de AAIB
### Autores:
+ Bernardo Teixeira
+ Miguel Andrade
+ Sara Lobo

### Resumo:
Este trabalho consiste na implementação de um classificador cuja a finalidade é informar os médicos se determinado paciente necessita de cadeira elétrica ou automática, com base nos valores de aceleração do telefone. De forma a enriquecer o nosso trabalho identificaram-se sete labels, incluindo as anteriores, que são as seguintes:
1. Cadeira Manual
2. Cadeira Elétrica
3. Foi Empurrado
4. Teste Inválido
5. Parado
6. Telemóvel não colocado no suporte

Para uma melhor compreensão da estrutura deste repositório e das funcionalidades associadas a cada ficheiro deve ser lido o relatório disponível em ....

### Instalação da aplicação
A aplicação foi desenvolvida em Cordova e a sua pasta é 'Mobile'. De forma a instalar a mesma no seu telemóvel deve instalar o Node.js e de seguida o Cordova, através do comando:
`npm install -g cordova`. De seguida, basta através da consola ir até à pasta 'Mobile' e correr o comando `cordova run android`, caso o seu dispositivo seja android. De outra forma, consulte a [documentação](https://cordova.apache.org/docs/en/latest/guide/cli/index.html#add-platforms) para adicionar mais plataformas e inicializar a aplicação.

### Código do servidor RPI
#### Configuração 
Visto que a comunicação entre o telefone e o RPI é feita através de uma socket, na tabela seguintes encontram-se as especificações da mesma:

|IP | 192.168.0.74|
| ------- | ----------- |
|Porta    | 5005        |

#### Classificação
Com recurso ao *software* Orange foram testados diversos classificadores e avaliadas a *accuracy* e matriz de confusão de cada classificador usando diversos métodos de *cross-validation*. Após alterações sucessivas no algoritmo de processamento dos dados e extração de *features*, com vista a aumentar a *accuracy* obtida, nomeadamente acrescentando e removendo algumas *features*, concluímos que o melhor classificador no contexto deste problema é uma implementação do algoritmo *Random Forest* com 60 árvores (`n_estimators`), 7 atributos considerados em cada bifurcação (`max_features`), um limite de profundidade de 4 em cada árvore (`max_depth`) e um mínimo de 5 amostras por folha (`min_samples_leaf`). O critério utilizado pelo algoritmo *Random Forest* para medir a qualidade de cada *split* é o critério de Gini.

Foi utilizada uma base de dados com 53 aquisições, simulando os 6 cenários previstos, para treinar o classificador *Random Forest* referido. Inicialmente foram extraídas 54 *features* mas este número foi reduzido para 28 com vista a melhorar a *accuracy* e tempo de execução do programa. Com *10-fold cross validation* a *Classification Accuracy* da aplicação do algoritmo *Random Forest* mencionado ronda os 96.2%. Usando como método de validação o algoritmo *leave-one-out* a *Classification Accuracy* ronda os 90.6%. Consideramos assim que em média obtivémos uma *Classification Accuracy* de aproximadamente 93%. 
Uma vez que existem 6 classes (E, I, N, P, S, X), a probabilidade de um classificador acertar aleatoriamente é 1/6 ≅ 17%. Podemos assim concluir que os resultados obtidos pelo classificador implementado são aproximadamente 5.6 vezes superiores a um classificador aleatório, sendo este valor bastante satisfatório na nossa opinião.

### Suporte para a cadeira
De forma a garantir o bom funcionamento do classificador sugere-se a impressão 3D do ficheiro .STL que se encontra neste repositório. Este deve ser colocado da seguinte forma:
![alt text](https://github.com/Mhubris/AAIB-work/blob/master/images_ex/cadeira.JPG "")

### QR codes para teste
![alt text](https://github.com/Mhubris/AAIB-work/blob/master/images_ex/bernardo.png "Bernardo")
![alt text](https://github.com/Mhubris/AAIB-work/blob/master/images_ex/miguel.png "Miguel")
![alt text](https://github.com/Mhubris/AAIB-work/blob/master/images_ex/sara.png "Sara")

