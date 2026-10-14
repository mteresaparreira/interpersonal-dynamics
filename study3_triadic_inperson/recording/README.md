# Study 3 recording pipeline

Reconstructed from the run-day protocol. The ROS package itself
(`record_social_dining`) lives on the lab recording machine and is **not in this
repository** — **[NO ACCESS]**. What follows is the operating sequence so the
capture can be reproduced or audited.

## Hardware

| Device | Count | Notes |
|---|---|---|
| Intel RealSense camera | 3 | Labelled `A`, `B`, `C` with tape; mounted on one shared central stand, each aimed at one seat. RGB + depth. |
| ReSpeaker microphone array | 1 | At the base of the camera stand. Physically marked for orientation so the per-direction audio channels in the bag file map to known seats. LED ring brightness set to 0 (`self.pixel_ring.set_brightness(0)` in `respeaker_noetic/scripts/respeaker_node.py`) so it does not blink on voice activity and distract participants. |
| Camcorder + tripod | 1 | Whole-scene view, HDMI to a monitor in the adjacent RIG Lab for unobtrusive observation. |
| Recording laptop | 1 | On a separate table; driven remotely over AnyDesk during the session. |

Reference for the ReSpeaker channel/direction layout:
<https://github.com/furushchev/respeaker_ros/blob/master/scripts/respeaker_node.py#L216>

## Pre-flight

1. Confirm ≥ 10 GB free on the recording machine.
2. Confirm no existing bag with this session name:
   `~/recording_ws/src/record_social_dining/bag/<session_id>.bag` — **the launch
   file will overwrite without warning.**
3. Bring up the devices:
   ```bash
   cd ~/catkin_ws/
   source ~/.bashrc
   roslaunch record_social_dining start_devices_depth.launch
   # (a highres variant, start_devices_highres.launch, was also used)
   ```
4. In a second terminal, check `rostopic list` shows all three cameras and the
   audio topics (`/audio`, `/audio/channel0`, …). Audio topics can take a few
   seconds to appear.
5. Open `rqt` to confirm all three video streams are live, then close it. If a
   stream is missing, re-seat the USB cables and hit the blue refresh button.
   (Three RealSense cameras on one bus is bandwidth-marginal; a dedicated PCIe USB
   card was added for this reason.)

## Recording

```bash
roslaunch record_social_dining record_depth.launch bagname:=<session_id>
# verify afterwards:
rosbag info ./src/record_social_dining/bag/<session_id>.bag
```

Start the recording over AnyDesk, from outside the room, immediately before the
five-minute timer.

## Extraction

```bash
cd src/record_social_dining
python3 extract_all_bags_audio.py
bash  extract_all_bags_video.sh
```

Produces one `.wav` and per-participant `.mp4` clips at **15 fps**. These are the
inputs to `../preprocessing/`.

## Serving CORAE

```bash
cd CORAE-Development
bash launch.sh
```

Participants reach their own instance at a static per-seat URL
(`<host>/static/A`, `/static/B`, `/static/C`). Credentials for the host are in the
lab's private protocol document and are deliberately **not reproduced here** — see
[`../../docs/privacy.md`](../../docs/privacy.md).

## Archiving

Bag, wav, mp4 and the CORAE JSON files go to the project Cornell Box folder.
Consent forms and paper rankings go to the physical folder. Verify the Box upload
from a *different* machine before deleting anything locally.
