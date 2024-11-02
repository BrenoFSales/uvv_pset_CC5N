# **PSET - Linguagens de Programação**
## *Processamento de imagem*

Neste respositório está documentado todo o estudo de processamento de imagens e algorítmos relacionados a manipulação das mesmas utilizando cálculos e aplicação de *kernels* para obter efeitos/filtros.

Nos arquivos iniciais fornecidos pelo professor da disciplinas (inclusive os mesmos arquivos fornecidos em sua integra se encontram no primeiro commit do repositório) possuía um script pset1.py onde se encontrava a classe imagem e todos os seus atributos e métodos iniciais, esses métodos o professou já disponibilizou em sua total funcionalidade, e foram utilizados os seguintes métodos ao decorrer do pset:

* carregar(): 
> Carrega uma imagem do arquivo fornecido e retorna uma instância dessa classe representando essa imagem. Também realiza a conversão para tons de cinza.

* nova():
>  Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

* savar():
> Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo. Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será inferido a partir do nome fornecido. Se nome_arquivo for fornecido como um objeto semelhante a um arquivo, o tipo de arquivo será determinado pelo parâmetro 'modo'.

* mostrar():
> Mostra uma imagem em uma nova janela Tk, da biblioteca do tkinter.
---

Vale ressaltar que nesse arquivo possui orientações, como por exemplo não ser permitido importar outras bibliotecas além do que já constavam no script, então por esse motivo não foi utilizada o Numpy por exemplo para trabalhar com as matrizes das imagens.

Além desse script com todo o algorítmo de processamento das imagens, há também um arquivo python para testes unitários, ao final da conclusão de todas as questões do PSET o objetivo é concluir a execusão desse script com todos os testes tendo seu resultado como **'OK'**. Em resumo os testes unitários comparam os resultados gerados do algorítmo criado, com resultados esperados de imagens já disponibilizadas pelo professor em um diretório.

## Sobre a classe *Imagem*

* Atributos:
    - largura;
    - altura;
    - quantidade de pixels.

* Métodos:
    - get_pixel
        > Para obter o valor do pixel.
    
    - set_pixel
        > Para aplicar novo valor do pixel.

    - aplicar_por_pixel:
        > Obtém o valor de cada pixel da imagem aplicando novo valor aos mesmos.
    
    - aplicar_kernel
        > Essa função aplica um kernel a uma imagem, através do cálculo de correlação linear orientado no PSET,retornando uma nova imagem com os valores calculados para apllicar os filtros.

