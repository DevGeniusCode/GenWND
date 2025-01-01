from src.window.controls.user import UserControl


class ScrollListBoxControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for ScrollListBoxControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'SCROLLLISTBOX'
            self.properties['NAME'] = 'ListBox'
            self.properties['STYLE'] = ['SCROLLLISTBOX', 'MOUSETRACK']
            self.properties['HEADERTEMPLATE'] = 'LabelRegular'
            self.properties['attributes'] = {
                'LISTBOXDATA': [
                    {'LENGTH': 100}, {'AUTOSCROLL': 0},
                    {'AUTOPURGE': 0}, {'SCROLLBAR': 1},
                    {'MULTISELECT': 0}, {'COLUMNS': 2},
                    {'COLUMNSWIDTH': 30}, {'COLUMNSWIDTH': 20},
                    {'FORCESELECT': 1}]
            }
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'BlackSquare', 'COLOR': (0, 0, 0, 126), 'BORDERCOLOR': (49, 55, 168, 255)},
                    {'IMAGE': 'ListBoxHiliteItemLeftEnd', 'COLOR': (255, 255, 0, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'ListBoxHiliteItemRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteItemRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'ListBoxHiliteItemSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 4, 0, 0), 'BORDERCOLOR': (49, 55, 168, 255)},
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
                    {'IMAGE': 'BlackSquare', 'COLOR': (0, 0, 0, 126), 'BORDERCOLOR': (49, 55, 168, 255)},
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
