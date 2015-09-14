#include <motion/KickModule.h>
#include <common/KeyframeSequence.h>
#include <memory/FrameInfoBlock.h>
#include <memory/JointCommandBlock.h>
#include <memory/WalkRequestBlock.h>
#include <memory/OdometryBlock.h>
#include <memory/BodyModelBlock.h>
#include <memory/JointBlock.h>
#include <memory/SensorBlock.h>
#include <memory/KickRequestBlock.h>

#define JOINT_EPSILON (0.1f * DEG_T_RAD)

KickModule::KickModule() : state_(Finished), sequence_(NULL) { }

void KickModule::initSpecificModule() {
  auto file = cache_.memory->data_path_ + "/keyframe.yaml";
  sequence_ = new KeyframeSequence();
  if(!sequence_->load(file))
    sequence_ = NULL;
}

void KickModule::start() {
  state_ = Initial;
  keyframe_ = 0;
  frames_ = 0;
}

bool KickModule::finished() {
  return state_ == Finished;
}

void KickModule::specifyMemoryDependency() {
  requiresMemoryBlock("frame_info");
  requiresMemoryBlock("walk_request");
  requiresMemoryBlock("processed_joint_angles");
  requiresMemoryBlock("processed_joint_commands");
  requiresMemoryBlock("odometry");
  requiresMemoryBlock("processed_sensors");
  requiresMemoryBlock("body_model");
  requiresMemoryBlock("kick_request");
}

void KickModule::specifyMemoryBlocks() {
  getMemoryBlock(cache_.frame_info,"frame_info");
  getMemoryBlock(cache_.walk_request,"walk_request");
  getMemoryBlock(cache_.joint,"processed_joint_angles");
  getMemoryBlock(cache_.joint_command,"processed_joint_commands");
  getMemoryBlock(cache_.odometry,"odometry");
  getMemoryBlock(cache_.sensor,"processed_sensors");
  getMemoryBlock(cache_.body_model,"body_model");
  getMemoryBlock(cache_.kick_request,"kick_request");
}

void KickModule::processFrame() {
  if(state_ == Finished) return;
  if(sequence_ == NULL) return;
  if(keyframe_ >= sequence_->keyframes.size()) {
    state_ = Finished;
    return;
  }
  auto& keyframe = sequence_->keyframes[keyframe_];
  if(state_ == Initial) {
    if(reachedKeyframe(keyframe)) {
      state_ = Running;
    } else {
      moveToInitial(keyframe);
      return;
    }
  }
  if(frames_ == keyframe.frames) {
    keyframe_++;
    frames_ = 0;
    processFrame();
    return;
  }
  if(keyframe_ == sequence_->keyframes.size() - 1) {
    state_ = Finished;
    return;
  }
  auto& next = sequence_->keyframes[keyframe_ + 1];
  moveBetweenKeyframes(keyframe, next, frames_);
  frames_++;
}

bool KickModule::reachedKeyframe(const Keyframe& keyframe) {
  for(int i = 0; i < NUM_JOINTS; i++) {
    if(fabs(cache_.joint->values_[i] - keyframe.joints[i]) > JOINT_EPSILON) 
      return false;
  }
}

void KickModule::moveToInitial(const Keyframe& keyframe) {
  //TODO: fill in
}

void KickModule::moveBetweenKeyframes(const Keyframe& start, const Keyframe& finish, int cframe) {
  if(cframe == 0) {
    // send timed joint commands via command block
  }
#ifdef TOOL
  float progress = (cframe + 1.0f) / start.frames;
  for(int i = 0; i < NUM_JOINTS; i++) {
    auto delta = (finish.joints[i] - start.joints[i]) * progress;
    cache_.joint->values_[i] += delta;
  }
#endif
}