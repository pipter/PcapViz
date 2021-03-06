from argparse import ArgumentParser

from pcapviz.core import GraphManager
from pcapviz.sources import ScapySource

if __name__ == '__main__':

    parser = ArgumentParser(description='pcap topology drawer')
    parser.add_argument('-i', '--pcaps', nargs='*', help='capture files to be analyzed')
    parser.add_argument('-o', '--out', help='topology will be stored in the specified file')
    parser.add_argument('-g', '--graphviz', help='graph will be exported to the specified file (dot format)')
    parser.add_argument('--layer2', action='store_true', help='create layer2 topology')
    parser.add_argument('--layer3', action='store_true', help='create layer3 topology')
    parser.add_argument('--layer4', action='store_true', help='create layer4 topology')
    #parser.add_argument('-e', '--exclude', nargs='*', help='exclude nodes from analysis')
    parser.add_argument('-fi', '--frequent-in', action='store_true', help='print frequently contacted nodes to stdout')
    parser.add_argument('-fo', '--frequent-out', action='store_true', help='print frequent source nodes to stdout')

    args = parser.parse_args()

    if args.pcaps:
        packets = ScapySource.load(args.pcaps)

        #if args.exclude:
        #    packet_ls = exclude_ips(packet_lists=packet_ls, ips=args.exclude)
        if args.layer2:
            layer = 2
        elif args.layer3:
            layer = 3
        elif args.layer4:
            layer = 4
        else:
            layer = 3

        g = GraphManager(packets, layer=layer)

        if args.out:
            g.draw(filename=args.out)

        if args.frequent_in:
            g.get_in_degree()

        if args.frequent_out:
            g.get_out_degree()

        if args.graphviz:
            g.get_graphviz_format(args.graphviz)