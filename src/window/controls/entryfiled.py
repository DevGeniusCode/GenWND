from src.window.controls.user import UserControl


class EntryFieldControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for EntryFieldControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'ENTRYFIELD'
            self.properties['NAME'] = 'TextEntry'
            self.properties['STYLE'] = ['ENTRYFIELD', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'IMAGE']
            self.properties['HEADERTEMPLATE'] = 'TextEntry'
            self.properties['TEXT'] = 'Entry'
            self.properties['attributes'] = {
                'TEXTENTRYDATA': [
                    {'MAXLEN': 64}, {'SECRETTEXT': 0}, {'NUMERICALONLY': 0}, {'ALPHANUMERICALONLY': 0}, {'ASCIIONLY': 1}]
            }
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'TextEntryEnabledLeftEnd', 'COLOR': (0, 0, 0, 255), 'BORDERCOLOR': (0, 0, 0, 255)},
                    {'IMAGE': 'TextEntryEnabledRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryEnabledRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryEnabledSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0),'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'TextEntryDisabledLeftEnd', 'COLOR': (0, 0, 128, 255), 'BORDERCOLOR': (0, 0, 0, 255)},
                    {'IMAGE': 'TextEntryDisabledRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryDisabledRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryDisabledSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                ],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'TextEntryHiliteLeftEnd', 'COLOR': (0, 0, 0, 255), 'BORDERCOLOR': (0, 0, 0, 255)},
                    {'IMAGE': 'TextEntryHiliteRightEnd', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryHiliteRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'TextEntryHiliteSmallRepeatingCenter', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ]
            }
