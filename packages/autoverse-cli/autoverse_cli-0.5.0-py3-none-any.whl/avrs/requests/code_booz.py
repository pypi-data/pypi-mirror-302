from avrs.requests.request import AvrsApiRequest
from argparse import RawTextHelpFormatter

class AvrsCodeBoozRequest():
    def __init__(self, parent_parser, cfg):
        psr = parent_parser.add_parser(
            'lwi', 
            help='light-weight interface logging options\n\n')
        sps = psr.add_subparsers(required=True, help='light-wieght interface logging options')

        AvrsCodeBoozStartLogging(sps, cfg)
        AvrsCodeBoozStopLogging(sps, cfg)
        AvrsCodeBoozGetTimes(sps, cfg)

class AvrsCodeBoozStartLogging(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'CodeBoozLog', 'Ego')
        psr = parser.add_parser(
            'start-log', help='starts logging', formatter_class=RawTextHelpFormatter)

        psr.add_argument(
            'out_file', 
            help='the name of the log file to create (within the \"Saved\" directory)')

        psr.add_argument(
            '--format', choices=('binary', 'csv'), default='binary', help='the format to save logged data')

        psr.add_argument(
            '--rate-hz', type=float, default=100.0, help='the rate in hz to log data')

        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
            'Action': 'Start',
            'FileName': args.out_file,
            'RateHz': args.rate_hz,
            'Format': args.format
        }

class AvrsCodeBoozStopLogging(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'CodeBoozLog', 'Ego')
        psr = parser.add_parser(
            'stop-log', help='starts logging', formatter_class=RawTextHelpFormatter)

        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
            'Action': 'Stop'
        }

class AvrsCodeBoozGetTimes(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'CodeBoozLog', 'Ego')
        psr = parser.add_parser(
            'get-times', help='starts logging', formatter_class=RawTextHelpFormatter)

        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
            'Action': 'GetTimes'
        }