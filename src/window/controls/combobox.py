from src.window.controls.user import UserControl


class ComboBoxControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for ComboBoxControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'COMBOBOX'
            self.properties['NAME'] = 'ComboBox'
            self.properties['STYLE'] = ['COMBOBOX', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'IMAGE']
            self.properties['HEADERTEMPLATE'] = 'ComboBoxEntry'
            self.properties['TOOLTIPTEXT'] = 'TOOLTIP:LanIP'
            self.properties['attributes'] = {
                'COMBOBOXDATA': [{'ISEDITABLE': 0}, {'MAXCHARS': 16}, {'MAXDISPLAY': 2}, {'ASCIIONLY': 0}, {'LETTERSANDNUMBERS': 0}]
            }
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (47, 55, 168, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemLeftEnd', 'COLOR': (254, 254, 254, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXDROPDOWNBUTTONENABLEDDRAWDATA': [
                    {'IMAGE': 'VSliderDownButtonEnabled', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'VSliderDownButtonHiliteSelected', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXDROPDOWNBUTTONDISABLEDDRAWDATA': [
                    {'IMAGE': 'VSliderDownButtonDisabled', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (128, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXDROPDOWNBUTTONHILITEDRAWDATA': [
                    {'IMAGE': 'VSliderDownButtonHilite', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'VSliderDownButtonHiliteSelected', 'COLOR': (254, 254, 254, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXEDITBOXENABLEDDRAWDATA': [
                    {'IMAGE': 'TextEntryEnabledLeftEnd', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'TextEntryEnabledRightEnd', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'TextEntryEnabledRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryEnabledSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXEDITBOXDISABLEDDRAWDATA': [
                    {'IMAGE': 'TextEntryDisabledLeftEnd', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (0, 0, 0, 255)},
                    {'IMAGE': 'TextEntryDisabledRightEnd', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'TextEntryDisabledRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryDisabledSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXEDITBOXHILITEDRAWDATA': [
                    {'IMAGE': 'TextEntryHiliteLeftEnd', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'TextEntryHiliteRightEnd', 'COLOR': (254, 254, 254, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'TextEntryHiliteRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryHiliteSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXLISTBOXENABLEDDRAWDATA': [
                    {'IMAGE': 'BlackSquare', 'COLOR': (0, 0, 0, 255), 'BORDERCOLOR': (49, 55, 168, 255)},
                    {'IMAGE': 'ListBoxHiliteItemLeftEnd', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'ListBoxHiliteItemRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteItemRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteItemSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXLISTBOXDISABLEDDRAWDATA': [
                    {'IMAGE': 'BlackSquare', 'COLOR': (0, 0, 0, 255), 'BORDERCOLOR': (49, 55, 168, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'COMBOBOXLISTBOXHILITEDRAWDATA': [
                    {'IMAGE': 'BlackSquare', 'COLOR': (0, 0, 0, 255), 'BORDERCOLOR': (49, 55, 168, 255)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemLeftEnd', 'COLOR': (254, 254, 254, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteSelectedItemSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXENABLEDUPBUTTONDRAWDATA': [
                    {'IMAGE': 'VSliderUpButtonEnabled', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'VSliderUpButtonHiliteSelected', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXDISABLEDUPBUTTONDRAWDATA': [
                    {'IMAGE': 'VSliderUpButtonDisabled', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXHILITEUPBUTTONDRAWDATA': [
                    {'IMAGE': 'VSliderUpButtonHilite', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'VSliderUpButtonHiliteSelected', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXENABLEDDOWNBUTTONDRAWDATA': [
                    {'IMAGE': 'VSliderDownButtonEnabled', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'VSliderDownButtonHiliteSelected', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXDISABLEDDOWNBUTTONDRAWDATA': [
                    {'IMAGE': 'VSliderDownButtonDisabled', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXHILITEDOWNBUTTONDRAWDATA': [
                    {'IMAGE': 'VSliderDownButtonHilite', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'VSliderDownButtonHiliteSelected', 'COLOR': (254, 254, 254, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXENABLEDSLIDERDRAWDATA': [
                    {'IMAGE': 'VSliderEnabledTopEnd', 'COLOR': (255, 190, 0, 0), 'BORDERCOLOR': (47, 55, 168, 255)},
                    {'IMAGE': 'VSliderEnabledBottomEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'VSliderEnabledRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'VSliderEnabledSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXDISABLEDSLIDERDRAWDATA': [
                    {'IMAGE': 'VSliderDisabledTopEnd', 'COLOR': (128, 128, 128, 0), 'BORDERCOLOR': (148, 112, 0, 255)},
                    {'IMAGE': 'VSliderDisabledBottomEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'VSliderDisabledRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'VSliderDisabledSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'LISTBOXHILITESLIDERDRAWDATA': [
                    {'IMAGE': 'VSliderHiliteTopEnd', 'COLOR': (0, 255, 0, 0), 'BORDERCOLOR': (49, 55, 168, 255)},
                    {'IMAGE': 'VSliderHiliteBottomEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'VSliderHiliteRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'VSliderHiliteSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'SLIDERTHUMBENABLEDDRAWDATA': [
                    {'IMAGE': 'ScrollBarThumbEnabled', 'COLOR': (255, 4, 0, 0), 'BORDERCOLOR': (255, 243, 28, 255)},
                    {'IMAGE': 'ScrollBarThumbHiliteSelected', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'SLIDERTHUMBDISABLEDDRAWDATA': [
                    {'IMAGE': 'ScrollBarThumbDisabled', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'SLIDERTHUMBHILITEDRAWDATA': [
                    {'IMAGE': 'ScrollBarThumbHilite', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'ScrollBarThumbHiliteSelected', 'COLOR': (254, 254, 254, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ]
            }
