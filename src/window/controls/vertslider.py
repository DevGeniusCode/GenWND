from src.window.controls.user import UserControl


class VertSliderControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None):
        super().__init__(window_uuid, properties, children)
        # Assign default values for VertSliderControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'VERTSLIDER'
            self.properties['NAME'] = 'VertSlider'
            self.properties['STYLE'] = ['VERTSLIDER', 'MOUSETRACK']
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
                    {'IMAGE': 'NoImage', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (64, 64, 64, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
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
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'SLIDERTHUMBENABLEDDRAWDATA': [
                    {'IMAGE': 'WindowResizeEnabled', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'WindowResizePushed', 'COLOR': (128, 128, 128, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'SLIDERTHUMBDISABLEDDRAWDATA': [
                    {'IMAGE': 'WindowResizeDisabled', 'COLOR': (64, 64, 64, 255), 'BORDERCOLOR': (128, 128, 128, 255)},
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
                    {'IMAGE': 'WindowResizeHilite', 'COLOR': (0, 255, 0, 255), 'BORDERCOLOR': (128, 255, 128, 255)},
                    {'IMAGE': 'WindowResizePushed', 'COLOR': (0, 0, 255, 255), 'BORDERCOLOR': (128, 128, 255, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ]
            }
