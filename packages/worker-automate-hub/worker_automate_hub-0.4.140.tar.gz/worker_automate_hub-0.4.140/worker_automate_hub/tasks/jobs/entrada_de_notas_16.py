import asyncio
import warnings

import pyautogui
from pywinauto.application import Application
from pywinauto_recorder.player import (
    set_combobox,
)
from rich.console import Console
from worker_automate_hub.api.client import sync_get_config_by_name

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    import_nfe,
    kill_process,
    login_emsys,
    type_text_into_field,
    set_variable,
    worker_sleep,
)
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

pyautogui.PAUSE = 0.5
console = Console()

emsys = EMSys()

async def entrada_de_notas_16(task):
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
            await worker_sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login
        
        await worker_sleep(10)

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
            return {"sucesso": False, "retorno": f"{import_nfe['retorno']}"}

        await worker_sleep(10)

        # Download XML
        get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
        get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        env_config, _ = load_env_config()

        # await emsys.download_xml(env_config["XML_DEFAULT_FOLDER"], get_gcp_token, get_gcp_credentials, nota["nfe"])

         # Permanece 'XML'
        #Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        await worker_sleep(3)

        # Click Downloads
        await emsys.get_xml(nota["nfe"])
        await worker_sleep(30)

        app = Application().connect(title="Informações para importação da Nota Fiscal Eletrônica")
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        if nota["cfop"]:
            console.print(f"Inserindo a informação da CFOP, caso se aplique {nota["cfop"]} ...\n")
            if nota["cfop"] != "5910":
                combo_box_natureza_operacao = main_window.child_window(class_name="TDBIComboBox", found_index=0)
                combo_box_natureza_operacao.click()
                await worker_sleep(3)
                set_combobox("||List", "1403 - COMPRA DE MERCADORIAS- 1.403")
                await worker_sleep(3)
            else:
                combo_box_natureza_operacao = main_window.child_window(class_name="TDBIComboBox", found_index=0)
                combo_box_natureza_operacao.click()
                await worker_sleep(3)
                set_combobox("||List", "1910 - ENTRADA DE BONIFICACAO- COM ESTOQUE- 1910")
                await worker_sleep(3)

        #INTERAGINDO COM O CAMPO ALMOXARIFADO
        filial_empresa_origem = nota["filialEmpresaOrigem"]
        valor_almoxarifado = filial_empresa_origem + "50"
        pyautogui.press('tab')
        pyautogui.write(valor_almoxarifado)
        await worker_sleep(2)
        pyautogui.press('tab')

        await worker_sleep(3)
        #INTERAGINDO COM CHECKBOX Utilizar unidade de agrupamento dos itens
        fornecedor = nota["nomeFornecedor"]
        console.print(f"Fornecedor: {fornecedor} ...\n")
        console.print(f"Sim, nota emitida para: {fornecedor}, marcando o agrupar por unidade de medida...\n")
        checkbox = main_window.child_window(
            title="Utilizar unidade de agrupamento dos itens",
            class_name="TCheckBox",
        )
        if not checkbox.is_checked():
            checkbox.check()
            console.print("Realizado o agrupamento por unidade de medida... \n")

        await worker_sleep(5)
        console.print("Clicando em OK... \n")
        btn_ok = main_window.child_window(title="Ok")
        btn_ok.set_focus()
        btn_ok.click()
        await worker_sleep(15)

        await emsys.verify_warning_and_error("Information", "&No")

        await worker_sleep(10)
        # await emsys.percorrer_grid()
        await emsys.select_tipo_cobranca()
        await emsys.inserir_vencimento_e_valor(nota["dataVencimento"], nota["valorNota"])
        await worker_sleep(5)
        await emsys.incluir_registro()
        await worker_sleep(5)
        await emsys.verify_warning_and_error("Warning", "OK")
        await worker_sleep(5)
        resultado = await emsys.verify_max_vatiation()

        if resultado["sucesso"] == False:
            return resultado
        
        await emsys.incluir_registro()

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}
