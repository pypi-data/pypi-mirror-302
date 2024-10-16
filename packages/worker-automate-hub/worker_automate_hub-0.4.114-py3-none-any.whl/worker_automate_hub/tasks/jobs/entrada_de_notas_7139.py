import warnings

import pyautogui
from pywinauto.application import Application
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
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def entrada_de_notas_7139(task):
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

        #Abre um novo emsys
        await kill_process("EMSys")
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

        await worker_sleep(10)

        # Download XML
        get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
        get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        env_config, _ = load_env_config()

        download_result = await download_xml(env_config["XML_DEFAULT_FOLDER"], get_gcp_token, get_gcp_credentials, nota["nfe"])
        if download_result['sucesso'] == True:
            console.log('Download do XML realizado com sucesso', style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{download_result['retorno']}"}

        await get_xml(nota["nfe"])
        await worker_sleep(3)

        # Deleta o xml
        await delete_xml(nota["nfe"])
        
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
                    return {"sucesso": False, "retorno": f"Warning: Erro ao clicar em NO: {e}"}
                await worker_sleep(7)
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
        if cfop == 5104 or str(cfop).startswith("51"):
            combo_box_natureza_operacao = main_window.child_window(class_name="TDBIComboBox", found_index=0)
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1102-COMPRA DE MERCADORIA ADQ. TERCEIROS - 1.102")
            await worker_sleep(3)
        elif cfop == 6102:
            combo_box_natureza_operacao = main_window.child_window(class_name="TDBIComboBox", found_index=0)
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "2102-COMPRA DE MERCADORIAS SEM DIFAL - 2.102")
            await worker_sleep(3)
        else:
            console.print("Erro mapeado, CFOP diferente de 6102 ou 5104/51, necessario ação manual ou ajuste no robo...\n")
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
        console.print("Clicando em OK... \n")
        try:
            btn_ok = main_window.child_window(title="Ok")
            btn_ok.click()
        except:
            btn_ok = main_window.child_window(title="&Ok")
            btn_ok.click()
        await worker_sleep(6)

        console.print("Verificando a existencia de Informations...\n")
        app = Application().connect(title="Information")
        main_window = app["Information"]

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
                console.print(f"Erro ao clicar em NO em information: {e}")
                return {"sucesso": False, "retorno": f"Information: Erro ao clicar em NO: {e}"}
            await worker_sleep(7)
        else:
            console.print("Warning - Erro após a importação do arquivo...\n")
            return {"sucesso": False, "retorno": 'Warning - Erro após a importação do arquivo, não foi encontrado o botão No para andamento do processo... \n'}
        
        await worker_sleep(6)
        while True:
            aguarde_aberta = False
            from pywinauto import Desktop
            for window in Desktop(backend='uia').windows():
                if "Aguarde" in window.window_text():
                    aguarde_aberta = True
                    console.print("A janela 'Aguarde' está aberta. Aguardando...\n")
                    break

            if not aguarde_aberta:
                console.print("A janela 'Aguarde' foi fechada. Continuando para encerramento do processo...\n")
                break

        
        # Inclui registro
        console.print(f"Incluindo registro...\n")
        try:
            ASSETS_PATH = "assets"
            inserir_registro = pyautogui.locateOnScreen(ASSETS_PATH + "\\entrada_notas\\IncluirRegistro.png", confidence=0.8)
            pyautogui.click(inserir_registro)
        except Exception as e:
            console.print(f"Não foi possivel incluir o registro utilizando reconhecimento de imagem, Error: {e}...\n tentando inserir via posição...\n")
            incluir_registro()

        retorno = False
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            window_message = win32clipboard.GetClipboardData().strip()
            win32clipboard.CloseClipboard()
            if 'nota fiscal inclu' in window_message.lower():
                retorno = True
            else:
                retorno = await verify_nf_incuded()
        except:
            retorno = await verify_nf_incuded()

        if retorno:
            console.print("\nNota lançada com sucesso...", style="bold green")
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
