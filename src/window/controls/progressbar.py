from src.window.controls.user import UserControl


class ProgressBarControl(UserControl):
    def __init__(self, window_uuid, properties=None, children=None, file_name=None):
        super().__init__(window_uuid, properties, children, file_name)
        # Assign default values for ProgressBarControl
        if properties:
           self.properties.update(properties)
        else:
            self.properties['WINDOWTYPE'] = 'PROGRESSBAR'
            self.properties['NAME'] = 'ProgressBar'
            self.properties['STYLE'] = ['PROGRESSBAR', 'MOUSETRACK']
            self.properties['STATUS'] = ['ENABLED', 'IMAGE']
            self.properties['textures'] = {
                'ENABLEDDRAWDATA': [
                    {'IMAGE': 'LoadingBar_L', 'COLOR': (255, 0, 0, 255), 'BORDERCOLOR': (255, 128, 128, 255)},
                    {'IMAGE': 'LoadingBar_R', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'LoadingBar_C', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (47, 55, 168, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'LoadingBar_DePowered', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'LoadingBar_Progress', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ],
                'DISABLEDDRAWDATA': [
                    {'IMAGE': 'NoImage', 'COLOR': (64, 64, 64, 255), 'BORDERCOLOR': (192, 192, 192, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (192, 192, 192, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
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
                    {'IMAGE': 'NoImage', 'COLOR': (47, 55, 168, 255), 'BORDERCOLOR': (254, 254, 254, 255)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)},
                    {'IMAGE': 'NoImage', 'COLOR': (255, 255, 255, 0), 'BORDERCOLOR': (255, 255, 255, 0)}
                ]
            }
