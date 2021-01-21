#!/usr/bin/python


import rospy
import rosbag
import os
import sys
import argparse




def change_frame_id(inbag,outbag):
  rospy.loginfo('   Processing input bagfile: %s', inbag)
  rospy.loginfo('  Writing to output bagfile: %s', outbag)


  outbag = rosbag.Bag(outbag,'w')

  start_time = rospy.Duration(rosbag.Bag(inbag,'r').get_start_time()-0.1)
  print('start time', start_time)
  
  for topic, msg, t, conn_header in rosbag.Bag(inbag,'r').read_messages(return_connection_header=True):
    if msg._has_header:
      msg.header.stamp = msg.header.stamp - start_time
    if topic == "/tf" or topic == "/tf_static":
        for transform in msg.transforms:
          transform.header.stamp = transform.header.stamp - start_time

    outbag.write(topic, msg, t- start_time, connection_header=conn_header)
  rospy.loginfo('Closing output bagfile and exit...')
  outbag.close()

if __name__ == "__main__":
  rospy.init_node('change_frame_id')
  parser = argparse.ArgumentParser(
      description='reate a new bagfile from an existing one replacing the frame id of requested topics.')
  parser.add_argument('-o', metavar='OUTPUT_BAGFILE', required=True, help='output bagfile')
  parser.add_argument('-i', metavar='INPUT_BAGFILE', required=True, help='input bagfile')
  args = parser.parse_args()

  try:
    change_frame_id(args.i,args.o)
  except Exception, e:
    import traceback
    traceback.print_exc()