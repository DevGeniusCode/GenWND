from src.window.controls.user import UserControl


class HorzSliderControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for HorzSliderControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'HORZSLIDER'
            self.properties['NAME'] = 'HorzSlider'
            self.properties['STYLE'] = ['HORZSLIDER', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'IMAGE', 'TABSTOP']
            self.properties['attributes'] = {
                'SLIDERDATA': [{'MINVALUE': 1}, {'MAXVALUE': 10}]
            }
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'hilightedbox', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (64, 64, 64, 255)},
                    {'IMAGE': 'dehilightedbox', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)}
                ],
                'HILITEDRAWDATA': [
                    {'IMAGE': 'linebox', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'arrow', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)}
                ],
                'SLIDERTHUMBENABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (255, 128, 128, 255), 'BORDERCOLOR': (255, 0, 0, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                ],
                'SLIDERTHUMBDISABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (64, 64, 64, 255), 'BORDERCOLOR': (128, 128, 128, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (0, 0, 0, 255), 'BORDERCOLOR': (64, 64, 64, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)}
                ],
                'SLIDERTHUMBHILITEDRAWDATA': [
                    {'IMAGE': 'arrow', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (0, 128, 0, 255)},
                    {'IMAGE': 'arrow', 'COLOR': (0, 0, 255, 255), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 255), 'BORDERCOLOR': (255, 255, 255, 255)}
                ]
            }
