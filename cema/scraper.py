from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

def iniciar_navegador(usuario, sen):
    # Configurar opções do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Inicializa o navegador com as opções configuradas
    nav = webdriver.Chrome(options=options)
    nav.get('https://sisregiii.saude.gov.br/')

    # Login
    user = nav.find_element(By.ID, 'usuario')
    user.send_keys(usuario)

    senha = nav.find_element(By.ID, 'senha')
    senha.send_keys(sen)

    # Espera até que o botão esteja clicável
    wait = WebDriverWait(nav, 10)
    btn1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudoFull"]/div[1]/div[1]/div[8]/input')))
    btn1.click()
    sleep(1)
    
    return nav, wait

def BuscarDadosPaciente(sus, usuario, sen):
    nav, wait = iniciar_navegador(usuario, sen)
    
    ConsultaGeral = nav.find_element(By.XPATH, '//*[@id="barraMenu"]/ul/li[3]/a')
    ConsultaGeral.click()
    ConsultaCNS = nav.find_element(By.XPATH, '//*[@id="barraMenu"]/ul/li[3]/ul/li[1]/a')
    ConsultaCNS.click()

    # Muda para o iframe correto
    nav.switch_to.frame("f_main")

    # Preenche o campo do CNS
    cns = nav.find_element(By.XPATH, '//*[@id="main_div"]/form/center[1]/table/tbody/tr[2]/td[2]/input')
    cns.send_keys(sus)

    # Clica no botão de pesquisa
    nav.find_element(By.NAME, 'btn_pesquisar').click()
    sleep(1)

    # Faz o scraping do conteúdo da página
    Conteudo = nav.page_source
    site = BeautifulSoup(Conteudo, 'html.parser')

    Pacote = site.find_all(attrs={"colspan": "2"})
    dados = [p.text for p in Pacote]

    table = site.find('table', class_='table_listagem', width='90%')
    rows = table.find_all('tr')[1:]
    telefones = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:  # Certifica-se de que a linha tem pelo menos 3 células
            tipo_telefone = cells[0].text.strip()
            ddd = cells[1].text.strip()
            numero = cells[2].text.strip()
            telefone_completo = f"{ddd} {numero}"
            telefones.append((tipo_telefone, telefone_completo))
            Tel = telefone_completo

    dadosPAC = {}
    if len(dados) > 37:
        dadosPAC['nome'] = dados[3]
        dadosPAC['sus'] = sus
        dadosPAC['mae'] = dados[7]
        dadosPAC['sexo'] = dados[11]
        dadosPAC['raca'] = dados[12]
        caid = dados[15]
        dadosPAC['dn'] = caid[0:10]
        dadosPAC['tipsang'] = dados[16]
        dadosPAC['nacionalidade'] = dados[19]
        dadosPAC['naturalidade'] = dados[20]
        dadosPAC['cidade'] = dados[36]
        dadosPAC['telefone'] = Tel

    nav.quit()
    return dadosPAC

def BuscarDadosCirugia(solicitacao, usuario, sen):
    nav, wait = iniciar_navegador(usuario, sen)
    
    ConsultaAMB = nav.find_element(By.XPATH, '//*[@id="barraMenu"]/ul/li[4]/a')
    ConsultaAMB.click()
    ConsultaCNS = nav.find_element(By.XPATH, '//*[@id="barraMenu"]/ul/li[4]/ul/li[1]/a')
    ConsultaCNS.click()

    # Muda para o iframe correto
    nav.switch_to.frame("f_main")

    # Preenche o campo Cod Solicitação
    cns = nav.find_element(By.XPATH, '//*[@id="main_page"]/form/center/table/tbody/tr[2]/td[2]/input')
    cns.send_keys(solicitacao)

    # Clica no botão de pesquisa
    nav.find_element(By.NAME, 'pesquisar').click()
    waitt = WebDriverWait(nav, 10)
    cir = waitt.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_page"]/form/center[2]/table/tbody/tr[3]/td[8]')))
    cir.click()
    sleep(1)

    # Faz o scraping do conteúdo da página
    Conteudo = nav.page_source
    site = BeautifulSoup(Conteudo, 'html.parser')
    
    # Inicializar listas para armazenar chaves e valores
    listaKey = []
    listaValue = []

    # Ignorar as linhas de marcação
    ignorar_linhas = ['UNIDADE SOLICITANTE', 'UNIDADE EXECUTANTE', 'Dados do Paciente', 'Dados da Solicitação', 'PREPARO(S) PARA O PROCEDIMENTO(S)', 'AVISOS DO MUNICÍPIO']

    # Extrair dados da tabela
    table = site.find('table', class_='table_listagem')
    if table:
        rows = table.find_all('tr')
        contador = 0
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols if ele.text.strip()]

            # Ignorar linhas de marcação exatamente como estão
            if len(cols) > 0 and cols[0] in ignorar_linhas:
                continue

            # Alternar entre chaves e valores
            if contador % 2 == 0:
                listaKey.extend(cols)
            else:
                listaValue.extend(cols)
            
            contador += 1

    # Criar o dicionário associando as listas de chaves e valores
    dados = {k: v for k, v in zip(listaKey, listaValue)}

    nav.quit()

    dadosPAC = {}    
    dadosCIR = {}
    lista = {}

    dadosPAC['nome'] = dados['Nome do Paciente']
    dadosPAC['sus'] = dados['CNS:']
    dadosPAC['mae'] = dados['Nome da Mãe']
    dadosPAC['sexo'] = dados['Sexo:']
    dadosPAC['raca'] = dados['Raça:']
    caid = dados['Data de Nascimento:']
    dadosPAC['dn'] = caid[0:10]
    dadosPAC['tipsang'] = dados['Tipo Sanguíneo:']
    dadosPAC['nacionalidade'] = dados['Nacionalidade:']
    dadosPAC['naturalidade'] = dados['Município de Nascimento:']
    dadosPAC['cidade'] = dados['Município de Residência:']    
    dadosPAC['telefone'] = dados ['Telefone(s):']
    dadosCIR['sol'] = dados ['Código da Solicitação:']
    dadosCIR['datasol'] = dados ['Data Solicitação:']
    dadosCIR['status'] = dados ['Situação Atual:']
    dadosCIR['classificacao'] = dados ['Risco:']
    dadosCIR['medico'] = dados ['Nome Médico Solicitante:']
    dadosCIR['diagnostico'] = dados ['Diagnóstico Inicial:']
    dadosCIR['cid'] = dados ['CID:']
    dadosCIR['procedimento'] = dados ['Procedimentos Solicitados:']
    dadosCIR['codunificado'] = dados ['Cód. Unificado:']
    dadosCIR['codinterno'] = dados ['Cód. Interno:']
    dadosCIR['justificativa'] = dados ['Laudo / Justificativa: (Exibir Histórico)']
    dadosCIR['chave'] = dados ['Chave de Confirmação:']
    dadosCIR['dataaprova'] = dados ['Data Aprovação:']
    dadosCIR['dataauto'] = dados ['Data e Horário de Atendimento:']
    lista['dadosPAC'] = dadosPAC
    lista['dadosCIR'] = dadosCIR

    return lista


Pac = BuscarDadosPaciente('708201135939142','HRSCARLOSEDUARDO', '23UROLOGIA')
print(Pac)

Dados = BuscarDadosCirugia('521098496','HRSCARLOSEDUARDO', '23UROLOGIA')
print (Dados)