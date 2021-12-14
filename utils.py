import json
import subprocess
import time
from pathlib import Path
import logging
from DownloadGUI import startGUI
from multiprocessing import Process

class Data:
    """
    Program içerisinde geçici olarak tutulacak verileri tutar
    """
    boards  = {}
    threads = []
    config = {}
    websockets = []
    processes = []

def executeCli(command:str) -> str:
    """
    verilen komutu çalıştırır, komut bitene kadar programı bekletir ve çıktıyı döner.


    command(str): cmd'ye yazılacak komut, arduino-cli kısmı hariç

    bknz: executeCli("config init") --> cmd ekranına "arduino-cli config init" yazdıracaktır
    """
    logging.info(f"Executing command arduino-cli {command}")
    returnString = subprocess.check_output(f"arduino-cli {command}", shell=True)
    return returnString.decode("utf-8")

def executeCliPipe(command:str) -> subprocess.PIPE:
    """
    verilen komutu çalıştırır, komutun bitmesini beklemez, komutun çalıştığı process ile olan pipe'ı döner.


    command(str): cmd'ye yazılacak komut, arduino-cli kısmı hariç

    bknz: executeCli("config init") --> cmd ekranına "arduino-cli config init" yazdıracaktır
    """
    logging.info(f"Executing pipe command arduino-cli {command}")
    pipe = subprocess.Popen(f"arduino-cli {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return pipe

def evaluatePipe(pipe: subprocess.PIPE) -> bool:
    t = pipe.communicate()[1].decode("utf-8")
    if t:
        logging.critical(t)
        process.terminate()
        return False
    return True
    #TODO if there is no error, return output, so instead of f() -> bool f() -> bool, string

def createFolder(fileDir:str) -> None:
    """
    Yeni klasör oluşturur. Eğer var ise, bir değişiklik yapmaz


    fileDir(str):oluşturulacak klasörün yolu
    """
    logging.info(f"Creating folder {fileDir}")
    Path(fileDir).mkdir(parents=True, exist_ok=True)

def createInoFile(code:str) -> None:
    """
    .ino dosyasını geçici klasörün içerisine oluşturur.


    code(str): kayıt edilecek kod
    """
    tempPath = Data.config["TEMP_PATH"]
    logging.info(f"Creating Ino file at {tempPath}")
    createFolder(tempPath)
    createFolder(f"{tempPath}/tempCode")
    with open(f"{tempPath}/tempCode/tempCode.ino", "w") as inoFile:
        inoFile.writelines(code)
        logging.info(f"File created")


def setupDeneyap() -> bool:
    """
    Program ilk yüklendiğinde çalıştırılır, arduino-cli'in konfigurasyonunu yapar, deneyap kartı arduino-cli'a ekler ve yükler.
    """

    process = Process(target=startGUI)
    process.start()

    try:
        executeCli("config init")
    except:
        logging.info(f"Init file does exist skipping this step")
    else:
        logging.info(f"Init file created")

    string = executeCli("config dump")
    if not ("deneyapkart" in string):
        logging.info("package_deneyapkart_index.json is not found on config, adding it")
        executeCli("config add board_manager.additional_urls https://raw.githubusercontent.com/deneyapkart/deneyapkart-arduino-core/master/package_deneyapkart_index.json")
        logging.info("added package_deneyapkart_index.json to config")

    else:
        logging.info("package_deneyapkart_index.json is found on config skipping this step")

    pipe = executeCliPipe("core install deneyap:esp32@1.3.2")
    t = pipe.communicate()[1].decode("utf-8")
    if t:
        logging.critical(t)
        process.terminate()
        return False

    pipe = executeCliPipe("lib install Stepper IRremote")
    t = pipe.communicate()[1].decode("utf-8")
    if t:
        logging.critical(t)
        process.terminate()
        return False
    """
    pipe = executeCliPipe("config set library.enable_unsafe_install true")
    t = pipe.communicate()[1].decode("utf-8")
    if t:
        logging.critical(t)
        process.terminate()
        return False

    pipe = executeCliPipe("lib install --zip-path libzips/Tone32.zip")
    t = pipe.communicate()[1].decode("utf-8")
    if t:
        logging.critical(t)
        process.terminate()
        return False
    """
    Data.config['runSetup'] = False
    configDataString = json.dumps(Data.config)
    with open(f"{Data.config['CONFIG_PATH']}\config.json", 'w') as configFile:
        logging.info(f"Config File Changed")
        configFile.write(configDataString)

    process.terminate()
    return True

