import os
import sys
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_registry():
    if not is_admin():
        print("Please run this script as Administrator to update the registry.")
        # Re-run as admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    # Get pythonw executable and foldercheck script path
    pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw_path):
        pythonw_path = sys.executable # fallback
        
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "foldercheck.py"))
    
    if not os.path.exists(script_path):
        print(f"Error: Could not find main script at {script_path}")
        return

    # Define ProgID
    prog_id = "FolderCheck.File"
    ext = ".check"

    try:
        # 1. Register ProgID
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, prog_id) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "FolderCheck Checklist")
            
            # Default Icon
            with winreg.CreateKey(key, "DefaultIcon") as icon_key:
                # Using a generic system text/list icon
                winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, f"{sys.executable},0")
                
            # Open Command
            with winreg.CreateKey(key, r"shell\open\command") as cmd_key:
                command = f'"{pythonw_path}" "{script_path}" "%1"'
                winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, command)

        # 2. Register Extension and ShellNew
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, prog_id)
            
            # Add to "New" context menu
            with winreg.CreateKey(key, "ShellNew") as shellnew_key:
                # Initialize new files with valid JSON template
                template_data = '{"items": []}'
                winreg.SetValueEx(shellnew_key, "Data", 0, winreg.REG_SZ, template_data)

        # Notify Explorer of file association changes
        SHCNE_ASSOCCHANGED = 0x08000000
        SHCNF_IDLIST = 0x0000
        ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)

        print("Registry setup complete!")
        print(f"Extension '{ext}' is now associated with FolderCheck.")
        print("You can now right-click in Explorer -> New -> FolderCheck Checklist.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_registry()
    input("Press Enter to exit...")
