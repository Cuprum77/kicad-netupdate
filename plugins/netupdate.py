import os
import pcbnew
import json
import wx
import os
from glob import glob


class netupdate(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "NetUpdate"
        self.category = "Modify PCB"
        self.description = "Updates the netclasses in the .kicad_pro file to match the schematic colors."
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./resources/icon.png")


    def find_pro_file(self, pcb_path):
        pcb_dir = os.path.dirname(pcb_path)
        pcb_dir = os.path.join(pcb_dir, "*.kicad_pro") 
        files = glob(pcb_dir)
        file = files[0] if files else None

        return file


    def update_kicad_pro(self, file_path, board):
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'net_settings' in data and 'classes' in data['net_settings']:
            classes = data['net_settings']['classes']

            for class_item in classes:
                for class_item in classes:
                    if 'schematic_color' in class_item and 'pcb_color' in class_item:
                        class_item['pcb_color'] = class_item['schematic_color']

                    # Write the updated data back to the file
                    with open(file_path, 'w') as file:
                        json.dump(data, file, indent=2)

            self.show_message_box("Success", f"Update completed!\nPlease completely close down KiCad and reopen it to see the changes.")
        else:
            self.show_message_box("Error", "Could not find net_settings.classes in the file structure.")


    def show_message_box(self, header, message):
        dlg = wx.MessageDialog(None, message, header, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def Run(self):
        board = pcbnew.GetBoard()
        pcb_path = board.GetFileName()

        if not pcb_path:
            self.show_message_box("Error", "Please save the board before running this plugin.")
            return
        
        pro_file = self.find_pro_file(pcb_path)

        if not pro_file:
            self.show_message_box("Error", "Could not find the .kicad_pro file.")
            return

        self.update_kicad_pro(pro_file, board)
                

netupdate().register()