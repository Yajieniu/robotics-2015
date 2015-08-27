import core
from copy import deepcopy
from memory import walk_param, robot_state
import UTdebug
from core import DEG_T_RAD,RAD_T_DEG
from util import Dynamic

##########################-
# BHWALK PARAMETERS
##########################-
def initWalk():
  walk_param.send_params_ = True
  walk_param.bh_params_.set = True # DON'T FORGET THIS
  # defaults
  walk_param.bh_params_.speedMax = core.Pose2D(0.8,120,50)
  walk_param.bh_params_.speedMaxBackwards = 50
  walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  walk_param.bh_params_.rsSpeedMax = core.Pose2D(0.87,300,180)# 0.87, 300, 200
  walk_param.bh_params_.rsMaxChange = core.Pose2D(0.87,50,50)#0.87,50,50
  walk_param.bh_params_.rs_turn_angle_offset = 0 #TODO 07/19/2015
  # Default settings for walk speed control
  walk_param.sagittal_prior_mean = 3;
  walk_param.sagittal_prior_stddev = 6.0;
  walk_param.coronal_prior_mean = 1.5;
  walk_param.coronal_prior_stddev = 6.0;
  # Default settings for forwards/backwards transition
  walk_param.dir_change_wait_duration = 100;
  walk_param.turn_limit = 1.0;
  walk_param.walking_turn_limit = 1.0;

  # robot specific
  id = core.CONFIG_ID
  set = True
  # Austin Villa IDs
  if id == 35:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by katie 1/23/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 36:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by katie 1/23/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 41:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by katie 1/23/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 43:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by katie 1/23/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 42:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by katie 1/25/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 47:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by katie 1/25/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 40:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 4/30/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,20,10)
  elif id == 46:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
  elif id == 50:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
  elif id == 51:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
  elif id == 52:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
  elif id == 53:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
  elif id == 54:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
    # carpet challenge	
    #walk_param.bh_params_.rsSpeedMax = core.Pose2D(0.7,270,180) # by Ruohan 7/18/15
  elif id == 55:
    walk_param.bh_params_.speedMax = core.Pose2D(0.4,100,40) # by Josiah 5/1/15
    walk_param.bh_params_.speedMaxChange = core.Pose2D(0.1,10,10)
  else:
    set = False

  if not core.TOOL:
    if set:
      UTdebug.log(0,'  BH Robot specific params found for',id)
    else:
      UTdebug.log(0,'  ** No BH Robot specific params found for',id)


##########################
cfgWalk1 = Dynamic()
# max speeds
cfgWalk1.max_step_size_ = (DEG_T_RAD*20,60,40) # Apparently the constructor is Rot,X,Y not X,Y,Rot (MQ 3/17/2011)
# dimensions of walk
cfgWalk1.foot_separation_ = 2 * 48
cfgWalk1.walk_height_ = 175
cfgWalk1.pendulum_height_ = 310
cfgWalk1.step_height_ = 12.5
cfgWalk1.phase_length_ = 0.46 #0.42 #46 #0.50
cfgWalk1.double_support_frac_ = 0.1
cfgWalk1.left_foot_zmp_offset_ = Dynamic()
cfgWalk1.left_foot_zmp_offset_.x = -10
cfgWalk1.left_foot_zmp_offset_.y = -20 # -22.5 # -15
cfgWalk1.right_foot_zmp_offset_ = Dynamic()
cfgWalk1.right_foot_zmp_offset_.x = -10
cfgWalk1.right_foot_zmp_offset_.y = 20

# how delayed are these sensors
cfgWalk1.accel_sensor_delay_frames_ = 0
cfgWalk1.pen_sensor_delay_frames_ = 6

cfgWalk1.num_averaged_sensor_zmp_frames_ = 1
cfgWalk1.num_averaged_sensor_pen_frames_ = 3

cfgWalk1.closed_loop_zmp_ = True
cfgWalk1.closed_loop_pen_ = True

cfgWalk1.interp_zmp_forward_ = False
cfgWalk1.interp_zmp_side_amount_ = 0.0


cfgWalk1.zmp_sensor_control_ratio_ = 1.0 #0.3
cfgWalk1.pen_sensor_control_ratio_ = 0.5#0.5 #0.3 #1.0 #0.3

cfgWalk1.tilt_roll_factor_ = 0.1 #1 #0 # how much tilt and roll to use

cfgWalk1.min_step_change_time_ = 0.3
# both lift and step timings are proportions of the single support phase
cfgWalk1.lift_start_time_ = 0.0
cfgWalk1.lift_stop_time_ = 0.9
cfgWalk1.step_start_time_ = 0.0
cfgWalk1.step_stop_time_ = 0.9

cfgWalk1.step_speed_factor_ = 5 # factor for sigmoid
cfgWalk1.hip_roll_offset_amount_ = DEG_T_RAD * -3
cfgWalk1.hip_roll_offset_rise_frac_ = 0.04 / 0.50
cfgWalk1.hip_roll_offset_fall_frac_ = 0.12 / 0.50
cfgWalk1.hip_roll_offset_start_frac_ = 0.00
cfgWalk1.hip_roll_offset_stop_frac_ = 1.00

cfgWalk1.swing_tilt_amount_ = DEG_T_RAD * 5
cfgWalk1.swing_tilt_start_frac_ = 0.5
cfgWalk1.swing_tilt_stop_frac_ = 1.0


cfgNDD = Dynamic()
# max speeds
cfgNDD.max_step_size_ = (DEG_T_RAD*20,120,40) # Apparently the constructor is Rot,X,Y not X,Y,Rot (MQ 3/17/2011)
# dimensions of walk
cfgNDD.foot_separation_ = 2 * 50
cfgNDD.pendulum_height_ = 260

cfgNDD.walk_height_ = 202 #235+cfgNDD.pendulum_height_ #250.456

cfgNDD.step_height_ = 15#20
cfgNDD.phase_length_ = 0.42 #0.42 #0.42 #46 #0.50
cfgNDD.double_support_frac_ = 0.1 #0.3333
cfgNDD.left_foot_zmp_offset_ = Dynamic()
cfgNDD.left_foot_zmp_offset_.x = -15
cfgNDD.left_foot_zmp_offset_.y = 6 # -22.5 # -15
cfgNDD.right_foot_zmp_offset_ = Dynamic()
cfgNDD.right_foot_zmp_offset_.x = -15
cfgNDD.right_foot_zmp_offset_.y = -6

cfgNDD.accel_sensor_delay_frames_ = 0
cfgNDD.pen_sensor_delay_frames_ = 6

cfgNDD.num_averaged_sensor_zmp_frames_ = 1
cfgNDD.num_averaged_sensor_pen_frames_ = 3

cfgNDD.closed_loop_zmp_ = False #True
cfgNDD.closed_loop_pen_ = False #True

cfgNDD.interp_zmp_forward_ = True #True
cfgNDD.interp_zmp_side_amount_ = 20#20.0

cfgNDD.zmp_sensor_control_ratio_ = 1.0 #0.3
cfgNDD.pen_sensor_control_ratio_ = 0.5#0.5 #0.3 #1.0 #0.3

cfgNDD.tilt_roll_factor_ = 0 # how much tilt and roll to use

cfgNDD.min_step_change_time_ = 0.3
# both lift and step timings are proportions of the single support phase
cfgNDD.lift_start_time_ = 0.0
cfgNDD.lift_stop_time_ = 1.0
cfgNDD.step_start_time_ = 0.0
cfgNDD.step_stop_time_ = 1.0

cfgNDD.step_speed_factor_ = 5 # factor for sigmoid
cfgNDD.hip_roll_offset_amount_ = DEG_T_RAD * -2.0
cfgNDD.hip_roll_offset_rise_frac_ = 0.04
cfgNDD.hip_roll_offset_fall_frac_ = 0.04
cfgNDD.hip_roll_offset_start_frac_ = 0.0
cfgNDD.hip_roll_offset_stop_frac_  = 1.0

cfgNDD.swing_tilt_amount_ = 0.0
cfgNDD.swing_tilt_start_frac_ = 0.5
cfgNDD.swing_tilt_stop_frac_ = 1.0


###### SIM

cfgSimWalk1 = deepcopy(cfgWalk1)
cfgSimWalk1.max_step_size_ = {DEG_T_RAD*20,80,40} # Apparently the constructor is Rot,X,Y not X,Y,Rot (MQ 3/17/2011)

cfgSimWalk1.num_averaged_sensor_zmp_frames_ = 3
cfgSimWalk1.num_averaged_sensor_pen_frames_ = 3
cfgSimWalk1.accel_sensor_delay_frames_ = 6
cfgSimWalk1.hip_roll_offset_amount_ = DEG_T_RAD * 0 #-3 #0# 1
cfgSimWalk1.tilt_roll_factor_ = 0 #0.1



cfgSimNDD = deepcopy(cfgNDD)
cfgSimNDD.max_step_size_ = {DEG_T_RAD*20,80,40}
cfgSimNDD.num_averaged_sensor_zmp_frames_ = 3
cfgSimNDD.num_averaged_sensor_pen_frames_ = 3
cfgSimNDD.accel_sensor_delay_frames_ = 6
cfgSimNDD.hip_roll_offset_amount_ = DEG_T_RAD * 0 #-3 #0# 1
