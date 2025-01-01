from src.window.controls.user import UserControl


class PushButtonControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for ButtonControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'PUSHBUTTON'
            self.properties['NAME'] = 'Button'
            self.properties['STYLE'] = ['PUSHBUTTON', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'IMAGE']
            self.properties['HEADERTEMPLATE'] = 'MainButton'
            self.properties['TEXT'] = 'Button'
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'Buttons-Left', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (47, 55, 168, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-Middle', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-Right', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'Buttons-Disabled-Left', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (128, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-Disabled-Middle', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-Disabled-Right', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                ],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'Buttons-HiLite-Left', 'COLOR': (209, 253, 4, 255), 'BORDERCOLOR': (59, 60, 52, 255)},
                    {'IMAGE': 'Buttons-Pushed-Left', 'COLOR': (47, 55, 168, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-Pushed-Middle', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-Pushed-Right', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-HiLite-Middle', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'Buttons-HiLite-Right', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                ]
            }
