#!/usr/bin/python


import rospy
import rosbag
import os
import sys
import argparse


def merge_header(ns, frame_id):
    if frame_id.startswith('/'):
        return ns + frame_id
    else:
        return ns + '/' + frame_id

def change_frame_id(inbag,outbag,frame_id):
  rospy.loginfo('   Processing input bagfile: %s', inbag)
  rospy.loginfo('  Writing to output bagfile: %s', outbag)
  rospy.loginfo('           Writing frame_id: %s', frame_id)

  outbag = rosbag.Bag(outbag,'w')

  for topic, msg, t, conn_header in rosbag.Bag(inbag,'r').read_messages(return_connection_header=True):
    if msg._has_header:
        msg.header.frame_id = merge_header(frame_id, msg.header.frame_id)
        #msg.header.stamp = msg.header.stamp + rospy.Duration(1831.72)
    if topic == "/tf" or topic == "/tf_static":
        # if topic == "/tf_static":
        #     print conn_header
        for transform in msg.transforms:
            transform.header.frame_id = merge_header(frame_id, transform.header.frame_id)
            #transform.header.stamp = transform.header.stamp + rospy.Duration(1831.72)
            transform.child_frame_id = merge_header(frame_id, transform.child_frame_id)
    else:
       topic = frame_id + topic
    outbag.write(topic, msg, t, connection_header=conn_header)
  rospy.loginfo('Closing output bagfile and exit...')
  outbag.close()

if __name__ == "__main__":
  rospy.init_node('change_frame_id')
  parser = argparse.ArgumentParser(
      description='reate a new bagfile from an existing one replacing the frame id of requested topics.')
  parser.add_argument('-o', metavar='OUTPUT_BAGFILE', required=True, help='output bagfile')
  parser.add_argument('-i', metavar='INPUT_BAGFILE', required=True, help='input bagfile')
  parser.add_argument('-f', metavar='FRAME_ID', required=True, help='desired frame_id name in the topics')
  args = parser.parse_args()

  try:
    change_frame_id(args.i,args.o,args.f)
  except Exception, e:
    import traceback
    traceback.print_exc()