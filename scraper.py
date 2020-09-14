# <dl>
#     <dt>Pieces</dt>
#     <dd><a class="plain" href="/inventories/10251-1">2380</a></dd>
#     <dt>Minifigs</dt>
#     <dd><a class="plain" href="/minifigs/inset-10251-1">5</a></dd>
#     <dt>RRP</dt>
#     <dd>$169.99, 149.99€ | <a class="popuplink plain" href="prices?set=10251-1">More</a></dd>
#     <dt>PPP</dt>
#     <dd>7.1c, 6.3c</dd>
#     <dt>Packaging</dt>
#     <dd>Box</dd>
#     <dt>Availability</dt>
#     <dd>Retail - limited</dd>
#     <dt>Instructions</dt>
#     <dd><a class="popuplink plain" href="instructions2?set=10251-1&amp;s=1">Yes</a></dd>
#     <dt>Additional images</dt>
#     <dd><a class="plain" href="/sets/10251-1?more-images">26</a></dd>
#     <dt>Set type</dt>
#     <dd>Normal</dd>
# </dl>
import scrapy

class BrickSetSpyder(scrapy.Spider):
    # um nome qualquer para o nosso scrapy
    name = "bricket_spider"
    # a lista de sites a serem passados nele 
    start_urls = ["https://brickset.com/sets/year-2016"]

    def parse(self, response):
        # seletor css para pegar todos elementos da pagina
        SET_SELECTOR = '.set'

        for brickset in response.css(SET_SELECTOR):
            
            # pseudo seletor para pegar o conteudo da minha tag h1 que contem o nome do LEGO
            NAME_SELECTOR = 'h1 ::text'

            # e aqui pegamos a imagem que esta disposta  dentro do src da tag img
            #  dentro de uma tag a usando novamente um pseudo seletor css
            IMAGE_SELECTOR = 'img ::attr(src)'
            
             
            # nesse caso utilizamos xpath que é uma linguagem de consulta de xml
            # pois o problema para pegar essas informaçoes é mais complexo,
            # tive que pegar o texto que esta dentro de
            # uma tag dl e essa tag dl contem duas informações 
            # o nome da minha label e a quantidade de peçãs que preciso coletar
            # exemplo:
            # _____________________________________________________________________
            # <dl>                                                               //
            #     <dt>Pieces</dt>                                                //
            #     <dd><a class="plain" href="/inventories/10251-1">2380</a></dd> //
            #     ...                                                            //
            # </dl>                                                              //
            # ___________________________________________________________________//
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            
            # _____________________________________________________________________
            # <dl>                                                               //
            #     ...                                                            //
            #     <dt>Minifigs</dt>                                              //
            #     <dd><a class="plain" href="/inventories/10251-1">2380</a></dd> //
            #     ...                                                            //
            # </dl>                                                              //
            # ___________________________________________________________________//
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'

           
            yield {
                # aqui estamos pegando apenas o primeiro elemento do meu pseudo sseletor 
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'img': brickset.css(IMAGE_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            }

            # aqui assim que concluimos a extração de dados da pagina rastreamos a proxima
            # localizando onde esta o link da proxima pagina o scrapy.request() é um valor 
            # dizendo para o scrapy rastrear esse link, e em callback pedimos para que a
            # resposta seja mandada para parse que é o nosso metodo
            NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )


