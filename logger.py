import logging
import os

rutaLog = os.path.join(os.getcwd(), "log\\ejemploLog.log")
#print("miRuta:", rutaLog)

logging.basicConfig(
    level=logging.INFO #indica desde cuales son los errores que se estaran mostrando en consola o guardando en el archivo .log, se basa en el nivel de severidad (se debe usar el parametro en mayusculas)
    , filename=rutaLog #indica que el log se estara guardando en este archivo
    , filemode="a" # "a" (append) opcion default, indica que si el archivo ya existe añade los registros de log, 
                   # "w" (write) indica que el archivo se sobreescribira
    , format="%(asctime)s - %(levelname)s - %(message)s" #podemos cambiar el formato con el que se muestran los logs por default
    , datefmt="%D %H:%M:%S" #muestra la hora
    #, datefmt="%D" #muestra fecha dd/mm/yyyy
    )

def escribirLog(mensaje):
    logging.info(mensaje)

def escribirLogError(mensaje):
    logging.error(mensaje)


