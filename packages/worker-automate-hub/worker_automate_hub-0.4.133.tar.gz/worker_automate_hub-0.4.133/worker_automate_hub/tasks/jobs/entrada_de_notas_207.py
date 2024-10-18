import warnings
import getpass
import os
import pyautogui
from pywinauto.application import Application
from pywinauto.timings import wait_until
from pywinauto.keyboard import send_keys
from pywinauto_recorder.player import set_combobox
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
    sync_get_config_by_name,
)
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.toast import show_toast, task_bar_toast
from worker_automate_hub.utils.util import (
    delete_xml,
    download_xml,
    get_xml,
    import_nfe,
    incluir_registro,
    kill_process,
    login_emsys,
    set_variable,
    type_text_into_field,
    verify_nf_incuded,
    worker_sleep,
    read_xml_file,
    extract_group_by_itens,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def entrada_de_notas_207(task):
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        #Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)
       
        #Seta config entrada na var nota para melhor entendimento
        nota = task['configEntrada']
        multiplicador_timeout = int(float(task["sistemas"][0]["timeout"]))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        #Fecha a instancia do emsys - caso esteja aberta
        await kill_process("EMSys")

        # Download XML
        get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
        get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        env_config, _ = load_env_config()

        download_result = await download_xml(env_config["XML_DEFAULT_FOLDER"], get_gcp_token, get_gcp_credentials, nota["nfe"])
        if download_result['sucesso'] == True:
            console.log('Download do XML realizado com sucesso', style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{download_result['retorno']}"}

        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config['conConfiguracao'], app, task)

        if return_login['sucesso'] == True:
            type_text_into_field('Nota Fiscal de Entrada', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await worker_sleep(2)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login
        
        await worker_sleep(6)
        #Procura campo documento
        console.print('Navegando pela Janela de Nota Fiscal de Entrada...\n')
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]

        console.print("Controles encontrados na janela 'Nota Fiscal de Entrada, navegando entre eles...\n")
        panel_TNotebook = main_window.child_window(class_name="TNotebook", found_index=0)
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(class_name="TPageControl", found_index=0)
        panel_TTabSheet = panel_TPageControl.child_window(class_name="TTabSheet", found_index=0)
        combo_box_tipo_documento = panel_TTabSheet.child_window(class_name="TDBIComboBox", found_index=1)
        combo_box_tipo_documento.click()
        console.print("Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n")
        await worker_sleep(2)
        set_combobox("||List", "NOTA FISCAL DE ENTRADA ELETRONICA - DANFE")
        console.print("Tipo de documento 'NOTA FISCAL DE ENTRADA ELETRONICA - DANFE', selecionado com sucesso...\n")

        await worker_sleep(4)

        #Clica em 'Importar-Nfe'
        imported_nfe  = await import_nfe()
        if imported_nfe['sucesso'] == True:
            console.log(imported_nfe['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{imported_nfe['retorno']}"}

        await worker_sleep(5)

        await get_xml(nota["nfe"])
        await worker_sleep(3)

        
        #VERIFICANDO A EXISTENCIA DE WARNINGS
        await worker_sleep(4)
        try:
            console.print("Verificando a existencia de warning após a importação do xml...\n")
            app = Application().connect(title="Warning")
            main_window = app["Warning"]
            
            console.print("Clicando em NO, para andamento do processo...\n")
            # btn_no = main_window.child_window(title="&No")
            btn_no = main_window["&No"]

            if btn_no.exists():
                try:
                    btn_no.click()
                    await worker_sleep(4)
                    if main_window.exists():
                        btn_no = main_window.child_window(title="&No")
                        console.print("Clicando novamente em NO")
                        btn_no.click()
                except Exception as e:
                    console.print(f"Erro ao clicar em NO: {e}")
                await worker_sleep(5)
            else:
                console.print("Warning - Erro após a importação do arquivo...\n")
                return {"sucesso": False, "retorno": 'Warning - Erro após a importação do arquivo, não foi encontrado o botão No para andamento do processo... \n'} 
        except:
            console.print("Não possui nenhum warning após a importação do xml...\n")
        
        #VERIFICANDO A EXISTENCIA DE ERRO
        try:
            app = Application().connect(title="Erro")
            main_window = app["Erro"]
            await worker_sleep(7)
            all_controls_from_error = main_window.children()
            capturar_proxima_mensagem = False

            for control in all_controls_from_error:
                control_text = control.window_text()

                if "Mensagem do Banco de Dados" in control_text:
                    capturar_proxima_mensagem = (
                        True
                    )

                elif capturar_proxima_mensagem:
                    return {"sucesso": False, "retorno": f'Pop-UP Erro após a importação do arquivo, erro do banco de dados: {control_text} \n'}

                if "XML já foi importado anteriormente" in control_text:
                    return {"sucesso": False, "retorno": f'Pop-UP Erro após a importação do arquivo, Nota descartada {control_text}... \n'}           
        except:
            console.print("Não possui nenhuma mensagem de erro após a importação do xml...\n")

        app = Application().connect(title="Informações para importação da Nota Fiscal Eletrônica")
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        #INTERAGINDO COM A NATUREZA DA OPERACAO
        cfop = int(nota["cfop"])
        console.print(f"Inserindo a informação da CFOP, caso se aplique {cfop} ...\n")
        if cfop == 5655 or str(cfop).startswith("56"):
            combo_box_natureza_operacao = main_window.child_window(class_name="TDBIComboBox", found_index=0)
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1652-COMPRA DE MERCADORIAS- 1.652")
            await worker_sleep(3)
        
        else:
            console.print("Erro mapeado, CFOP diferente de 5655 ou 56, necessario ação manual ou ajuste no robo...\n")
            return {"sucesso": False, "retorno": f"Erro mapeado, CFOP diferente de 5655 ou 56, necessario ação manual ou ajuste no robo"}


        #INTERAGINDO COM O CAMPO ALMOXARIFADO
        filialEmpresaOrigem = nota["filialEmpresaOrigem"]
        console.print(f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n")
        #task_bar_toast("Teste toast bar", f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...", 'Worker', 10)
        #show_toast("Teste toast", f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...")
        try:
            new_app = Application(backend="uia").connect(
                title="Informações para importação da Nota Fiscal Eletrônica"
            )
            window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
            edit = window.child_window(
                class_name="TDBIEditCode", found_index=3, control_type="Edit"
            )
            valor_almoxarifado = filialEmpresaOrigem + "50"
            edit.set_edit_text(valor_almoxarifado)
            edit.type_keys("{TAB}")

        except Exception as e:
            console.print(f"Erro ao iterar itens de almoxarifado: {e}")
            return {"sucesso": False, "retorno": f"Erro ao iterar itens de almoxarifado: {e}"}


        await worker_sleep(3)
        #INTERAGINDO COM CHECKBOX Utilizar unidade de agrupamento dos itens
        console.print("Verificando se a nota é do fornecedor SIM Lubrificantes \n")
        fornecedor = nota["nomeFornecedor"]
        itens_agrupado = False
        console.print(f"Fornecedor: {fornecedor} ...\n")
        if "sim lubrificantes" in fornecedor.lower():
            console.print(f"Sim, nota emitida para: {fornecedor}, marcando o agrupar por unidade de medida...\n")
            checkbox = window.child_window(
                title="Utilizar unidade de agrupamento dos itens",
                class_name="TCheckBox",
                control_type="CheckBox"
            )
            if not checkbox.get_toggle_state() == 1:
                checkbox.click()
                console.print("Realizado o agrupamento por unidade de medida... \n")
        else:
            console.print("Não foi necessario realizar o agrupamento por unidade de medida... \n")
        
        await worker_sleep(2)
        console.print("Clicando em OK... \n")
        try:
            btn_ok = main_window.child_window(title="Ok")
            btn_ok.click()
        except:
            btn_ok = main_window.child_window(title="&Ok")
            btn_ok.click()
        await worker_sleep(6)


        username = getpass.getuser()
        console.print('Verificando se existem itens nao localizados para o fornecedor...\n')
        try:
            app = Application().connect(class_name="TFrmAguarde")
            main_window = app["TMessageForm"]

            if main_window.exists():
                main_window.type_keys('%n')

                await worker_sleep(4)
                app = Application().connect(class_name="TFrmExibeLogErroImportacaoNfe")
                main_window = app["TFrmExibeLogErroImportacaoNfe"]

                btn_save = main_window.child_window(title="Salvar", class_name="TBitBtn")

                if btn_save.exists():
                    btn_save.click()
                    await worker_sleep(4)
                    app = Application().connect(title="Salvar")
                    main_window = app["Salvar"]
                    main_window.type_keys('%n')
                    path_to_txt = f"C:\\Users\\{username}\\Downloads\\erro_itens{nota["nfe"]}.txt"
                    pyautogui.write(path_to_txt)
                    await worker_sleep(1)
                    main_window.type_keys('%l')

                    conteudo = ''
                    await worker_sleep(3)
                    with open(path_to_txt, 'r', encoding='utf-8') as arquivo:
                        conteudo = arquivo.read()

                    os.remove(path_to_txt)
                    console.print(f"Itens nao localizados para o fornecedor...\n")
                    return {"sucesso": False, "retorno": f"Itens nao localizados para o fornecedor, Mensagem: {conteudo}"}
                else:
                    console.print(f"Botao Salvar - Não foi encontrado...\n")
                    return {"sucesso": False, "retorno": f"Botao Salvar - Não foi encontrado"}
        except Exception as e:
            console.print("Não possui nenhum itens nao localizados para o fornecedo...\n")


        console.print('Navegando pela Janela de Nota Fiscal de Entrada...\n')
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        console.print('Acessando os itens da nota... \n')
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("{DOWN " + ("5") + "}")

        #CONFIRMANDO SE A ABA DE ITENS FOI ACESSADA COM SUCESSO
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TPage.wait("visible")
        panel_TTabSheet = panel_TPage.child_window(class_name="TTabSheet")
        title_n_serie = panel_TPage.child_window(title="N° Série")

        console.print('Verificando se os itens foram abertos com sucesso... \n')
        if not title_n_serie:
            console.print(f"Não foi possivel acessar a aba de 'Itens da nota...\n")
            return {"sucesso": False, "retorno": "Não foi possivel acessar a aba de 'Itens da nota'"}

        await worker_sleep(2)

        console.print('Acessando os itens indivualmente... \n')
        send_keys("{TAB 2}", pause=0.1)
        await worker_sleep(2)
        
        path_to_xml = f"C:\\Users\\{username}\\Downloads\\{nota["nfe"]}.xml"
        get_xml_itens = await read_xml_file(path_to_xml)
        itens = await extract_group_by_itens(get_xml_itens)


        console.print(f"Trabalhando com os itens, alterando a unidade com base na descrição do item \n")
        try:
            for item in itens:
                n_item = item['n_item']
                formato = item['formato']
                descricao = item['descricao']
                pos_x = formato.find('X')
                cod_split = str(formato[1:pos_x])

                send_keys('^({HOME})')
                await worker_sleep(1)

                if int(n_item) > 1:
                    send_keys('{DOWN ' + str(n_item) + '}')

                if cod_split != "1":
                    console.print(f"Item a ser ajustado: {descricao} \n")
                    await worker_sleep(2)
                    send_keys('+{F10}')
                    await worker_sleep(1)
                    send_keys('{DOWN 2}')
                    await worker_sleep(1)
                    send_keys('{ENTER}')
                    
                    await worker_sleep(2)
                    app = Application().connect(title="Alteração de Item")
                    main_window = app["Alteração de Item"]

                    main_window.set_focus()

                    edit = main_window.child_window(class_name="TDBIEditCode", found_index=0)

                    #ITERAGINDO COM O IPI
                    tpage_ipi = main_window.child_window(class_name="TPanel", found_index=0)
                    ipi = tpage_ipi.child_window(class_name="TDBIComboBox", found_index=2)

                    ipi_value = ipi.window_text()

                    console.print(f"Trabalhando com os itens, valor do IP {ipi_value}... \n")
                    if len(ipi_value) == 0:
                        console.print(f"Trabalhando com os itens, valor do IP em branco, selecionando IPI 0% ... \n")
                        ipi.click_input()
                        send_keys("^({HOME})")
                        send_keys("{DOWN 6}")
                        send_keys("{ENTER}")

                        await worker_sleep(4)
                        tpage_ipi = main_window.child_window(class_name="TPanel", found_index=0)
                        ipi = tpage_ipi.child_window(class_name="TDBIComboBox", found_index=2)

                        ipi_value = ipi.window_text()

                        if 'IPI 0%' in ipi_value:
                            console.print(f"Trabalhando com os itens, sucesso ao selecionar o valor do IPI ... \n")
                        else:
                            return {"sucesso": False, "retorno": f"Erro ao selecionar o IPI de unidade nos itens, IPI: {ipi_value}"} 

                        await worker_sleep(4)

                    try:
                        console.print(f"SELECIONANDO UN-{cod_split} - F PARA UNIDADE ...\n")
                        get_unidade = main_window.child_window(class_name="TDBIComboBox", found_index=1)
                        combo_box_group = "UN-"+cod_split+" - F"
                        if cod_split in get_unidade.window_text():
                            get_unidade.click_input()
                            set_combobox("||List", combo_box_group)
                            await worker_sleep(4)
                        
                        #VERIFICANDO SE FOI SELECIONADO CORRETAMENTE
                        console.print(f"VERIFICANDO SE FOI SELECIONADO UN-{cod_split} - F PARA UNIDADE ...\n")
                        get_unidade = main_window.child_window(class_name="TDBIComboBox", found_index=1)
                        if cod_split in get_unidade.window_text():
                            combo_box_group = "UN-"+cod_split+" - F"
                            console.print(f"NÃO FOI SELECIONADO UN-{cod_split} - F PARA UNIDADE, TENTANDO SELECIONAR COMO CAIXA...\n")
                            num_adjusted = cod_split
                            if int(cod_split) < 9:
                                num_adjusted = "0"+str(cod_split)
                            combo_box_group = "CAIXA C/"+num_adjusted
                            get_unidade.click_input()
                            set_combobox("||List", combo_box_group)
                            await worker_sleep(4)
                        
                        get_unidade = main_window.child_window(class_name="TDBIComboBox", found_index=1)
                        if cod_split in get_unidade.window_text():
                            return {"sucesso": False, "retorno": f"Erro ao selecionar o tipo de unidade nos itens, item: {n_item} {descricao}, não possui UN-{cod_split} - F OU CAIXA C/{cod_split} "} 
                        else:
                            console.print(f"SELECIONADO COMO CAIXA PARA UNIDADE...\n")

                    except Exception as e:
                        return {"sucesso": False, "retorno": f"Erro ao selecionar o tipo de unidade nos itens: {e}"}

                    try:
                        btn_alterar = main_window.child_window(title="&Alterar")
                        btn_alterar.click()
                    except:
                        btn_alterar = main_window.child_window(title="Alterar")
                        btn_alterar.click()
                    await worker_sleep(3)

        except:
            return {"sucesso": False, "retorno": f"Erro aotrabalhar nas alterações dos itens: {e}"}

        await worker_sleep(2)
        # Inclui registro
        console.print(f"Incluindo registro...\n")
        try:
            ASSETS_PATH = "assets"
            inserir_registro = pyautogui.locateOnScreen(ASSETS_PATH + "\\entrada_notas\\IncluirRegistro.png", confidence=0.8)
            pyautogui.click(inserir_registro)
        except Exception as e:
            console.print(f"Não foi possivel incluir o registro utilizando reconhecimento de imagem, Error: {e}...\n tentando inserir via posição...\n")
            await incluir_registro()

        #Verifica se a info 'Nota fiscal incluida' está na tela   
        await worker_sleep(6)
        retorno = False
        try:
            app = Application().connect(class_name="TFrmNotaFiscalEntrada")
            main_window = app["Information"]

            main_window.set_focus()
            
            console.print(f"Tentando clicar no Botão OK...\n")
            btn_ok = main_window.child_window(class_name="TButton")

            if btn_ok.exists():
                btn_ok.click()
                retorno = True
            else:
                console.print(f" botão OK Não enontrado")
                retorno = await verify_nf_incuded()

        except Exception as e:
            console.print(f"Erro ao conectar à janela Information: {e}\n")
            return {"sucesso": False, "retorno": f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}"}


        if retorno:
            console.print("\nNota lançada com sucesso...", style="bold green")
            await worker_sleep(6)
            return {"sucesso": True, "retorno": f"Nota Lançada com sucesso!"}
        else:
            console.print("Erro ao lançar nota", style="bold red")
            return {"sucesso": False, "retorno": f"Erro ao lançar nota"}
        

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}

    finally:
        await kill_process("EMSys")
        # Deleta o xml
        await delete_xml(nota["nfe"])
