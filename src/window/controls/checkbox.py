from src.window.controls.user import UserControl


class CheckBoxControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for CheckBoxControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'CHECKBOX'
            self.properties['NAME'] = 'CheckBox'
            self.properties['STYLE'] = ['CHECKBOX', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'IMAGE', 'BORDER']
            self.properties['HEADERTEMPLATE'] = 'LabelRegular'
            self.properties['TEXT'] = 'CheckBox'
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'Active-Unchecked', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'Active-Checked', 'COLOR': (0, 0, 255, 255), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'Disabled-Unchecked', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'Disabled-Checked', 'COLOR': (64, 64, 64, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (128, 255, 128, 255)},
                    {'IMAGE': 'Active-HiLighted', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'Active-Checked', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                ]
            }
