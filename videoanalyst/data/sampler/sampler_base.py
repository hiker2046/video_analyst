# -*- coding: utf-8 -*-

import json
import pickle
import tarfile
import time
from abc import ABCMeta, abstractmethod
from typing import List, Dict

import cv2 as cv
import nori2 as nori
import numpy as np

from yacs.config import CfgNode

from videoanalyst.data.dataset.dataset_base import DatasetBase
from videoanalyst.utils import Registry

TRACK_SAMPLERS = Registry()
VOS_SAMPLERS = Registry()

TASK_SAMPLERS = Dict(
    track=TRACK_SAMPLERS,
    vos=VOS_SAMPLERS,
)

class SamplerBase:
    __metaclass__ = ABCMeta

    r"""
    base class for Sampler. Reponsible for sampling from multiple datasets and forming training pair / sequence.

    Define your hyper-parameters here in your sub-class.
    """
    default_hyper_params = dict()

    def __init__(self, datasets: List[DatasetBase]=[], seed: int=0) -> None:
        r"""
        Dataset Sampler, reponsible for sampling from different dataset

        Arguments
        ---------
        cfg: CfgNode
            data config, including cfg for datasset / sampler
        datasets: List[DatasetBase]
            collections of datasets
        seed: int
            seed to initialize random number generator
            important while using multi-worker data loader
        """
        self._hyper_params = self.default_hyper_params
        self._state = dict()
        self.datasets = datasets
        self._state["rng"] = np.random.RandomState(seed)

    def get_hps(self) -> dict:
        r"""
        Getter function for hyper-parameters

        Returns
        -------
        dict
            hyper-parameters
        """
        return self._hyper_params

    def set_hps(self, hps: dict) -> None:
        r"""
        Set hyper-parameters

        Arguments
        ---------
        hps: dict
            dict of hyper-parameters, the keys must in self.__hyper_params__
        """
        for key in hps:
            if key not in self._hyper_params:
                raise KeyError
            self._hyper_params[key] = hps[key]
            
    def update_params(self) -> None:
        r"""
        an interface for update params
        """

    def __next__(self) -> dict:
        r"""
        An interface to sample data
        """
