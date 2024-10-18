"""
Class for a single task in a Meta Learning environnement

Note:
A task instance does not have all the information required to perform the training. Notably, it
lacks the ProbaMap object necessary to interpret the post_param, as well as the prior. As such,
the task can only be interpreted in the wider context of a MetaLearningEnv object.
"""

import os
from typing import Callable, Optional

import apicutils.basic_io as io
from picproba.types import ProbaParam, SamplePoint
from picmeta.types import MetaData
from picoptim.fun_evals import FunEvals


class Task:
    """
    Class for a single learning task.

    A task instance does not have all the information required to perform the training. Notably, it
    lacks the ProbaMap object necessary to interpret the post_param, as well as the prior. As such,
    the task can only be interpreted in the wider context of a MetaLearningEnv object.

    Attributes:
        score: scoring function for the task.
        temperature: the temperature of the task.
        post_param: the currently trained posterior parameter (prior as well as ProbaMap is
            specified in the MetaLearningEnv).
        accu_sample_val: FunEvals container for evaluation of the score.
        meta_data: MetaData of the task.
        save_path: where the task data is saved.
        parallel: should 'score' calls be parallelized.
        vectorized: is 'score' vectorized.

    Method:
        save. Save the task data (can be loaded later through load_task function).
            score and meta_data are pickled (using 'dill' package). The rest are stored in
            human readable function.
    """

    def __init__(
        self,
        score: Callable[[SamplePoint], float],
        temperature: float = 1.0,
        post_param: Optional[ProbaParam] = None,
        accu_sample_val: Optional[FunEvals] = None,
        meta_data: Optional[MetaData] = None,
        train_hyperparams: Optional[dict] = None,
        save_path: Optional[str] = None,
        parallel: bool = True,
        vectorized: bool = False,
    ):
        self.score = score
        self.post_param = post_param
        self.accu_sample_val = accu_sample_val
        self.temp = temperature

        self.meta_data = meta_data

        if train_hyperparams is None:
            self.train_hyperparams = {}
        else:
            self.train_hyperparams = train_hyperparams

        self.parallel = parallel
        self.vectorized = vectorized

        self.end_score = None
        self.save_path = save_path

    def save(
        self, name: Optional[str], path: Optional[str] = None, overwrite: bool = True
    ) -> str:
        """Save Task data

        Task data is saved in folder 'name' situated at 'path'.
        If 'name' is not provided, defaults to saving in 'save_path'.

        Function "score" is saved using 'dill' library.
        """
        # Check that path + name provided are coherent
        if name is not None:
            if path is None:
                path = "."
            if not os.path.isdir(path):
                raise ValueError(f"{path} should point to a folder")
            acc_path = os.path.join(path, name)
            os.makedirs(acc_path, exist_ok=overwrite)
        else:
            acc_path = self.save_path  # type: ignore
            if acc_path is None:
                raise ValueError(
                    "Could not interpret where to save (save_path argument missing and name not provided)"
                )

        def mk_pth(name):
            return os.path.join(acc_path, name)

        # Save accu_sample_val
        # The name of the subclass is also saved for future loading
        if self.accu_sample_val is not None:
            self.accu_sample_val.save(
                name=self.FUN_EVALS_PATH, path=acc_path, overwrite=overwrite
            )

        # Save score function (dill)
        io.rw_dl.save(mk_pth(self.SCORE_PATH), self.score)
        io.rw_dl.save(mk_pth(self.META_DATA_PATH), self.meta_data)
        io.rw_jsonlike.save(mk_pth(self.INFO_PATH),{
            "post_param":self.post_param,
            "temperature":self.temp,
            "parallel":self.parallel,
            "vectorized":self.vectorized
            }, )
        return acc_path

    FUN_EVALS_PATH = "FUN_EVALS"
    SCORE_PATH = "SCORE.dl"
    META_DATA_PATH = "META_DATA.dl"
    INFO_PATH = "INFO.json"

    @classmethod
    def load(cls, path):
        def mk_pth(name):
            return os.path.join(path, name)
        score = io.rw_dl.load(mk_pth(cls.SCORE_PATH))
        accu_sample_val = FunEvals.load(mk_pth(cls.FUN_EVALS_PATH))
        meta_data = io.rw_dl.load(mk_pth(cls.META_DATA_PATH))
        info = io.rw_jsonlike(mk_pth(cls.INFO_PATH))

        return cls(score=score, accu_sample_val=accu_sample_val, meta_data=meta_data, **info)