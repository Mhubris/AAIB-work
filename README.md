# Trabalho de AAIB
### Autores:
+ Bernardo Teixeira
+ Miguel Andrade
+ Sara Lobo

### Resumo:
Este trabalho consiste na implementação de um classificador cuja a finalidade é informar os médicos se determinado paciente necessita de cadeira elétrica ou automática, com base nos valores de aceleração do telefone. De forma a enrriquecer o nosso trabalho identificaram-se sete labels, incluindo as anteriores, que são as seguintes:
1. Parado
2. Teste Inválido
3. Cadeira Elétrica
4. Cadeira Manual
5. Foi Empurrado
6. Andou para trás
7. Telemóvel não colocado no suporte

### Instalação da aplicação
A aplicação foi desenvolvida em Cordova e a sua pasta é 'Mobile'. De forma a instalar a mesma no seu telemóvel deve instalar o Node.js e de seguida o Cordova, através do comando:
`npm install -g cordova` De seguida basta, através da consola, ir até à pasta 'Mobile' e correr o comando `cordova run android`, caso o seu dispositivo seja android. De outra forma, consulte a [documentação](https://cordova.apache.org/docs/en/latest/guide/cli/index.html#add-platforms) para adicionar mais plataformas e inicializar a aplicação.

### Código do servidor RPI
#### Configuração 
Visto que a comunicação entre o telefone e o RPI é feita através de uma socket, na tabela seguintes encontram-se as especificações da mesma:

|IP | 192.168.0.74|
| ------- | ----------- |
|Porta    | 5005        |

#### Classifcação

### Suporte para a cadeira
De forma a garantir o bom funcionamento do classificador sugere-se a impressão do ficheiro .STL que se encontra no repositório. Este deve ser colocado da seguinte forma:
![alt text](https://github.com/Mhubris/AAIB-work/blob/master/cadeira.JPG "")

