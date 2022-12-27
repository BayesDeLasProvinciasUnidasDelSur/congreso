
#################################################################
#################################################################
#driver.execute_script("arguments[0].scrollIntoView(true);", info_personas[i]);


# VERSION CUANDO HAY MUCHOS AUTORES
mas_personas = driver_paper.find_elements(by=By.XPATH, value= '//article/div[2]/section/div[2]/div[1]/div[1]/button')
if False:#if mas_personas[0].text == "Show additional authors":
    affil_links_all = []
    autor_links_all = []
    #
    ActionChains(driver_paper).move_to_element(mas_personas[0]).click(mas_personas[0]).perform()#
    #
    time.sleep(0.2)
    footer = driver_paper.find_elements(by=By.XPATH, value= '//article/div[2]/section/div[2]/div[1]/div[2]//footer/els-paginator/nav/ul/li')
    footer_int = [ int(e.text) for e in footer if e.text.isdigit() ]
    footer = [e for e in footer if e.text.isdigit()]
    f = 0
    while (f <= len(footer)):
        # Personas
        info_personas = driver_paper.find_elements(by=By.XPATH, value= '//article/div[2]/section/div[2]/div[1]/div[2]//li/els-button')
        tree_paper = html.fromstring(driver_paper.page_source)
        xpath_personas = [e.getroottree().getpath(e) for e in tree_paper.xpath('//article/div[2]/section/div[2]/div[1]/div[2]//li/els-button') ]
        # Visibles
        wa, wb, wc, wd = window_bounds(driver)
        visibles = [ element_completely_viewable(driver_paper,e, wa, wb, wc, wd) for e in info_personas ]
        in_view_personas = [e for j, e in enumerate(info_personas) if visibles[j]]
        visible_xpath_personas = [xp for j, xp in enumerate(xpath_personas) if visibles[j] ]
        ultimo_analizado = False
        while (not ultimo_analizado):
            # Datos (Links)
            affil_links, autor_links = autores(in_view_personas[0:3], visible_xpath_personas)
            affil_links_all += affil_links
            autor_links_all += autor_links
            # Condicion
            ultimo_analizado = element_completely_viewable(driver_paper, info_personas[-1], wa, wb, wc, wd)
            # Scroll
            driver_paper.execute_script("arguments[0].scrollIntoView();", in_view_personas[-1])
            #
            info_personas = driver_paper.find_elements(by=By.XPATH, value= '//article/div[2]/section/div[2]/div[1]/div[2]//li/els-button')
            visibles = [ element_completely_viewable(driver_paper,e, wa, wb, wc, wd) for e in info_personas ]
            in_view_personas = [e for j, e in enumerate(info_personas) if visibles[j]]
            visible_xpath_personas = [xp for j, xp in enumerate(xpath_personas) if visibles[j] ]
        #
        ActionChains(driver_paper).move_to_element(footer[f+1]).click(footer[f+1]).perform()#
        f += 1

        # Cierro
        x_elemento = driver_paper.find_element(by=By.XPATH, value= '//article/div[2]/section/div[2]/div[1]/div[2]//header/div[1]/els-button[1]')
        ActionChains(driver_paper).move_to_element(x_elemento).click(x_elemento).perform()

