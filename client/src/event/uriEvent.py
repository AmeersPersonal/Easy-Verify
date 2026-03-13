import winreg, os, sys


def is_uri_registered(name:str, cmd:str)-> bool:

    """
    On launch this will check if the uri registred
    The return value is a boolean
    this function will be only probaly used in register_uri function
    """

    
    cmd_path  = rf"Software\Classes\{name}\shell\open\command"
    
    try:

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cmd_path) as current_key: # checks if path exists
           current = winreg.QueryValue(current_key, "")
           if current == cmd: #cchecks if the cmd exists
               return True
    
    except(FileNotFoundError, OSError):
        pass
    else:
        return False


def register_uri(name:str, path:str)->None:
    """
    registers the uri
   
    """

    python_ex = sys.executable
    cmd1 = f'"{os.path.abspath(path)}" "%1"'
    key_path = rf"Software\Classes\{name}"

    if is_uri_registered(name, cmd1):
        print("Uri Exists")
        return
    
    try:
        #root stuff
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f"URL:{name} Protocol" )
            winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

        #cmd
        cmd_path  = rf"Software\Classes\{name}\shell\open\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_path) as key:
            winreg.SetValue(key,"", winreg.REG_SZ, cmd1)
        print("test")


    except Exception:
        print("Test 2")
        return
    

