from deployment.exploration_strategies.exploration_strategy import ExplorationStrategy
from deployment.deployment_helpers import get_obstacle_forces as gof, AtLandingConditionException
from helpers import normalize, rot_mat_2D, get_vector_angle as gva

import numpy as np
from enum import IntEnum

class LineExploreKind(IntEnum):
      ONE_DIM_GLOBAL = 1,
      TWO_DIM_GLOBAL = 2,
      ONE_DIM_LOCAL  = 3,
      TWO_DIM_LOCAL  = 4,

class LineExplore(ExplorationStrategy):

  RSSI_TRHESHOLD = 0.5

  def __init__(self, K_o=1, force_threshold=0.01, kind=LineExploreKind.ONE_DIM_GLOBAL,
              get_exploration_dir_callback= lambda MIN, neighs, F_O: None):
    self.K_o = K_o
    self.force_threshold = force_threshold
    self.kind = kind
    self.get_exploration_dir_callback = get_exploration_dir_callback

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):

    land_due_to_no_neighs = False

    F_n = np.zeros((2, ))
    F_o = gof(self.K_o, MIN, ENV)

    x_is = np.concatenate([b.pos.reshape(2, 1) for b in beacons], axis=1)
    xi_is = np.array([MIN.get_xi_to_other_from_model(b) for b in beacons])

    if int(self.kind) <= 2:
      """GLOBAL METHODS"""

      if self.kind == LineExploreKind.ONE_DIM_GLOBAL:
        x_is = x_is[0, :]

        """ Default values """
        k_is = np.ones(x_is.shape)
        a_is = np.ones(x_is.shape)
        a_is[-1] = 1 + (1/k_is[-1])*np.sum(k_is[:-1])

        """ Leads to equally spaced drones """
        k_is = np.zeros(x_is.shape)
        k_is[-1] = 2*1
        a_is[-1] = 1

        """ Test for 'move back gains' (a_i*k_i = 0 for all 0 < i < n) """
        
        """ test 1 """

        k_is = np.zeros(x_is.shape)
        a_is = np.ones(x_is.shape)
        a_is[-1] = 2
        k_is[-1] = 1

        """ test 2 """

        k_is = np.ones(x_is.shape)
        a_is = np.zeros(x_is.shape)

        a_is[-1] = 2
        k_is[-1] = np.sum(k_is) - 1

        assert k_is[-1]*a_is[-1] > np.sum(k_is) or np.isclose(k_is[-1]*a_is[-1], np.sum(k_is)) and a_is[-1] >= 0,\
           "Conditions on constants a_i and k_i do not hold. Cannot guarantee x_{n+1} > x_{n}"
        
        F_n = -np.sum(k_is*(MIN.pos[0] - a_is*(x_is + xi_is)))
        F_o = 0*F_o[0]
      
      elif self.kind == LineExploreKind.TWO_DIM_GLOBAL:
        k_is = np.zeros(len(beacons))
        k_is[-1] = 1
        x_is = np.concatenate([b.pos.reshape(2, 1) for b in beacons], axis=1)
        xi_is = np.array([MIN.get_RSSI(b) for b in beacons])*np.ones((2, 1))
        F_n = -np.sum(k_is*(MIN.pos.reshape(2, 1) - (x_is + xi_is)), axis=1).reshape(2, )
   
    else:
      """ LOCAL METHODS """
      neigh_indices, = np.where(xi_is > self.RSSI_TRHESHOLD)
      land_due_to_no_neighs = len(neigh_indices) == 0
      
      if land_due_to_no_neighs:
          print(f"{MIN.ID} STOPPED due to no neighs")
      else:
        self.neighs = beacons[neigh_indices]

        x_is = x_is[:, neigh_indices]
        xi_is = xi_is[neigh_indices]

        if self.kind == LineExploreKind.ONE_DIM_LOCAL:
          x_is = x_is[0, :]

          m = np.argmax(x_is)

          k_is = np.ones(x_is.shape)
          a_is = 1.1*np.ones(x_is.shape)

          a_is[m] = (1/k_is[m])*np.sum(k_is) + 1


          """ Leads to equally spaced drones """
          #k_is = np.zeros(x_is.shape)
          #k_is[j] = 2*1
          #a_is[j] = 1

          """ Using qualitative info. about xi function vol. 1"""
          a_is = np.ones(x_is.shape)
          a_is[m] = 1.1
          k_is = np.ones(x_is.shape)

          delta_is = np.array([b.get_xi_max_decrease() for b in self.neighs])

          k_is[m] = (1/(a_is[m]-1))*np.sum(np.delete(k_is*(1+a_is*delta_is), m)) + 0.1
          
          """ Using qualitative info. about xi function vol. 2"""
          k_is = np.ones(x_is.shape)
          a_is = np.ones(x_is.shape)

          a_is[m] = (1/k_is[m])*np.sum(np.delete(k_is*(1+a_is*delta_is), m)) + 1

          assert (k_is[m]*a_is[m] > np.sum(k_is) or np.isclose(k_is[m]*a_is[m], np.sum(k_is))) and a_is[m] >= 0,\
            f"""
            Conditions on constants a_i and k_i do not hold. Cannot guarantee x_n_plus_one > max(x_i) for i in neighbors of nu_n_plus_one.
            {k_is[m]*(a_is[m] - 1)} >=? {np.sum(np.delete(k_is, m))} and {a_is[m]} >= 0.
            """
            
          F_n = np.array([-np.sum(k_is*(MIN.pos[0] - a_is*(x_is + xi_is))), 0])
          F_o = 0*F_o

        else:
          v_is = np.concatenate([
            b.exploration_dir.reshape(2, 1) for b in self.neighs
          ], axis=1)

          """ Behdads gain approach """

          k_is = np.array([b.k for b in self.neighs])
          a_is = np.array([b.a for b in self.neighs])

          MIN.a = np.min(a_is) + 1
          MIN.k = 1

          """ Testing dynamic gains """

          l = np.argmax(np.array([b.ID for b in self.neighs]))
          k_is = np.ones(neigh_indices.shape)
          a_is = np.zeros(neigh_indices.shape)
          a_is[l] = neigh_indices.shape[0]

          """ Calculating force """
          F_n = -np.sum(k_is*(MIN.pos.reshape(2, 1) - a_is*(x_is + xi_is*v_is)), axis=1).reshape(2, )
      
    F = F_n + F_o
    at_landing_condition = land_due_to_no_neighs or np.linalg.norm(F) < self.force_threshold
    if at_landing_condition:
      MIN.exploration_dir = self.get_exploration_dir_callback(MIN, self.neighs, F_o)
      raise AtLandingConditionException
    return F

  @staticmethod
  def __clamp(F, limit):
    norm_F = np.linalg.norm(F)
    if norm_F > limit:
      return limit*F/norm_F
    return F