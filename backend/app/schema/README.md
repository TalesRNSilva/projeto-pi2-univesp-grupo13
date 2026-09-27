# O que é 

Essa pasta serve para declarar objetos de schema para encapsular e validar os objetos recebidos e enviados
nas interações via endpoints da API. 

Fluxo esperado é: definir uma classe de schema nessa pasta; quando chegar uma requisição, validar
a requisição com o schema de entrada. Quando for enviar uma resposta, encapsular a resposta 
com o schema de resposta e converter para JSON.