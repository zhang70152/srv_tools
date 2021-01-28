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

def change_frame_id_and_time(inbag,frame_id,outbag):
  rospy.loginfo('   Processing input bagfile: %s', inbag)
  rospy.loginfo('           Writing frame_id: %s', frame_id)

  start_time = rospy.Time.from_sec(rosbag.Bag(inbag,'r').get_start_time())
  start_time_1 = rospy.Duration(rosbag.Bag(inbag,'r').get_start_time())
  print('start time', start_time.to_sec())

  for topic, msg, t, conn_header in rosbag.Bag(inbag,'r').read_messages(return_connection_header=True):
    if msg._has_header:
        msg.header.frame_id = merge_header(frame_id, msg.header.frame_id)
        if msg.header.stamp <  start_time  :
          print('msg.header.stamp', msg.header.stamp.to_sec())
          msg.header.stamp = rospy.Time.from_sec(0.0)
        else :  
          msg.header.stamp = msg.header.stamp - start_time
    if topic == "/tf" or topic == "/tf_static":
        for transform in msg.transforms:
            transform.header.frame_id = merge_header(frame_id, transform.header.frame_id)
            transform.child_frame_id = merge_header(frame_id, transform.child_frame_id)
            if transform.header.stamp < start_time:
              print('transform.header.stamp', transform.header.stamp.to_sec())
              transform.header.stamp = rospy.Time.from_sec(0.0)
            else:
              transform.header.stamp = transform.header.stamp - start_time
    else:
       topic = frame_id + topic
    if t <  start_time:
      print('t: ', t.to_sec())
      outbag.write(topic, msg, rospy.Time.from_sec(0.0), connection_header=conn_header)
    else:
      outbag.write(topic, msg, t - start_time_1, connection_header=conn_header)
  rospy.loginfo('Closing output bagfile and exit...')

  


def merge(inbag1, inbag2, outbag='final.bag', topics=None, exclude_topics=[], raw=True):
  #Open output bag file:
  try:
    out = rosbag.Bag(outbag, 'a' if os.path.exists(outbag) else 'w')
  except IOError as e:
    #print('Failed to open output bag file %s!: %s' % (outbag, e.message), file=sys.stderr)
    return 127

  for topic, msg, t in rosbag.Bag(inbag1, 'r').read_messages(topics=topics, raw=raw):
    #if topic not in exclude_topics:
    out.write(topic, msg, t, raw=raw)
  for topic, msg, t in rosbag.Bag(inbag2, 'r').read_messages(topics=topics, raw=raw):
    #if topic not in exclude_topics:
    out.write(topic, msg, t, raw=raw)

  out.close()

  return 0


if __name__ == "__main__":
  rospy.init_node('change_frame_id')
  parser = argparse.ArgumentParser(
      description='reate a new bagfile from an existing one replacing the frame id of requested topics.')


  parser.add_argument('-i1', metavar='INPUT_BAGFILE_1', required=True, help='input bagfile')
  parser.add_argument('-f1', metavar='FRAME_ID_1', required=True, help='desired frame_id name in the topics')
  parser.add_argument('-i2', metavar='INPUT_BAGFILE_2', required=True, help='input bagfile')
  parser.add_argument('-f2', metavar='FRAME_ID_2', required=True, help='desired frame_id name in the topics')
  parser.add_argument('-o', metavar='OUTPUT_BAGFILE', required=True, help='output bagfile')

  args = parser.parse_args()

  try:
    outbag = rosbag.Bag(args.o,'w')
    #out = rosbag.Bag(outbag, 'a' if os.path.exists(outbag) else 'w')
  except IOError as e:
    a=5
    #print('Failed to open output bag file %s!: %s' % (outbag, e.message), file=sys.stderr)
 

  try:
    change_frame_id_and_time(args.i1, args.f1, outbag)
    change_frame_id_and_time(args.i2, args.f2, outbag)
    outbag.close()
    #merge(outbag1,outbag2)
  except Exception, e:
    import traceback
    traceback.print_exc()