#pragma once

#include <common/RobotInfo.h>
#include <common/YamlConfig.h>

class Keyframe : public YamlConfig {
  public:
    Keyframe() = default;
    Keyframe(std::string name);
    void deserialize(const YAML::Node& node);
    void serialize(YAML::Emitter& emitter) const;

    std::array<float,NUM_JOINTS> joints;
    std::string name;
    int frames;
};

class KeyframeSequence : public YamlConfig {
  public:
    void deserialize(const YAML::Node& node);
    void serialize(YAML::Emitter& emitter) const;

    std::vector<Keyframe> keyframes;
};
