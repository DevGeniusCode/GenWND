from src.window.controls.user import UserControl


class RadioButtonControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for RadioButtonControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'RADIOBUTTON'
            self.properties['NAME'] = 'RadioButton'
            self.properties['STYLE'] = ['RADIOBUTTON', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'HIDDEN', 'IMAGE', 'BORDER']
            self.properties['HEADERTEMPLATE'] = 'LabelRegular'
            self.properties['TEXT'] = 'Radio Button'
            self.properties['attributes'] = {
                'RADIOBUTTONDATA': [{'GROUP': 1}]
            }
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'RadioButtonEnabledLeft', 'COLOR': (1, 1, 1, 160), 'BORDERCOLOR': (47, 55, 168, 255)},
                    {'IMAGE': 'RadioButtonEnabledMiddle', 'COLOR': (128, 0, 0, 0), 'BORDERCOLOR': (0, 0, 0, 0)},
                    {'IMAGE': 'RadioButtonEnabledRight', 'COLOR': (117, 43, 1, 200), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'RadioButtonDisabledLeft', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'RadioButtonDisabledMiddle', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'RadioButtonDisabledRight', 'COLOR': (64, 64, 64, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'RadioButtonEnabledLeft', 'COLOR': (1, 1, 1, 160), 'BORDERCOLOR': (47, 55, 168, 255)},
                    {'IMAGE': 'RadioButtonEnabledMiddle', 'COLOR': (128, 0, 0, 0), 'BORDERCOLOR': (0, 0, 0, 0)},
                    {'IMAGE': 'RadioButtonEnabledRight', 'COLOR': (117, 43, 1, 200), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'RadioButtonHilightedLeft', 'COLOR': (0, 1, 0, 160), 'BORDERCOLOR': (47, 55, 168, 255)},
                    {'IMAGE': 'RadioButtonHilightedMiddle', 'COLOR': (0, 128, 0, 0), 'BORDERCOLOR': (128, 255, 128, 255)},
                    {'IMAGE': 'RadioButtonHilightedRight', 'COLOR': (117, 43, 0, 200), 'BORDERCOLOR': (254, 254, 254, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ]
            }
