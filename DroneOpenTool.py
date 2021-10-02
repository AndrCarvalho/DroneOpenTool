import argparse
import os

from OfflineRun import offline_runner
from OnlineRun import online_runner


def main(workspace, name, start, goal, planner, output, gran, margin, restr, area, weight):
    print(workspace)

    if planner == "Online":
        online_runner(str(workspace + '\\' + name),
                      (float(start[1:-1].split(',')[0]), float(start[1:-1].split(',')[1])),
                      (float(goal[1:-1].split(',')[0]), float(goal[1:-1].split(',')[1])), gran, margin, restr, weight,
                      output)
    elif planner == "Offline":
        offline_runner(str(workspace + '\\' + name),
                       (float(start[1:-1].split(',')[0]), float(start[1:-1].split(',')[1])),
                       (float(goal[1:-1].split(',')[0]), float(goal[1:-1].split(',')[1])), gran, margin, restr, area,
                       weight, output)
    else:
        print("Error: Planner not available.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DroneOpenTool: Create and Plan your drone mission.')
    m_details = parser.add_argument_group(title="Mission details", description=None)
    m_details.add_argument('--outputPath', metavar='path', required=False, default="",
                           help='the path to workspace')
    m_details.add_argument('--mission', metavar='name', required=True,
                           help='name to the mission')
    m_details.add_argument('--start', metavar='start', required=True,
                           help='starting location: (lat, lon)')
    m_details.add_argument('--goal', metavar='goal', required=True,
                           help='ending location: (lat, lon)')
    m_details.add_argument('--planner', metavar='planner', required=False, choices=['Online', 'Offline'],
                           help='planner type: Online, Offline')
    m_details.add_argument('--output', metavar='output', required=False,
                           help='output type [default: Html]')

    c_params = parser.add_argument_group(title="Computation Parameters", description=None)
    c_params.add_argument('--gran', metavar='granularity', required=True, type=int,
                          help='trajectory granularity')
    c_params.add_argument('--margin', metavar='marginlvl', required=True, type=int,
                          help='level of margin to obstacles')
    c_params.add_argument('--restr', metavar='restrictions', required=True,
                          choices=['buildings', 'airways', 'residential', 'water', 'woods', 'military'], nargs="+",
                          type=str,
                          help="list of restriction type e.g.['buildings',  'airways', 'residential', 'water', "
                               "'woods', 'military'] (you  can add multiple restrictions after --restr)")
    c_params.add_argument('--area', metavar='area', required=False,
                          help="custom defined rectangular area: (south,west,north,east)")
    c_params.add_argument('--obs_weight', metavar='weight', required=False, type=int, default=10000,
                          help="obstacle's weight")

    args = parser.parse_args()
    main(workspace=args.outputPath, name=args.mission, start=args.start, goal=args.goal, planner=args.planner,
         output=args.output, gran=args.gran, margin=args.margin, restr=args.restr, area=args.area,
         weight=args.obs_weight)
