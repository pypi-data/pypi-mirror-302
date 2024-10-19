import dexhub 
import numpy as np
from dataclasses import dataclass, field
import scipy 
from typing import *
from enum import Enum
import scipy.spatial
import time 
from datetime import datetime
import warnings 
import io 
import imageio 
import mujoco 
from dm_control import mjcf 


@dataclass
class SE3: 

    """
    A class representing a 3D rigid body transformation (SE3).

    This class encapsulates a 3D position and a 3D rotation, and provides methods to convert between transformation matrices and SE3 representations.

    Attributes:
        pos (np.ndarray): A 3D position vector represented as a numpy array of shape (3,).
        rot (scipy.spatial.transform.Rotation): A rotation represented as a `scipy.spatial.transform.Rotation` object. 
    """

    pos: np.ndarray
    rot: scipy.spatial.transform.Rotation


    def __post_init__(self):
        if self.pos.shape != (3,):
            raise ValueError(f"Position must be a 3D vector, got {self.pos.shape}")
        if not isinstance(self.rot, scipy.spatial.transform.Rotation):
            raise TypeError(f"Rotation must be a scipy.spatial.transform.Rotation object, got {type(self.rot)}")
        
    def get_matrix(self):
        """
        Converts the SE3 object to a 4x4 homogeneous transformation matrix.

        :return: A 4x4 numpy array representing the homogeneous transformation matrix.
        :rtype: np.ndarray
        """

        matrix = np.eye(4)
        matrix[:3, :3] = self.rot.as_matrix()
        matrix[:3, 3] = self.pos
        return matrix
    
    @classmethod
    def from_matrix(cls, matrix: np.ndarray):
        """
        Class method to create an SE3 object from a 4x4 transformation matrix.

        :param matrix: A 4x4 homogeneous transformation matrix.
        :type matrix: np.ndarray
        :return: An SE3 object representing the transformation encoded in the matrix.
        :rtype: SE3
        :raises ValueError: If the input matrix is not of shape (4, 4).
        """
        if matrix.shape != (4, 4):
            raise ValueError(f"Matrix must be a 4x4 homogeneous transformation matrix, got {matrix.shape}")

        # Extract rotation matrix (top-left 3x3) and position vector (top-right 3x1)
        rotation_matrix = matrix[:3, :3]
        position = matrix[:3, 3]

        # Create a Rotation object from the rotation matrix
        rotation = scipy.spatial.transform.Rotation.from_matrix(rotation_matrix)

        return cls(pos=position, rot=rotation)

@dataclass
class Observation: 
    """
    Represents an observation in the robot's environment, containing sensory and positional data.

    :param rgbs: A dictionary of RGB images captured from different camera views. The keys are strings (camera names), and the values are numpy arrays representing the images.
    :type rgbs: Dict[str, np.ndarray]
    
    :param qpos: The robot's joint positions, represented as a numpy array.
    :type qpos: np.ndarray
    
    :param gripper_qpos: The positions of the gripper joints, represented as a numpy array.
    :type gripper_qpos: np.ndarray
    
    :param ee_pose: The end-effector pose, represented by an SE3 object.
    :type ee_pose: SE3
    
    :param depths: Optional dictionary of depth images captured from different camera views. The keys are strings (camera names), and the values are numpy arrays representing depth maps.
    :type depths: Optional[Dict[str, np.ndarray]]
    
    :param qvel: Optional array of joint velocities.
    :type qvel: Optional[np.ndarray]
    
    :raises TypeError: If any of the input parameters are not of the expected type.
    :raises ValueError: If any of the RGB images in `rgbs` do not have the expected shape (width, height, 3).
    
        
    .. warning::
        We require both `qpos` and `ee_pose` fields to be present in the observation. 
        Logging of both is essential us to post-process every loggings, ensuring consistent axis conventions and frame transformations. 
        The post-processing step is performed by :func:`dexhub.utils.sanity_checker`.
    .. note::
        We are expecting RGB images to be in the shape (width, height, 3) and depth images to be in the shape (width, height).

    """


@dataclass
class Observation:
    _rgbs: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    _qpos: Optional[np.ndarray] = None
    _gripper_qpos: Optional[np.ndarray] = None
    _ee_pose: Optional[SE3] = None
    _depths: Optional[Dict[str, np.ndarray]] = None
    _qvel: Optional[np.ndarray] = None
    _mj_qpos: Optional[np.ndarray] = None
    _mj_qvel: Optional[np.ndarray] = None

    def __init__(self, rgbs: Optional[Dict[str, np.ndarray]] = None, qpos: Optional[np.ndarray] = None, gripper_qpos: Optional[np.ndarray] = None, ee_pose: Optional[SE3] = None, depths: Optional[Dict[str, np.ndarray]] = None, qvel: Optional[np.ndarray] = None, mj_qpos: Optional[np.ndarray] = None, mj_qvel: Optional[np.ndarray] = None):
        self._rgbs = rgbs
        self._qpos = qpos
        self._gripper_qpos = gripper_qpos
        self._ee_pose = ee_pose
        self._depths = depths
        self._qvel = qvel
        self._mj_qpos = mj_qpos
        self._mj_qvel = mj_qvel
        self.__post_init__()

    def __post_init__(self):
        # Initial type checks if values are provided at initialization
        if self._rgbs is not None:
            self._validate_rgbs(self._rgbs)
        if self._depths is not None:
            self._validate_rgbs(self._depths)
        if self._qpos is not None and not isinstance(self._qpos, np.ndarray):
            raise TypeError(f"qpos must be a numpy array, got {type(self._qpos)}")
        if self._gripper_qpos is not None and not isinstance(self._gripper_qpos, np.ndarray):
            raise TypeError(f"gripper_qpos must be a numpy array, got {type(self._gripper_qpos)}")
        if self._ee_pose is not None and not isinstance(self._ee_pose, SE3):
            raise TypeError(f"ee_pose must be an SE3 object, got {type(self._ee_pose)}")
        if self._qvel is not None and not isinstance(self._qvel, np.ndarray):
            raise TypeError(f"qvel must be a numpy array, got {type(self._qvel)}")
        if self._mj_qpos is not None and not isinstance(self._mj_qpos, np.ndarray):
            raise TypeError(f"mj_qpos must be a numpy array, got {type(self._mj_qpos)}")
        if self._mj_qvel is not None and not isinstance(self._mj_qvel, np.ndarray):
            raise TypeError(f"mj_qvel must be a numpy array, got {type(self._mj_qvel)}")
        
    # Property for qpos with a setter for type checking
    @property
    def qpos(self):
        return self._qpos

    @qpos.setter
    def qpos(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError(f"qpos must be a numpy array, got {type(value)}")
        self._qpos = value

    @property
    def qvel(self):
        return self._qvel
    
    @qvel.setter
    def qvel(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"qvel must be a numpy array, got {type(value)}")
        self._qvel = value

    # Property for depths with a setter for type checking
    @property
    def depths(self):
        return self._depths
    
    @depths.setter
    def depths(self, value):
        if value is not None:
            self._validate_rgbs(value)
        self._depths = value

    @property
    def rgbs(self):
        return self._rgbs
    
    @rgbs.setter
    def rgbs(self, value):
        if value is not None:
            self._validate_rgbs(value)
        self._rgbs = value

    @property
    def mj_qpos(self):
        return self._mj_qpos
    
    @mj_qpos.setter
    def mj_qpos(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"mj_qpos must be a numpy array, got {type(value)}")
        self._mj_qpos = value

    @property
    def mj_qvel(self):
        return self._mj_qvel
    
    @mj_qvel.setter
    def mj_qvel(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"mj_qvel must be a numpy array, got {type(value)}")
        self._mj_qvel = value

    # Property for gripper_qpos with a setter for type checking
    @property
    def gripper_qpos(self):
        return self._gripper_qpos

    @gripper_qpos.setter
    def gripper_qpos(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError(f"gripper_qpos must be a numpy array, got {type(value)}")
        self._gripper_qpos = value

    # Property for ee_pose with a setter for type checking
    @property
    def ee_pose(self):
        return self._ee_pose

    @ee_pose.setter
    def ee_pose(self, value):
        if not isinstance(value, SE3):
            raise TypeError(f"ee_pose must be an SE3 object, got {type(value)}")
        self._ee_pose = value

    def _validate_rgbs(self, rgbs):
        if not isinstance(rgbs, dict) or not all(isinstance(v, np.ndarray) for v in rgbs.values()):
            raise TypeError(f"rgbs must be a dictionary of numpy arrays, got {type(rgbs)}")
        for key, value in rgbs.items():
            if value.shape[-1] != 3 or len(value.shape) != 3:
                raise ValueError(f"Each numpy array in rgbs must have shape (width, height, 3), but '{key}' has shape {value.shape}")



@dataclass
class ObservationChunk:
    """
    A dataclass to represent a chunk of observations, useful for policy training.
    Shares the same attributes as :class:`dexhub.types.Observation` but with batch dimensions as the first axis.
    """
    
    rgbs: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qpos: Optional[np.ndarray] = None
    gripper_qpos: Optional[np.ndarray] = None
    ee_pose: Optional[np.ndarray] = None
    depths: Optional[Dict[str, np.ndarray]] = None
    qvel: Optional[np.ndarray] = None




@dataclass
class Action:
    """
    Represents an action for controlling the robot, which can include joint positions, velocities, torques, or the end-effector pose.

    :param qpos: The desired joint positions, represented as a numpy array. This is required for position control mode.
    :param qvel: The desired joint velocities, represented as a numpy array. This is required for velocity control mode.
    :param qtorque: The desired joint torques, represented as a numpy array. This is required for torque control mode.
    :param ee_pose: The desired end-effector pose, represented as an SE3 object.

    :raises ValueError: If the necessary control mode parameters (`qpos`, `qvel`, or `qtorque`) are missing for the respective control mode.
    """
    
    _qpos: Optional[np.ndarray] = None
    _qvel: Optional[np.ndarray] = None
    _qtorque: Optional[np.ndarray] = None
    _ee_pose: Optional[SE3] = None
    _gripper_qpos: Optional[np.ndarray] = None
    _gripper_qvel: Optional[np.ndarray] = None
    _mj_ctrl: Optional[np.ndarray] = None

    @property
    def mj_ctrl(self):
        return self._mj_ctrl
    
    @mj_ctrl.setter
    def mj_ctrl(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"mj_ctrl must be a numpy array, got {type(value)}")
        self._mj_ctrl = value

    # Property for qpos with type checking
    @property
    def qpos(self):
        return self._qpos
    
    @qpos.setter
    def qpos(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"qpos must be a numpy array, got {type(value)}")
        self._qpos = value

    # Property for qvel with type checking
    @property
    def qvel(self):
        return self._qvel

    @qvel.setter
    def qvel(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"qvel must be a numpy array, got {type(value)}")
        self._qvel = value

    # Property for qtorque with type checking
    @property
    def qtorque(self):
        return self._qtorque

    @qtorque.setter
    def qtorque(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"qtorque must be a numpy array, got {type(value)}")
        self._qtorque = value

    # Property for ee_pose with type checking
    @property
    def ee_pose(self):
        return self._ee_pose

    @ee_pose.setter
    def ee_pose(self, value):
        if value is not None and not isinstance(value, SE3):
            raise TypeError(f"ee_pose must be an SE3 object, got {type(value)}")
        self._ee_pose = value

    @property
    def gripper_qpos(self):
        return self._gripper_qpos
    
    @gripper_qpos.setter
    def gripper_qpos(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"gripper_qpos must be a numpy array, got {type(value)}")
        self._gripper_qpos = value


    @property
    def gripper_qvel(self):
        return self._gripper_qvel
    
    @gripper_qvel.setter
    def gripper_qvel(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError(f"gripper_qvel must be a numpy array, got {type(value)}")
        self._gripper_qvel = value


@dataclass
class ActionChunk:
    """
    A dataclass to represent a chunk of actions, useful for policy training.  
    Shares the same attributes as :class:`dexhub.types.Action` but with batch dimensions as the first axis.
    """
    
    qpos: Optional[np.ndarray] = None
    qvel: Optional[np.ndarray] = None
    qtorque: Optional[np.ndarray] = None
    ee_pose: Optional[np.ndarray] = None
    gripper_qpos: Optional[np.ndarray] = None
    gripper_qvel: Optional[np.ndarray] = None



@dataclass
class Transition: 
    """
    A data class representing a transition, which consists of an observation-action pair.

    Attributes:
        obs (Observation): The observation at the current time step.
        act (Action): The action taken based on the observation.
    """

    obs: Observation
    act: Action


class arms(Enum):
    """
    Enum representing different robotic arms.

    :cvar UR3E: Universal Robots UR3e arm.
    :cvar UR5E: Universal Robots UR5e arm.
    :cvar FR3: Franka Research 3 arm.
    :cvar PANDA: Franka Emika Panda arm.
    :cvar JACO: Kinova Jaco robotic arm.
    :cvar KINOVAGen3: Kinova Gen3 robotic arm.
    """

    UR3E = "UR3e"
    UR5E = "UR5e"
    FR3 = "Franka  Research 3"
    PANDA = "Franka Emika Panda"
    JACO = "Jaco"
    KINOVAGen3 = "Kinova Gen3"

class grippers(Enum):
    """
    Enum representing different robotic grippers.

    :cvar ROBOTIQ_2F85: Robotiq 2F-85 gripper.
    :cvar ROBOTIQ_2F140: Robotiq 2F-140 gripper.
    :cvar PANDA_HAND: Panda Hand gripper.
    """

    ROBOTIQ_2F85 = "Robotiq 2F-85"
    ROBOTIQ_2F140 = "Robotiq 2F-140"
    PANDA_HAND = "Panda Hand"

class hands(Enum):
    """
    Enum representing different multifingered robotic hands.

    :cvar SHADOW_HAND: Shadow Dexterous Hand.
    :cvar ALLEGRO_HAND: Allegro Hand.
    :cvar LEAP_HAND: Leap Hand.
    """
    SHADOW_HAND = "Shadow Dexterous Hand"
    ALLEGRO_HAND = "Allegro Hand"
    LEAP_HAND = "Leap Hand"


class control_modes(Enum):
    """
    Enum representing different control modes for robotic arms and hands.

    :cvar POSITION: Position control mode for direct control of joint positions.
    :cvar EEPOSE: End-effector pose control mode.
    :cvar VELOCITY: Velocity control mode for controlling joint velocities.
    """

    POSITION = "Position"
    EEPOSE = "End-Effector Pose"
    VELOCITY = "Velocity"


class TransitionStorage:
    """
    A class to store the logged transitions in memory and perform post-processing tasks like
    creating videos from RGB observations, compressing data, and checking the consistency of logged transitions.

    The `TransitionStorage` class stores a sequence of transitions along with timestamps, provides methods
    to append transitions, remove unnecessary data, and perform compression and decompression before saving
    and after loading.

    Attributes:
        data (List[Transition]): A list that holds the logged transitions.
        time_stamp (List[datetime]): A list that holds the timestamps for each logged transition.
        video_bytes (Dict[str, io.BytesIO]): A dictionary that stores video data (in bytes) for each camera.
        meta_data (Dict[str, Any]): A dictionary that stores metadata associated with the project.
        mjmodel_bytes (Dict[str, Optional[io.BytesIO]]): A dictionary that stores the MuJoCo model files (XML and asset files) as byte streams.
    """
    
    def __init__(self):
        """
        Initializes the `TransitionStorage` with empty lists for storing transitions and timestamps, 
        and initializes an empty dictionary for storing video buffers.
        """
        self.data: List[Transition] = []
        self.time_stamp: List[datetime] = []
        self.video_bytes: Dict[str, io.BytesIO] = {}
        self.meta_data: Dict[str, Any] = {}
        self.mjcf_data = {
            "xml": None,
            "assets": None, 
        }  
    
    def append(self, transition: Transition):
        """
        Appends a transition to the storage and records the current timestamp.

        :param transition: The transition to be added to the storage.
        :type transition: Transition
        """
        self.data.append(transition)
        self.time_stamp.append(datetime.now())

    def get_mjmodel(self):
        """
        Loads the MuJoCo model from the stored byte streams.
        """
        return mujoco.MjModel.from_xml_string(self.mjcf_data["xml"], self.mjcf_data["assets"])
    
    def register_meta_data(self, meta_data: Dict[str, Any]):
        """
        Registers the metadata associated with the project.

        :param meta_data: A dictionary containing the project metadata.
        :type meta_data: Dict[str, Any]
        """
        self.meta_data = meta_data

    def _remove_rgb(self):
        """
        Removes RGB images from the stored transitions to save memory during the compression process.

        This method replaces all RGB image data in the transitions with `None` to reduce the storage size
        after video encoding is done.
        """
        for transition in self.data:
            for key in transition.obs.rgbs.keys():
                transition.obs.rgbs[key] = None 
    
    def compress(self):
        """
        Compresses the logged transitions by creating videos from the RGB observations and
        removing the original RGB data from the transitions.

        This method first creates video files from the logged RGB frames for each camera, stores them
        in the `video_bytes` attribute, and then removes the raw RGB data to reduce memory usage.
        """
        self._make_video()
        self._make_thumbnail_video()
        self._remove_rgb()

    def _make_thumbnail_video(self):
        """
        Creates a thumbnail video from the logged RGB transitions: for multiple camera view points, 
        things are stacked vertically to create a vertically long video like Youtube shorts form. 
        """

        buffer = io.BytesIO()
        writer = imageio.get_writer(buffer, format='mp4', fps=30, codec='libx264', macro_block_size=4)

        for transition in self.data:
            # concatenate all the images vertically
            rgb = np.concatenate([transition.obs.rgbs[key] for key in transition.obs.rgbs.keys()], axis = 0)
            writer.append_data(rgb)

        writer.close()
        # actually write the buffer to a file
        buffer.seek(0)
        self.video_bytes["thumbnail"] = buffer

    def decompress(self):
        """
        Decompresses the logged transitions by decoding video files and restoring RGB frames.

        This method reads the video data stored in `video_bytes`, decodes it back into individual frames,
        and restores the RGB images into their corresponding transitions.
        """
        self._decode_video()
    
    def _realtime_check(self):
        """
        Checks if the transitions are logged at uniform time intervals.

        This method calculates the time intervals between consecutive transitions and issues a warning 
        if the intervals deviate by more than 10% from the mean time interval.

        :raises Warning: If transitions are not logged in uniform time intervals.
        """
        time_intervals = [self.time_stamp[i+1] - self.time_stamp[i] for i in range(len(self.time_stamp) - 1)]
        mean_time_interval = sum(time_intervals) / len(time_intervals)

        # Allow 10% deviation from mean time interval
        if not all(abs(t - mean_time_interval) < 0.1 * mean_time_interval for t in time_intervals):
            warnings.warn("Transitions are not logged in uniform time intervals.")

    def sanity_check(self):
        """
        Checks the logged transitions for consistency and correctness by solving an optimization problem
        to correct joint ordering and end-effector frame conventions.

        The optimization aligns joint ordering and end-effector frames by searching over permutations and 
        end-effector frame conventions using brute force and gradient descent, respectively.

        .. math::
            \min_{\\text{perm},\mathbf{T}} \sum  \| f(\\text{perm}(\\theta )) \cdot \mathbf{T} - \mathbf{T}^{ee} \|

        The brute-force search is performed for joint permutations, and the end-effector frame conventions
        are optimized using a differentiable forward kinematics layer.
        """
        # Optimization logic goes here

    def _make_video(self):
        """
        Creates videos from the logged RGB transitions and stores them as byte streams.

        This method loops through the RGB frames for each camera in the logged transitions, creates a video
        using the `libx264` codec, and stores the video in the `video_bytes` dictionary as a byte stream.

        :raises ValueError: If the RGB data for any camera is missing or invalid.
        """
        obs = self.data[0].obs
        camera_names = sorted(obs.rgbs.keys())

        self.video_bytes = {}

        for camera_name in camera_names:
            buffer = io.BytesIO()
            # Use libx264 codec with macro_block_size option for efficient encoding
            with imageio.get_writer(buffer, format='mp4', fps=30, codec='libx264', macro_block_size=4) as writer:
                for transition in self.data:
                    rgb = transition.obs.rgbs.get(camera_name)
                    if rgb is None:
                        raise ValueError(f"RGB data for camera '{camera_name}' is missing in some transitions.")
                    writer.append_data(rgb)
            
            buffer.seek(0)
            self.video_bytes[camera_name] = buffer

    def _decode_video(self) -> Dict[str, np.ndarray]:
        """
        Decodes the stored video byte streams into individual RGB frames and restores them in the transitions.

        This method reads the video files stored in the `video_bytes` dictionary, decodes them into individual
        frames, and restores the frames to the corresponding transitions for each camera.

        :raises ValueError: If any video file cannot be read or decoded.
        """
        for camera_name, buffer in self.video_bytes.items():
            buffer.seek(0)  # Ensure we're at the start of the buffer

            # Read the video data using imageio
            video = imageio.get_reader(buffer, format='mp4')

            # Convert the video to a list of frames (numpy arrays)
            frames = [frame for frame in video]

            if len(frames) != len(self.data):
                raise ValueError(f"Mismatch between the number of frames and transitions for camera '{camera_name}'.")

            for i, frame in enumerate(frames): 
                self.data[i].obs.rgbs[camera_name] = np.array(frame)


    def get_chunks(self, obs_chunk_size: int, act_chunk_size: int) -> List[Tuple[ObservationChunk, ActionChunk]]:
        """
        Splits the logged transitions into overlapping chunks of observations and actions.

        This method creates chunks of observations and actions, where the observation chunks and action chunks
        overlap. The chunk sizes for observations and actions are determined by `obs_chunk_size` and `act_chunk_size`.

        For example, with `obs_chunk_size=3` and `act_chunk_size=5`, and given the logged transitions:

        .. code-block:: python

            Observations: o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, ...
            Actions     : a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, ...

        The method will return the following chunks:

        .. code-block:: python

            [
                ((o1, o2, o3), (a3, a4, a5, a6, a7)), 
                ((o2, o3, o4), (a4, a5, a6, a7, a8)),
                ((o3, o4, o5), (a5, a6, a7, a8, a9)),
                ((o4, o5, o6), (a6, a7, a8, a9, a10)),
                ...
            ]

        The observation chunks will consist of consecutive `obs_chunk_size` observations, and the action chunks
        will be created starting from the middle of the observation chunk (at index `obs_chunk_size // 2`) and
        extending to `act_chunk_size`.

        :param obs_chunk_size: The number of consecutive observations to include in each observation chunk.
        :type obs_chunk_size: int
        :param act_chunk_size: The number of consecutive actions to include in each action chunk.
        :type act_chunk_size: int
        :return: A list of tuples, where each tuple contains an observation chunk and an action chunk.
        :rtype: List[Tuple[ObservationChunk, ActionChunk]]
                
        :raises ValueError: If the number of logged transitions is less than the chunk sizes.
        """
        if len(self.data) < max(obs_chunk_size, act_chunk_size):
            raise ValueError("The number of logged transitions is less than the chunk sizes.")

        chunk_pairs = [] 

        for i in range(len(self.data) - obs_chunk_size + 1):
            obs_chunk = [self.data[j].obs for j in range(i, i + obs_chunk_size)]
            
            # Action chunks start from the middle of the observation chunk and extend to the specified length.
            action_start = i + (obs_chunk_size // 2)
            action_end = min(action_start + act_chunk_size, len(self.data))
            act_chunk = [self.data[j].act for j in range(action_start, action_end)]

            obs_chunk = self._batchify_observations(obs_chunk)
            act_chunk = self._batchify_actions(act_chunk)

            chunk_pairs.append((obs_chunk, act_chunk))

        return chunk_pairs

    def _batchify_observations(observations: List[Observation]) -> ObservationChunk:
        """
        Combines a list of Observation objects into a single ObservationChunk
        by stacking the numpy arrays along axis=0.

        :param observations: A list of Observation objects to be combined.
        :type observations: List[Observation]
        :return: A single Observation object where the numpy arrays have been stacked along axis=0.
        :rtype: Observation
        """
        
        # Stack RGB dictionaries
        if all(obs.rgbs is not None for obs in observations):
            stacked_rgbs = {
                key: np.stack([obs.rgbs[key] for obs in observations], axis=0)
                for key in observations[0].rgbs.keys()
            }
        else:
            stacked_rgbs = None

        # Stack qpos arrays
        if all(obs.qpos is not None for obs in observations):
            stacked_qpos = np.stack([obs.qpos for obs in observations], axis=0)
        else:
            stacked_qpos = None

        # Stack gripper_qpos arrays
        if all(obs.gripper_qpos is not None for obs in observations):
            stacked_gripper_qpos = np.stack([obs.gripper_qpos for obs in observations], axis=0)
        else:
            stacked_gripper_qpos = None

        # Stack ee_pose arrays (assuming SE3 is a numpy-compatible type)
        if all(obs.ee_pose is not None for obs in observations):
            stacked_ee_pose = np.stack([obs.ee_pose for obs in observations], axis=0)
        else:
            stacked_ee_pose = None

        # Stack depth dictionaries
        if all(obs.depths is not None for obs in observations):
            stacked_depths = {
                key: np.stack([obs.depths[key] for obs in observations], axis=0)
                for key in observations[0].depths.keys()
            }
        else:
            stacked_depths = None

        # Stack qvel arrays
        if all(obs.qvel is not None for obs in observations):
            stacked_qvel = np.stack([obs.qvel for obs in observations], axis=0)
        else:
            stacked_qvel = None

        # Create a new ObservationChunk object with stacked data
        return ObservationChunk(
            rgbs=stacked_rgbs,
            qpos=stacked_qpos,
            gripper_qpos=stacked_gripper_qpos,
            ee_pose=stacked_ee_pose,
            depths=stacked_depths,
            qvel=stacked_qvel
        )


    def _batchify_actions(actions: List[Action]) -> ActionChunk:
        """
        Combines a list of Action objects into a single ActionChunk by stacking the numpy arrays along axis=0.

        :param actions: A list of Action objects to be combined.
        :type actions: List[Action]
        :return: A single ActionChunk object where the numpy arrays have been stacked along axis=0.
        :rtype: ActionChunk
        """
        
        # Stack qpos arrays
        if all(action.qpos is not None for action in actions):
            stacked_qpos = np.stack([action.qpos for action in actions], axis=0)
        else:
            stacked_qpos = None

        # Stack qvel arrays
        if all(action.qvel is not None for action in actions):
            stacked_qvel = np.stack([action.qvel for action in actions], axis=0)
        else:
            stacked_qvel = None

        # Stack qtorque arrays
        if all(action.qtorque is not None for action in actions):
            stacked_qtorque = np.stack([action.qtorque for action in actions], axis=0)
        else:
            stacked_qtorque = None

        # Stack ee_pose arrays (assuming SE3 is numpy-compatible)
        if all(action.ee_pose is not None for action in actions):
            stacked_ee_pose = np.stack([action.ee_pose for action in actions], axis=0)
        else:
            stacked_ee_pose = None

        # Stack gripper_qpos arrays
        if all(action.gripper_qpos is not None for action in actions):
            stacked_gripper_qpos = np.stack([action.gripper_qpos for action in actions], axis=0)
        else:
            stacked_gripper_qpos = None

        # Stack gripper_qvel arrays
        if all(action.gripper_qvel is not None for action in actions):
            stacked_gripper_qvel = np.stack([action.gripper_qvel for action in actions], axis=0)
        else:
            stacked_gripper_qvel = None

        # Return the batchified ActionChunk
        return ActionChunk(
            qpos=stacked_qpos,
            qvel=stacked_qvel,
            qtorque=stacked_qtorque,
            ee_pose=stacked_ee_pose,
            gripper_qpos=stacked_gripper_qpos,
            gripper_qvel=stacked_gripper_qvel
        )


    def clear(self):
        """
        Clears the stored transitions, timestamps, and video buffers.

        This method is automatically called after saving the transitions, clearing all logged data in the
        `TransitionStorage` object, including the transitions, timestamps, and video byte streams.
        """
        self.data = []
        self.time_stamp = []
        self.video_bytes = {}
        self.meta_data = {}


