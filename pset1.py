# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Breno Ferreira Sales
#    Matrícula: 202203561
#    Turma: CC5N
#    Email: breno.sales@uvvnet.com.br
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        return self.pixels[y * self.largura + x]

    def set_pixel(self, x, y, c):
        self.pixels[y * self.largura + x] = c

    def aplicar_kernel(self, kernel: list[list[int]]):
        """
        Essa função aplica um kernel(2D) à imagem, através de correlação de matrizes conforme o PDF do pset.
        """

        # Dimensões do kernel
        altura_kernel = len(kernel)
        largura_kernel = len(kernel[0])

        imagem_resultado = Imagem.nova(self.largura, self.altura)

        """
        - Calcule o padding vertical e horizontal
            Esses valores de padding são usados para adicionar pixels ao redor da imagem de entrada,
            antes de aplicar a correlação. Isso ajuda a preservar as bordas da imagem e evitar problemas de limite como:
            -- IndexError: list index out of range
        """
        padding_y = altura_kernel // 2
        padding_x = largura_kernel // 2

        # Percorre cada pixel da imagem
        for y in range(self.altura):
            for x in range(self.largura):
                soma = 0

                # Aplica o kernel no pixel atual
                for ky in range(altura_kernel):
                    for kx in range(largura_kernel):
                        # Calcula as coordenadas do pixel correspondente
                        pixel_y = y + ky - padding_y
                        pixel_x = x + kx - padding_x

                        # Verifica se o pixel está dentro da imagem
                        if (0 <= pixel_x < self.largura and 
                            0 <= pixel_y < self.altura):
                            # Obtem o valor do pixel e multplica pelo kernel
                            soma += self.get_pixel(pixel_x, pixel_y) * kernel[ky][kx]

                # Atribui o novo valor do pixel, limitando-o entre 0 e 255, para evitar números negativos, maiores que 255 (escala de ciza), e float. 
                imagem_resultado.set_pixel(x, y, min(max(int(soma), 0), 255))

        return imagem_resultado
    

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado

    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrada(self, n):
        raise NotImplementedError

    def focada(self, n):
        raise NotImplementedError

    def bordas(self):
        raise NotImplementedError

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    # --------------------------------------------------------------

    # Definir um kernel
    kernel_identidade = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]

    kernel_translacao = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    kernel_media = [
        [0.0, 0.2, 0.0],
        [0.2, 0.2, 0.2],
        [0.0, 0.2, 0.0]
    ]

    kernel_questao_4 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    kernel_blur = [
        [1/273, 4/273, 6/273, 4/273, 1/273],
        [4/273, 16/273, 24/273, 16/273, 4/273],
        [6/273, 24/273, 36/273, 24/273, 6/273],
        [4/273, 16/273, 24/273, 16/273, 4/273],
        [1/273, 4/273, 6/273, 4/273, 1/273]
    ]

    # Carregar imagem
    imagemOriginal = Imagem.carregar('./test_images/pigbird.png')

    # Aplicar a correlação
    imagemCorrelacionada = imagemOriginal.aplicar_kernel(kernel_blur)

    # Salvar e mostrar a nova imagem
    imagemCorrelacionada.salvar('./my_tests/Teste-Correlacao.png')
    print(imagemCorrelacionada)
    imagemCorrelacionada.mostrar()

    # --------------------------------------------------------------
    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
