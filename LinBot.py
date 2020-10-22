
#/*------------------------------------------------------------------------------------------*\
#|Git:                                                                                       *|                                                   
#|Nicolás Agustín Brogna                                                                     *|
#|*                                                                                          *|
#\*------------------------------------------------------------------------------------------*/

# Drivers, recordar instalar con PIP, 2 o 3.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import parametros, csv, os.path, time

# Funciones 
def search_and_send_request (keywords, till_page, writer):
    for page in range(1, till_page + 1):
        print('\Información: Revisando pagina numero %s' % (page))
        query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
        driver.get(query_url)
        time.sleep(5)
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(5)
        linkedin_urls = driver.find_elements_by_class_name('search-result__action-button')
        print('Informacion: %s conecciones encontradas en esta pagina %s' % (len(linkedin_urls), page))
        for connection in linkedin_urls:
            if connection.text == 'Conectar': # Ojo con esto que va a coordinar dependiendo Conectar o Connect.. tambien puede ser Submit.
                try:
                    coordinates = connection.location_once_scrolled_into_view # Coordenadas del scroll X, Y.
                    driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                    text = str(connection.get_attribute('aria-label'))
                    print("Información: %s" % (text))
                    time.sleep(5)
                    connection.click()
                    time.sleep(5)
                    if driver.find_elements_by_class_name('artdeco-button--primary')[0].is_enabled():
                        driver.find_elements_by_class_name('artdeco-button--primary')[0].click()
                        writer.writerow([text])
                    else:
                        driver.find_elements_by_class_name('artdeco-modal__dismiss')[0].click()
                except Exception as e:
                    print('ERROR: %s' % (e))
                time.sleep(5)

# Login
driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.linkedin.com/login')
driver.find_element_by_id('username').send_keys(parametros.linkedin_username)
driver.find_element_by_id('password').send_keys(parametros.linkedin_password)
driver.find_element_by_xpath('//*[@type="submit"]').click()
time.sleep(10)
#name = driver.find_elements_by_class_name('profile-rail-card__actor-link')[0].text.replace(' ', '')

# Archivo para cargar las conexiones que el bot realizó
file_name = parametros.file_name
file_exists =  os.path.isfile(file_name)
writer = csv.writer(open(file_name, 'a'))
if not file_exists: writer.writerow(['ConectarBot'])

# Busqueda... se saca del front. 
search_and_send_request(keywords=parametros.keywords, till_page=parametros.till_page, writer=writer)

# Todavía no pude realizar que haga un break el bot cuando ya termine la busqueda en lastpage. 
driver.quit()


