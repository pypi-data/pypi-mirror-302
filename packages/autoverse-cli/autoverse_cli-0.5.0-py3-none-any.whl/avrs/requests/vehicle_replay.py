from avrs.requests.request import AvrsApiRequest
from argparse import RawDescriptionHelpFormatter
from argparse import RawTextHelpFormatter

class AvrsVehicleReplayRequests():
    def __init__(self, parser, cfg):
        psr = parser.add_parser('vehicle-replay', help='utilty for recording and replaying vehicle motion')
        sps = psr.add_subparsers(required= True, help='sub-command vehicle-replay')
        SpawnReplayVehicle(sps, cfg)
        StartVehicleReplayRecording(sps, cfg)
        StopVehicleReplayRecording(sps, cfg)

class SpawnReplayVehicle(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'SpawnObject', '')
        psr = parser.add_parser(
            'spawn', help='spawn a vehicle intended to replay motion', formatter_class=RawTextHelpFormatter)

        psr.add_argument(
            'replay_file', 
            default='', 
            help='the replay file to use ("random" for a random profile)')

        psr.add_argument(
            '--name', 
            default='npc0', 
            help='name of the replay vehicle to spawn')

        psr.add_argument(
            '--vehicle-type', 
            default='EAV24', 
            help='what type of vehicle to spawn for replay')

        # psr.add_argument(
        #     '--position', 
        #     choices=('relative', 'absolute'), 
        #     default='absolute', 
        #     help=NPC_SPAWN_POSITION_HELP)


        # psr.add_argument(
        #     '--velocity-type', 
        #     default='constant', 
        #     help='the path the NPC follows is a constant velocity or speed')

        # psr.add_argument(
        #     '--speed', 
        #     type=float, 
        #     default=20, 
        #     help='the speed of the npc is m/s')

        psr.add_argument(
            '--rate', 
            type=float, 
            default=1.0, 
            help='the playback rate, 1.0 is normal')

        psr.add_argument(
            '--random-start',
            action='store_true',
            help='if set, will start at a random point in the replay')

        psr.add_argument(
            '--relative-dist', 
            type=float, 
            default=40.0, 
            help='the distance relative to ego to start the playback (-1 to start at playback start)')

        psr.add_argument(
            '--auto-start',
            action='store_true',
            help='if set, the npc will begin moving immediately')

        # psr.add_argument(
        #     '--enable-sensors', 
        #     type=bool, 
        #     default=False, 
        #     help='whether to enable sensors on the replay vehicle')

        psr.add_argument(
            '--with-view-cameras',
            action='store_true',
            help='if set, will attach viewing cameras to the replay vehicle')
        
        psr.set_defaults(func=self.send_request)
    

    def get_request_body(self, args):

        replay_ipd = {
            'bEnableRecording': False,
            'bRecordOnPhysicsTick': False,
            'recordMotionMinSpeedThreshold': 0.01,
            'bEnableReplay': True,
            'bApplyInitialConfig': True,
            'initialConfig': {
                'playRate': args.rate,
                'profile': args.replay_file,
                'bUseRandomProfile': args.replay_file == 'random',
                'replayAction': 'start' if args.auto_start else '',
                'bStartReplayAtRandomTime': args.random_start,
                'relativeDistance': args.relative_dist
            }
        }

        eav_init_pld = {
            "bEnableBsuCan": False,
            "bEnableKistlerCan": False,
            "bEnableBadeniaCan": False,
            "bHudEnabled": False,
            "bLidarEnabled": False,
            "bCameraEnabled": False,
            "bPublishInputs": False,
            "bPublishGroundTruth": False
        }

        plds = [
            {
                'TypeName': 'WheeledVehicleReplayIpd',
                'Body': replay_ipd
            },
            {
                'TypeName': 'Eav24Initializer',
                'Body': eav_init_pld
            }
        ]

        if args.with_view_cameras:
            plds.append(
                {
                    'TypeName': 'InitializerTemplates',
                    'Body': {
                        'Templates': [
                            {
                                'PayloadType': 'SimViewTargetIpd',
                                'PayloadSpec': 'DefaultCarCams'
                            }
                        ]
                    }
                })

        return {
            'Name': args.name,
            'Type': args.vehicle_type,
            'Location': {},
            'Rotation': {},
            'Payloads': plds
        }

class StartVehicleReplayRecording(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'ConfigureVehicleReplay', 'Ego')
        psr = parser.add_parser(
            'start-recording', help='begin recording vehicle motion', formatter_class=RawTextHelpFormatter)

        psr.add_argument(
            'out_file',
            help='the file name to use for the saved recording')

        psr.add_argument(
            '--rate-hz',
            type=float,
            default=100.0, 
            help='the rate to record vehicle motion. high rates will produce large files')

        psr.set_defaults(func=self.send_request)
    

    def get_request_body(self, args):
        return {
            'PlayRate': -1.0,
            'profile': '',
            'replayAction': '',
            #'teleportLocation': '',
            'recordAction': 'start',
            'recordFileName': args.out_file,
            'recordRateHz': args.rate_hz
        }

class StopVehicleReplayRecording(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'ConfigureVehicleReplay', 'Ego')
        psr = parser.add_parser(
            'stop-recording', help='begin recording vehicle motion', formatter_class=RawTextHelpFormatter)
        psr.set_defaults(func=self.send_request)
    

    def get_request_body(self, args):
        return {
            'recordAction': 'stop',
        }
