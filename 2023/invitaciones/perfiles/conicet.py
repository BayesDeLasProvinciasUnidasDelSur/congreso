from lxml import html
import requests
import csv

existe = 0
for i in range(64080,100000):#i=19500
    identificador = i
    url = 'https://www.conicet.gov.ar/new_scp/detalle.php?keywords=&id={}&datos_academicos=yes'.format(i)
    try:
        page = requests.get(url,timeout=5)
    except:
        continue
    if (page.status_code == 200) and (not "Lo sentimos! Actualmente no se puede acceder" in page.text):
        tree = html.fromstring(page.text)
        investigador = 'INV ' in page.text
        nombre = tree.xpath('//div[@class="titulo_nombre"]/text()')
        info_items = tree.xpath('//div[@class="contenido_item"]')
        if len(info_items) == 0:
            print(i, existe)
            continue
        existe += 1
        categoria = info_items[1].xpath('.//div[@class="contenido_label_info"]/text()')
        bayes = False; proba = False; MC = False
        bayes = bayes or "Bayes" in page.text; bayes = bayes or "bayes" in page.text
        proba = proba or "Probab" in page.text; proba = proba or "probab" in page.text
        MC = MC or "Monte Carlo" in page.text
        url = 'https://www.conicet.gov.ar/new_scp/detalle.php?keywords=&id={}&articulos=yes'.format(i)
        try:
            page = requests.get(url,timeout=5)
        except:
            continue
        bayes = bayes or "Bayes" in page.text; bayes = bayes or "bayes" in page.text
        proba = proba or "Probab" in page.text; proba = proba or "probab" in page.text
        MC = MC or "Monte Carlo" in page.text
        if (bayes or proba) or MC:
            print("Perfil!")
            with open('perfiles.csv','a') as fd:
                fd.write('{}, {}, {}, {}, {}, {}\n'.format(identificador, nombre[0], categoria[0], bayes, proba, MC) )

    print(i, existe)







